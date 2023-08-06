from setuptools import setup, find_packages

from commen.unit_fun import FunBase

setup(
    name='huhangkai',  # 对外模块的名字
    version=FunBase.get_version(),  # 版本号
    description='接口自动化',  # 描述
    author='胡杭凯',  # 作者
    author_email='3173825608@qq.com',
    # package_dir={"": "commen"},
    packages=find_packages(),
    package_data={'by': ['常用命令.py'],},
    include_package_data=True,
    python_requires=">=3.0",
    install_requires=[
        "faker",
        "openpyxl",
        "apscheduler",
        "rsa",
        "pyDes",
        "pycryptodome",
        "xlsxwriter",
        "pandas",
        "apache-beam",
        "pytest",
        "setuptools",
        "twine",
        "requests==2.29.0",
        "pandas",
        "click",
    ],
)


