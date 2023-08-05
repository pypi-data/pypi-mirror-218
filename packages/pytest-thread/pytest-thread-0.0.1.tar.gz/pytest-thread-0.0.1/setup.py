# -*-coding:utf-8-*-
# Create File Time:2023/7/7 12:13
# Author: sun chuo

from setuptools import setup

setup(
    name="pytest-thread",
    version='0.0.1',
    packages=["pytest_thread"],
    # 指定插件文件
    entry_points={"pytest11": ["pytest_thread = pytest_thread.pytest_thread"]},
    # pypi插件分类器
    classifiers=["Framework :: Pytest"],
)

