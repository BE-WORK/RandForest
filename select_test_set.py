# -*- coding:utf-8 -*-

import os
import shutil


def select_test_set(k, partition_num):
    """
    此函数在n个子集中选出1个测试集，剩余作为训练集，并将数据拷贝至相应位置。
    :param k: 第k次数据集划分，即第k此交叉验证。
    :param partition_num: 第partition_num个数据子集，用于测试。
    :return: none
    """
    path_train = 'tmp/data_train'  # 训练集所在路径
    path_test = 'tmp/data_test'  # 测试集所在路径
    path_data = 'tmp/cross_validation_' + str(k)  # 划分子集所在路径

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
    select_test_set(1, 1)


if __name__ == '__main__':
    main()
