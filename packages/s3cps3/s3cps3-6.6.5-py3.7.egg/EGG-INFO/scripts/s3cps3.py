import sys, boto3, json, os
from botocore.config import Config
import queue, threading
from concurrent import futures
from loguru import logger
from commons import parse_aws_param

input_path = sys.argv[1] # 内含jsonl
src_profile = sys.argv[2]
dest_profile = sys.argv[3]
thread_cnt = int(sys.argv[4])

src_ak, src_sk, src_end_point, src_addressing_style = parse_aws_param(src_profile)
dest_ak, dest_sk, dest_end_point, dest_addressing_style = parse_aws_param(dest_profile)

src_cli_config = Config(**{
            #使用Python里的字典解包功能创建一个Config类的实例
            "connect_timeout": 60,
            "read_timeout": 20,
            "max_pool_connections": 500,
            "s3": {
                "addressing_style": src_addressing_style,
            },
            "retries": {
                "max_attempts": 3,
            }
        })
dest_cli_config = Config(**{

            "connect_timeout": 60,
            "read_timeout": 20,
            "max_pool_connections": 200,
            "s3": {
                "addressing_style": dest_addressing_style,
            },
            "retries": {
                "max_attempts": 3,
            }
        })

src_cli =  boto3.session.Session().client("s3", aws_access_key_id=src_ak,  aws_secret_access_key=src_sk,  endpoint_url=src_end_point, region_name='', config=src_cli_config)
dest_cli = boto3.session.Session().client("s3", aws_access_key_id=dest_ak, aws_secret_access_key=dest_sk, endpoint_url=dest_end_point, region_name='', config=dest_cli_config)
cur_thread_id = threading.get_ident()

# 接下来开启线程，开始copy
class ThreadPoolExecutorWithQueueSizeLimit(futures.ThreadPoolExecutor):
    def __init__(self, max_workers=10, *args, **kwargs):
        """
        param: max_workers 最多并发执行数
        param: len_queue  队列长队 至少为 1
        """
        super().__init__(max_workers, *args, **kwargs)
        self._work_queue = queue.Queue(maxsize=max_workers*2)
        self.total_files = 0
        self.copyed_cnt = 0

    def qsize(self):
        return self._work_queue.qsize()
    
    def do_copy(self, src_bucket, src_path, dest_bucket, dest_path):
        try:
            src_path = src_path.strip()
            dest_path = dest_path.strip()
            res = src_cli.get_object(Bucket=src_bucket, Key=src_path)
            file_content = res["Body"].read()
            
            #logger.info(f">>上传：s3://{src_bucket}/{src_path} ==> s3://{dest_bucket}/{dest_path}")
            response = dest_cli.put_object(Bucket=dest_bucket, Key=dest_path, Body=file_content)
            #logger.info(f"<<上传：s3://{src_bucket}/{src_path} ==> s3://{dest_bucket}/{dest_path}")
            
            if 'ETag' in response:
                #logger.info(f"s3://{src_bucket}/{src_path} ==> s3://{dest_bucket}/{dest_path}")
                self.copyed_cnt += 1
                if self.copyed_cnt % 10000 == 0:
                    logger.info(f"{cur_thread_id}已完成：{self.copyed_cnt}/{self.total_files}")
                return True, None
            else:
                logger.error(f"s3://{src_bucket}/{src_path} ==> s3://{dest_bucket}/{dest_path}上传失败：{response}")
                exit(-1)
        except Exception as e:
            logger.error(f"s3://{src_bucket}/{src_path} ==> s3://{dest_bucket}/{dest_path}上传失败：{response}")
            logger.exception(e)
            exit(-1)
    
src_buckets = []
src_paths = []
dest_buckets = []
dest_paths = []

with open(input_path, "r", encoding='utf-8') as f:
    for l in f:
        o = json.loads(l)
        src_buckets.append(o["src_bucket"])
        src_paths.append(o["src_path"])
        dest_buckets.append(o["dst_bucket"])
        dest_paths.append(o["dst_path"])

total_files = len(src_buckets)
with ThreadPoolExecutorWithQueueSizeLimit(max_workers=thread_cnt) as thread_pooll:
    thread_pooll.total_files = total_files
    thread_pooll.map(thread_pooll.do_copy, src_buckets, src_paths, dest_buckets, dest_paths, chunksize=20)

logger.info(f"线程 {cur_thread_id} copy {total_files} 个文件成功")
exit(0)
