from setuptools import setup

with open("README.md", "r", encoding="utf-8") as rm:
      long_description = rm.read()

with open("requirements.txt", "r", encoding="utf-8") as rq:
      install_requires = rq.read()

setup(name='s3cps3',
      version='6.6.6',
      packages=['s3cps3'],
      long_description=long_description.replace('\n','\r\n'),
      package_data={'s3cps3':['*.xsh','*.sh']},
      install_requires=install_requires,
      scripts=['s3cps3/s32s3', 's3cps3/main.xsh', 's3cps3/commons.py', 's3cps3/listbucket.py', 's3cps3/s3bigcp.sh', 's3cps3/s3cps3.py',],
      # entry_points={
      #     'console_scripts':[
      #         's3cps3 = s3cps3.transfer:run_xsh_script',
      #     ]
      # },

      )