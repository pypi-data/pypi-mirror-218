# 第一：list 出来文件和路径
# 根据文件路径分炒年糕 大文件和小文件的list

#对于小文件启动python多进程+多线程传输
#对于大文件，启动脚本传输
# 以上两者并行

#!/usr/env xonsh
import sys,re,json,math
from loguru import logger
import uuid
import threading
import click
import os
import json


@click.command()
@click.option('--s', help='src_profile@s3://path/to/src/', required=True)
@click.option('--d', help='dst_profile@s3://path/to/dst/', required=True)
@click.option('--t', default=10, help='copy 大文件的进程数')
@click.option('--p', default=30, help='执行小文件copy的进程数')
@click.option('--c', default=False, help='是否重用list文件，由于扫描bucket可能很久，如果发生意外可以重新利用已经扫描生成的list文件（如果发现有）')
def main(s, d, t, p, c):
    file_sz_threadhold=1024*1024*10 # 10MB
    thread_per_process = 30
    src = s
    dst = d
    bigfile_copy_thread = t
    num_py_process = p
    #创建临时文件地址
    source_path_sorted=$(mktemp -t s32s3.XXX)
    dest_path_sorted=$(mktemp -t s32s3.XXX)
    file_to_copy=$(mktemp -t s32s3.XXX)
    bigfile=$(mktemp -t s32s3.XXX)
    littlefile=$(mktemp -t s32s3.XXX)
    uni=$(echo @(src+dst) | md5sum | cut -d ' ' -f 1)
    uni=uni.strip()
    bigpermanentfile = "big"+uni+".txt"
    littlepermanentfile = "little"+uni+".txt"
    # 删除存的哈希值的开头和结尾的空白字符
    source_path_sorted=source_path_sorted.strip()
    dest_path_sorted=dest_path_sorted.strip()
    file_to_copy=file_to_copy.strip()
    bigfile=bigfile.strip()
    littlefile=littlefile.strip()
    #使用正则匹配找到形如user@s3://bucket/path/to/obj/,三个括号应该包含三个部分，用户名，桶的名称，文件路径
    s3info = re.findall(r"(\w+)@s3:\/\/([^\/]+)\/(.*)", src)
    if not s3info or len(s3info[0])!=3:
        logger.error(f"{src} format ERROR")
        exit(-1)

    src_profile = s3info[0][0]
    src_bucket = s3info[0][1]
    src_path = s3info[0][2]
    if src_path.endswith("/"):
        src_path = src_path[0:-1]

    s3info = re.findall(r"(\w+)@s3:\/\/([^\/]+)\/(.*)", dst)
    if not s3info or len(s3info[0])!=3:
        logger.error(f"{src} format ERROR")
        exit(-1)

    dst_profile = s3info[0][0]
    dst_bucket = s3info[0][1]
    dst_path = s3info[0][2]
    if dst_path.endswith("/"):
        dst_path = dst_path[0:-1]

    def scan(bigfile,littlefile,bigpermanentfile,littlepermanentfile,src,dst):
        source_path_tmp =$(echo @(src) |md5sum |cut -d ' ' -f 1)
        dest_path_temp =$(echo @(dst) |md5sum |cut -d ' ' -f 1)
        source_path_tmp =$(mktemp -t s32s3.XXX)
        dest_path_temp=$(mktemp -t s32s3.XXX)
        source_path_tmp = source_path_tmp.strip()
        dest_path_temp = dest_path_temp.strip()

        #print(os.path.dirname(__file__))
        list_bucket_py = f"{os.path.dirname(__file__)}/listbucket.py"
        rtn1 = !(python3  @(list_bucket_py) @(src) > @(source_path_tmp))
        rtn2 = !(python3  @(list_bucket_py) @(dst) > @(dest_path_temp))
        # 返回码非零代表执行出错
        if rtn1.returncode != 0 or rtn2.returncode != 0:
            logger.error(f"list bucket error: {rtn1.err} {rtn2.err}")
            exit(1)
        else:
            # logger.info("list bucket ok")
            pass

        # -u表示消除排序输出中的重复行，
        sort -u @(source_path_tmp) > @(source_path_sorted)
        sort -u @(dest_path_temp) > @(dest_path_sorted)
        #只传输仅出现在第一个文件的内容
        comm -2 -3 @(source_path_sorted) @(dest_path_sorted) > @(file_to_copy)  # json文件

        # 进行大小分离
        with open(file_to_copy, "r", encoding='utf-8') as f, open(bigfile, "w", encoding="utf-8") as bf, open(littlefile, 'w', encoding='utf-8') as lf:
            with open(littlepermanentfile, "w", encoding='utf-8') as lpf, open(bigpermanentfile, "w", encoding='utf-8') as bpf:
                for l in f:
                    #把json格式的l转化成python里的对象保存在jso中
                    jso = json.loads(l)
                    sizebytes, filepath = jso['size'], jso['path']
                    filepath = filepath.strip()
                    if int(sizebytes) <= file_sz_threadhold:
                        # 分类到小文件，使用python线程实现高并发，提升速度
                        #f"{src_path}/{filepath}"把源路径和文件路径拼接起来，如果源路径为空，则只使用文件路径
                        _src_path = f"{src_path}/{filepath}" if len(src_path)>0  else filepath
                        _dst_path = f"{dst_path}/{filepath}" if len(dst_path)>0  else filepath
                        #创建一个字典存储源和目标存储桶的信息
                        cp_info = {
                            "src_bucket" : src_bucket,
                            "src_path" : _src_path,
                            "src_profile" : src_profile,
                            "dst_bucket" : dst_bucket,
                            "dst_path": _dst_path,
                            "dst_profile": dst_profile
                        }
                        lf.write(f"{json.dumps(cp_info, ensure_ascii=False, sort_keys=True)}\n")#lf里保存的是JSON格式数据
                        lpf.write(f"{json.dumps(cp_info, ensure_ascii=False, sort_keys=True)}\n")
                    else:
                        # 分类到大文件，使用命令提高吞吐
                        _src_path = f"{src_path}/{filepath}" if len(src_path)>0  else filepath
                        _dst_path = f"{dst_path}/{filepath}" if len(dst_path)>0  else filepath

                        cp_info = {
                            "src_profile" : src_profile,
                            "dst_profile": dst_profile,
                            "src_path" : f"s3://{src_bucket}/{_src_path}",
                            "dst_path": f"s3://{dst_bucket}/{_dst_path}",
                        }
                        #s = f"{src_profile}{chr(0)}{dst_profile}{chr(0)}s3://{src_bucket}/{_src_path}{chr(0)}s3://{dst_bucket}/{_dst_path}"
                        #bf.write(f"{s}\n")
                        bf.write(f"{json.dumps(cp_info, ensure_ascii=False,  sort_keys=True)}\n")
                        bpf.write(f"{json.dumps(cp_info, ensure_ascii=False,  sort_keys=True)}\n")
        return  file_to_copy, bigfile, littlefile
    #判断是否读取上次扫描的文件
    if c == 1:
        with open(bigpermanentfile, "r", encoding='utf-8') as readbpf, open(littlepermanentfile, "r",encoding='utf-8') as readlpf:

            bpfsize = os.path.getsize(bigpermanentfile)
            lpfsize = os.path.getsize(littlepermanentfile)
            if bpfsize == 0 and lpfsize == 0:
                scan(bigfile,littlefile,bigpermanentfile,littlepermanentfile,src,dst)
            else:
                with open(bigfile, "w", encoding="utf-8") as bf, open(littlefile, 'w', encoding='utf-8') as lf:
                    for bl in readbpf:
                        bf.write(bl)
                    for ll in readlpf:
                        lf.write(ll)
    else:
        scan(bigfile,littlefile,bigpermanentfile,littlepermanentfile,src,dst)
    #计算需要传输的文件和大小文件的数量
    total_file_cnt = int($(wc -l @(file_to_copy) | cut -d ' ' -f 1))
    total_big_file_cnt = int($(wc -l @(bigfile) | cut -d ' ' -f 1))
    total_little_file_cnt = int($(wc -l @(littlefile) | cut -d ' ' -f 1))
    logger.info(f"TOTAL: {total_file_cnt}")

    if total_file_cnt == 0 and total_little_file_cnt+total_big_file_cnt == 0:
        logger.info(f"{src} : no file to copy")
        exit(0)

    # cat @(littlefile)
    # 对大小文件分别用不同方法进行启动copy
    # 对于小文件，启动boto客户端python代码进行读写。
    # 先对小文件进行分割，按照进程数目分割
    little_file_list = []
    with open(littlefile, "r", encoding='utf-8') as f:
        for l in f:
            little_file_list.append(json.loads(l))

    total_little_file_cnt = len(little_file_list)
    process_need = max(1, total_little_file_cnt//thread_per_process) #需要多少python进程
    process_need = min(process_need, num_py_process)
    #得到每个进程应处理的文件数量
    file_part_sz = math.ceil(total_little_file_cnt//process_need)

    #分割成process_need个小的随机文件
    lfname = f"/tmp/{str(uuid.uuid4())}"
    little_file_path_list = [] # 指向小文件列表的文件
    for i in range(0, process_need):
        little_part_file_name = f"{lfname}_{i}.txt"
        little_file_path_list.append(little_part_file_name) # 存下来，然后传入到每个进程
        file_names = little_file_list[i::process_need] # 分割保存
        with open(little_part_file_name, "w", encoding='utf-8') as f:
            for o in file_names:
                f.write(f"{json.dumps(o, ensure_ascii=False)}\n")

    # 把路径写入文件
    with open(lfname, "w", encoding='utf-8') as f:
        for fp in little_file_path_list:
            f.write(f"{fp}\n")

    def awscli_cp(bigfile, bigfile_copy_thread:int,max_file_bytes:int):
        s3bigcp_sh=f"{os.path.dirname(__file__)}/s3bigcp.sh"
        #cat @(bigfile) | parallel -j @(bigfile_copy_thread) --colsep '\0' ./s3bigcp.sh "{1} {2} {3} {4}" @(max_file_bytes)
        cat @(bigfile) | parallel -j @(bigfile_copy_thread)  @(s3bigcp_sh) "{}" @(max_file_bytes)

    if total_big_file_cnt > 0:
        #读取file_to_copy内容后，使用jq命令提取.size字段，然后sort排序，tail -n 1选取一个最大值
        max_file_bytes=int($(cat @(file_to_copy) | jq '.size'| sort -n | tail -n 1))+1024*1024*10
        bigfile_thread = threading.Thread(target=awscli_cp, args=(bigfile, bigfile_copy_thread,max_file_bytes))
        bigfile_thread.start() # 启动大文件的copy

    if total_little_file_cnt >0:
        s3cps3_py = f"{os.path.dirname(__file__)}/s3cps3.py"
        cat @(lfname) | parallel @(f"-j {process_need} python {s3cps3_py} {{}} {src_profile} {dst_profile} {thread_per_process}".split(' '))

    # 对于大文件直接用awscli进行copy
    #join方法用于阻塞调用此方法的线程
    if total_big_file_cnt > 0:
        bigfile_thread.join()

try:
    main()
except Exception as e:
    logger.exception(e)
    exit(-1)
exit(0)
