# -*- coding: utf-8 -*-

import os
import random
import csv


def partition_data_set(path_root, k):
    """
    此函数将数据集随机划分成n等份，仅将划分规则写入文件，并无实质的文件移动。
    :param path_root: 数据集所在的根目录。
    :param k: 数据集的第k次划分。
    :return: none
    """
    path_tmp = path_root + '/tmp'  # 存放临时文件的路径
    if not os.path.exists(path_tmp):
        os.mkdir(path_tmp)

    marks = random.sample(xrange(1, 21), 20)  # 子集划分标记
    with open(path_tmp + '/cross_validation_' + str(k) + '.csv', 'wb') as split_file:
        csv_writer = csv.writer(split_file)
        for i in range(5):
            csv_writer.writerow(['Partition_' + str(i + 1)] + marks[i * 4:i * 4 + 4])


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):
        path = path.replace('\\', '/')
    if path == '':
        partition_data_set(path_root='C:/ScriptData/RandForest', k=1)
    else:
        partition_data_set(path_root=path)


if __name__ == '__main__':
    main()
