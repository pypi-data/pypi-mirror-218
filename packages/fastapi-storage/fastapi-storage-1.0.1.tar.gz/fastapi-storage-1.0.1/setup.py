from __future__ import print_function
from os import path
from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    packages=find_packages(),
    package_data={
        # 如果包中含有.txt文件，则包含它，我这里还有一个ui文件，那么也要包含。
    },
    include_package_data=True,  # 这个一定要设置为True
    entry_points={
        'console_scripts': [
            'storage:link = filesystem.__main__:main'
        ]
    },
    long_description=long_description,
    long_description_content_type='text/markdown'
)
