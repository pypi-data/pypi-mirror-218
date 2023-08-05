import boto3
import json
from botocore.config import Config
import sys, re, os
from loguru import logger
from commons import parse_aws_param

#保存传递给脚本的第一个参数
profile_s3path = sys.argv[1]
if not profile_s3path or not profile_s3path.endswith("/"):
    print("参数需要以/结尾，代表s3上的目录")
    exit(-1)

s3info = re.findall(r"(\w+)@s3:\/\/([^\/]+)\/(.*)", profile_s3path)
if not s3info or len(s3info[0])!=3:
    logger.error(f"{profile_s3path} format ERROR")
    exit(-1)

aws_profile = s3info[0][0]
bucket = s3info[0][1]
path = s3info[0][2]

ak, sk, end_point, addressing_style = parse_aws_param(aws_profile)

try:
    cli = boto3.client(service_name="s3", aws_access_key_id=ak, aws_secret_access_key=sk, endpoint_url=end_point,
                                    config=Config(s3={'addressing_style': addressing_style}))

    def list_obj_scluster():
        marker = None
        while True:
            #创建一个空字典存储限制每次列出桶中的对象个数，s3存储桶的名称，文件路径
            list_kwargs = dict(MaxKeys=1000, Bucket=bucket, Prefix=path)
            if marker:
                list_kwargs['Marker'] = marker
            #获取与list_kwargs参数匹配的S3对象列表，并存储在contents变量中。如果没有查询到任何对象，contents将为一个空列表
            response = cli.list_objects(**list_kwargs)
            contents = response.get("Contents", [])#获取桶内该路径下的对象列表
            yield from contents#一个个返回contents中的值
            if not response.get("IsTruncated") or len(contents)==0:
                break
            marker = contents[-1]['Key']

    for info in list_obj_scluster():
        file_path = info['Key']
        size = info['Size']
        f_info = {"size": size, "path": file_path}

        if path!="":
            f_info['path']=file_path[len(path):]
            #print(f"{size}\t{file_path[len(path):]}")
        else:
            f_info['path'] = file_path
            #print(f"{size}\t{file_path}")
        print(json.dumps(f_info, ensure_ascii=False, sort_keys=True))

except Exception as e:
    logger.exception(e)
    exit(-1)
exit(0)