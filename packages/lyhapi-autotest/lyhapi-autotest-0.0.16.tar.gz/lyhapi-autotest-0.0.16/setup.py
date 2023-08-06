# coding=utf-8
"""
作者：vissy@zhu
"""
from setuptools import setup, find_packages
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
setup(
    name="lyhapi-autotest",
    version="0.0.16",
    author="vissy0429",
    author_email="1187463903@qq.com",
    description="lyh interface autoTest",
    url="https://github.com/vissyzhu/lyhapi.git",
    license='MIT',
    packages=find_packages(),
    # zip_safe=False
)
