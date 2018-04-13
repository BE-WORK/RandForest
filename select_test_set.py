# -*- coding:utf-8 -*-

import os
import shutil


def select_test_set(path_root, k, partition_num):
    """
    此函数在n个子集中选出1个测试集，剩余作为训练集，并将数据拷贝至相应位置。
    :param path_root: 数据集所在的路径。
    :param k: 第k次数据集划分，即第k此交叉验证。
    :param partition_num: 第partition_num个数据子集，用于测试。
    :return: none
    """
    path_train = path_root + '/tmp/data_train'  # 训练集所在路径
    path_test = path_root + '/tmp/data_test'  # 测试集所在路径
    path_data = path_root + '/tmp/cross_validation_' + str(k)  # 划分子集所在路径

    if os.path.exists(path_train):  # 如果存在，先清除数据
        shutil.rmtree(path_train)
        os.mkdir(path_train)
    else:
        os.mkdir(path_train)

    if os.path.exists(path_test):
        shutil.rmtree(path_test)
        os.mkdir(path_test)
    else:
        os.mkdir(path_test)

    partitions = os.listdir(path_data)
    for partition in partitions:
        files = os.listdir(path_data + '/' + partition)
        if partition[-1] == str(partition_num):  # 将目标子集移至测试集所在目录
            for f in files:
                shutil.copy(path_data + '/' + partition + '/' + f, path_test)
        else:  # 将剩余子集移至训练集所在目录
            for f in files:
                shutil.copy(path_data + '/' + partition + '/' + f, path_train)


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):  # 转换路径格式
        path = path.replace('\\', '/')
    if path == '':
        select_test_set(path_root='C:/ScriptData/RandForest', k=1, partition_num=1)
    else:
        select_test_set(path_root=path, k=1, partition_num=1)


if __name__ == '__main__':
    main()
