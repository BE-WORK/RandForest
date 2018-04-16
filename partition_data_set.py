# -*- coding: utf-8 -*-

import os
import random
import csv


def partition_data_set(path_root, n_instance, k, n):
    """
    此函数将数据集随机划分成n等份，仅将划分规则写入文件，并无实质的文件移动。
    :param path_root: 数据集所在的根目录。
    :param k: 数据集的第k次划分。
    :return: none
    """
    path_tmp = path_root + '/tmp'  # 存放临时文件的路径
    if not os.path.exists(path_tmp):
        os.mkdir(path_tmp)

    marks = random.sample(xrange(1, n_instance + 1), n_instance)  # 子集划分标记
    with open(path_tmp + '/cross_validation_' + str(k) + '.csv', 'wb') as split_file:
        csv_writer = csv.writer(split_file)
        subset_size = n_instance / n
        for i in range(n):
            csv_writer.writerow(['Partition_' + str(i + 1)] + marks[i * subset_size:i * subset_size + subset_size])


def main():
    path = raw_input('Enter the root path of your data: ')
    if '' == path:
        path = 'C:/ScriptData/RandForest'
    elif path.find('\\') != -1:  # 转换路径格式
        path = path.replace('\\', '/')
    n_instance = raw_input('Enter the number of instances of a page: ')
    if '' == n_instance:
        n_instance = 20
    partition_data_set(path_root=path, n_instance=n_instance, k=1, n=5)


if __name__ == '__main__':
    main()
