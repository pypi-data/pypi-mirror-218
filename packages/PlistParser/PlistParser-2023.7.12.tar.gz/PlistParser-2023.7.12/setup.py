#!/usr/bin/python3
# -*- coding: utf-8 -*-


import setuptools  # 导入setuptools打包工具
import PlistParser


with open('requires.txt', 'r', encoding='utf-8') as requires:
    requires = requires.read().split('\n')
with open('README.md', 'r', encoding='utf-8') as README_md:
    long_description = README_md.read()


setuptools.setup(
    license='MIT',
    name='PlistParser',  # 项目名称
    version='2023.7.12',  # test 使用
    # version=PlistParser.__Version__,  # 包版本号，便于维护版本
    url=PlistParser.__ProjectLink__,  # 自己项目地址，比如github的项目地址
    author=PlistParser.__BuildPeople__,  # 作者，可以写自己的姓名
    author_email=PlistParser.__Contact__,  # 作者联系方式，可写自己的邮箱地址
    description=PlistParser.__SimpleDescription__,  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',  # 3 - Alpha | 4 - Beta | 5 - Production/Stable
        'Intended Audience :: Developers',  # 开发的目标用户
        'Topic :: Software Development :: Build Tools',  # 属于什么类型
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    keywords=['Plist', 'PlistParser'],
    platforms=['Windows', 'Linux', 'MacOS'],
    python_requires='>=3.9',  # 对python的最低版本要求
    install_requires=requires,  # 表明当前模块依赖哪些包，若环境中没有，则会从pypi中下载安装
    packages=setuptools.find_packages(),

)
