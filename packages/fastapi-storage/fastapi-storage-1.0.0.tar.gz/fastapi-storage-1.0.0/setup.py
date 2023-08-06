from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(name='fastapi-storage',  # 包名
      version='1.0.0',  # 版本号
      description='A small example package',
      long_description=long_description,
      author='xjaqil',
      author_email='1203227985@qq.com',
      url='https://mp.weixin.qq.com/s/9FQ-Tun5FbpBepBAsdY62w',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Topic :: Software Development :: Libraries'
      ],
      )
