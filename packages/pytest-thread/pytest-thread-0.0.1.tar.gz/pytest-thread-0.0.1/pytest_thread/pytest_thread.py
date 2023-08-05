# -*-coding:utf-8-*-
# Create File Time:2023/7/7 12:09
# Author: sun chuo
import gevent
from gevent import monkey

monkey.patch_all()


def pytest_addoption(parser):
    # 添加分组
    group = parser.getgroup('pytest-thread')
    # 添加参数信息
    group.addoption('--current', default=None, help='运行的线程数量')
    group.addoption('--runTask', default=None, dest='并发的任务粒度')


def run_test(items):
    """
    并发执行的任务函数
    :param items: 包含用例的列表
    :return:
    """
    for item in items:
        # 执行单条用例
        item.ihook.pytest_runtest_protocol(item=item, nextitem=None)


def pytest_runtestloop(session):
    """pytest用例执行的钩子函数"""
    # 获取命令传入的参数
    print('------', session)
    current = session.config.getoption('--current')
    runTask = session.config.getoption('--runTask')
    if runTask == 'mod':
        case_dict = {}
        # 遍历所有的用例---session.items  --> <list> 用例列表
        for item in session.items:
            # 创建用例的模块属性
            module = item.module

            if case_dict.get(module):
                # 保存用例
                case_dict[module].append(item)  # {‘模块’：‘列表’}
            else:
                case_dict[module] = [item]
        # 以模块为单位并发执行
        glist = []
        for cases in case_dict.values():
            g = gevent.spawn(run_test, cases)
            glist.append(g)
        # 等待所有协程结束
        gevent.joinall(glist)

    return True  # pytest钩子函数特点