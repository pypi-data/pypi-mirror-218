import os, re, configparser

def parse_aws_param(profile):
    # 解析配置文件,把文件路径组合起来，把代表用户主目录符号替换成用户主目录路径
    config_file = os.path.join(os.path.expanduser("~"), ".aws", "config")
    credentials_file = os.path.join(os.path.expanduser("~"), ".aws", "credentials")
    config = configparser.ConfigParser()
    config.read(credentials_file)
    config.read(config_file)
    # 获取 AWS 账户相关信息
    ak = config.get(profile, "aws_access_key_id")
    sk = config.get(profile, "aws_secret_access_key")
    if profile == "default":
        s3_str = config.get(f"{profile}", "s3")
    else:
        s3_str = config.get(f"profile {profile}", "s3")
    end_match = re.search("endpoint_url[\s]*=[\s]*([^\s\n]+)[\s\n]*$", s3_str, re.MULTILINE)
    if end_match:
        endpoint = end_match.group(1)
    else:
        raise ValueError(f"aws 配置文件中没有找到 endpoint_url")
    style_match = re.search("addressing_style[\s]*=[\s]*([^\s\n]+)[\s\n]*$", s3_str, re.MULTILINE)
    if style_match:
        addressing_style = style_match.group(1)
    else:
        addressing_style = "path"
    return ak, sk, endpoint, addressing_style
