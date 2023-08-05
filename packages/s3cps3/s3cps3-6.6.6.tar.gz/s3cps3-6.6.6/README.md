
## 命令功能
#### 实现数据桶到数据桶之间的数据传输功能，无需先下载到本地再上传；
#### 考虑到可能遇到大批量小文件传输的需求，本包可实现通过扫描分割大小文件，并将大文件通过aws包的cp命令传输，为小文件分配python多线程传输，提高传输效率;
#### 考虑到可能遇到各种因素导致传输中断，在中断后为了节省时间可以通过读取上一次扫描后生成的大小文件列表，跳过重新扫描这一步骤；


## 安装
### linux命令
s3cps3及其依赖项的安装使用pip和setuptools提供的一系列打包功能。为保证安装顺利，建议使用：
#### pip:9.0.2或更高版本
#### setuptools：36.2.0或更高版本
#### 安装s3cps3最安全的方法实在virtualenv中使用pip：
$ pip -m install s3cps3
#### 或者，如果您没有在virtualenv中安装，则全局安装：
$ sudo python -m pip install s3cps3
### awscli配置
#### 在使用s3cps3之前，您需要配置AWS凭证，您可以通过多种方式执行此操作：
#### 最快的入门方法是运行aws configure命令：
#### $ aws configure
#### AWS Access Key ID: MYACCESSKEY
#### AWS Secret Access Key: MYSECRETKEY
#### Default region name [us-west-2]: us-west-2
#### Default output format [None]: json
#### 要使用环境变量，请执行以下操作：
#### $ export AWS_ACCESS_KEY_ID=<access_key>
#### $ export AWS_SECRET_ACCESS_KEY=<secret_key>
#### 要使用共享凭据文件(credentials)，请创建一个INI格式的文件，如下所示：
#### [default]
#### aws_access_key_id=MYACCESSKEY
#### aws_secret_access_key=MYSECRETKEY

#### [testing]
#### aws_access_key_id=MYACCESKEY
#### aws_secret_access_key=MYSECRETKEY

#### 要使用配置文件，请创建一个INI格式的文件，如下所示：
#### [default]
#### aws_access_key_id=default access key
#### aws_secret_access_key=default secret key

#### [profile testing]
#### aws_access_key_id=testing access key
#### aws_secret_access_key=testing secret key

#### [plugins]
#### endpoint = awscli_plugin_endpoint

## 使用
#### s3cps3命令具有以下结构：
#### s32cp options parameters options parameters ..
#### 例如，从源数据桶传输文件到目标数据桶，可以参考：
#### s32s3 --s src_profile@s3://path/to/src/ --d dst_profile@s3://path/to/dst/
#### 如果想要调用上次扫描的大小文件列表，可以参考：
#### s32s3 --s src_profile@s3://path/to/src/ --d dst_profile@s3://path/to/dst/ --c 1



