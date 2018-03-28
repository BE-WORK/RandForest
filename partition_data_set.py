# -*- coding: utf-8 -*-

import os
import shutil
import random


def partition_data_set(k, n):
    """
    此函数将数据集随机划分成n等份。
    :param k: 数据集的第k次划分。
    :param n: 将数据集划分成n等份。
    :return: none
    """
    path_data_set = 'data_csv'  # 数据集存放的路径
    path_tmp = 'tmp'  # 存放临时文件的路径
    if not os.path.exists(path_tmp):
        os.mkdir(path_tmp)
    if not os.path.exists(path_tmp + '/cross_validation_' + str(k)):  # 判断路径“tmp/cross_validation_k”是否存在
        os.mkdir(path_tmp + '/cross_validation_' + str(k))
    for i in range(1, n + 1):
        if not os.path.exists(path_tmp + '/cross_validation_' + str(k) + '/partition_' + str(
                i)):  # 判断路径“tmp/cross_validation_k/partition_i”是否存在
            os.mkdir(path_tmp + '/cross_validation_' + str(k) + '/partition_' + str(i))

    marks = random.sample(xrange(0, 20), 20)  # 子集划分标记

    goods = os.listdir(path_data_set)
    for g in goods:
        pages = os.listdir(path_data_set + '/' + g)
        for p in pages:
            fetches = os.listdir(path_data_set + '/' + g + '/' + p)
            partition_number = 1  # 记录当前子集编号
            cnt = 0  # 记录给当前子集中拷贝的文件数目
            for i in range(len(fetches)):
                shutil.copy(path_data_set + '/' + g + '/' + p + '/' + fetches[marks[i]],
                            path_tmp + '/cross_validation_' + str(k) + '/partition_' + str(partition_number))
                cnt += 1
                if cnt == 4:
                    cnt = 0
                    partition_number += 1


def main():
    partition_data_set(1, 5)


if __name__ == '__main__':
    main()
