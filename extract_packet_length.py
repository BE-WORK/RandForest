# -*- coding: utf-8 -*-

# import datetime
import os
import csv


def extract_packet_length(path_root, csv_file, is_train_data):
    """
    此函数处理单个传入的csv文件，抽取数据包Length字段。
    :param path_root:数据集所在的根目录。
    :param csv_file: 传入的csv文件路径。
    :param is_train_data: 传入的标示，用于判断当前处理的是训练集数据还是测试集数据。
    :return:none
    """
    path_tmp = path_root + '/tmp'
    if is_train_data:
        length_file = file(path_tmp + '/train.csv', 'a')
    else:
        length_file = file(path_tmp + '/test.csv', 'a')

    with open(csv_file, 'rb') as file_obj:
        csv_reader = csv.reader(file_obj)
        file_name = csv_file.split('/')[-1]
        page_name = file_name[:file_name.rfind('-')]
        # print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start loading ' + file_name + '...'
        incoming = []
        outgoing = []
        bidirectional = []

        ipv4 = '172.29.23.168'  # 我电脑的ipv4地址
        for order, date, src, dst, pro, length in csv_reader:
            if dst.find(ipv4) != -1:
                incoming.append(length)
            if src.find(ipv4) != -1:
                outgoing.append(length)
            if length.find('Length') == -1:
                bidirectional.append(length)

        # 将抽取的Length字段写入目标文件
        count_in_a_cell = 0  # 用于控制每个excel单元格存储的数据包Length字段的数目（使单元格字符数目不溢出）
        for income in incoming:  # 第一行写入incoming方向的数据包Length字段
            length_file.write(income + ' ')
            count_in_a_cell = count_in_a_cell + 1
            if count_in_a_cell == 1000:  # 每个excel单元格写入1000个Length字段
                count_in_a_cell = 0
                length_file.write(',')
        length_file.write('\n')
        count_in_a_cell = 0
        for outgo in outgoing:  # 第二行写入outgoing方向的数据包Length字段
            length_file.write(outgo + ' ')
            count_in_a_cell = count_in_a_cell + 1
            if count_in_a_cell == 1000:
                count_in_a_cell = 0
                length_file.write(',')
        length_file.write('\n')
        count_in_a_cell = 0
        for bidirection in bidirectional:  # 第三行写入bidirectional方向的数据包Length字段
            length_file.write(bidirection + ' ')
            count_in_a_cell = count_in_a_cell + 1
            if count_in_a_cell == 1000:
                count_in_a_cell = 0
                length_file.write(',')
        length_file.write('\n')
        length_file.write(page_name + '\n')  # 第四行写入前三行对应的网页标签

    length_file.close()


def extract_length_feature(path_root, k, partition_num):
    """
    此函数分别为训练集和测试集数据抽取数据包Length字段。
    :param path_root: 数据集所在的根目录。
    :param k: 第k此交叉验证。
    :param partition_num: 以编号为partition_num的子集作为测试集。
    :return: none
    """
    path_train_features = path_root + '/tmp/train.csv'
    path_test_features = path_root + '/tmp/test.csv'
    path_csv = path_root + '/data_csv'
    path_cv_k = path_root + '/tmp/cross_validation_' + str(k) + '.csv'

    # 先清除之前的数据
    if os.path.exists(path_train_features):
        os.remove(path_train_features)
    if os.path.exists(path_test_features):
        os.remove(path_test_features)

    train_set = []  # 标记训练集
    test_set = []  # 标记测试集
    with open(path_cv_k, 'rb') as split_file:
        csv_reader = csv.reader(split_file)
        for partition, f1, f2, f3, f4 in csv_reader:
            if partition_num == int(partition[-1]):
                test_set.append(f1)
                test_set.append(f2)
                test_set.append(f3)
                test_set.append(f4)
            else:
                train_set.append(f1)
                train_set.append(f2)
                train_set.append(f3)
                train_set.append(f4)

    goods = os.listdir(path_csv)
    for g in goods:
        pages = os.listdir(path_csv + '/' + g)
        for p in pages:
            fetches = os.listdir(path_csv + '/' + g + '/' + p)
            for f in fetches:
                instance_num = f.split('-')[-1].split('.')[0]
                if instance_num in train_set:  # 判断当前实例是否属于训练集
                    extract_packet_length(path_root, path_csv + '/' + g + '/' + p + '/' + f, True)
                else:
                    extract_packet_length(path_root, path_csv + '/' + g + '/' + p + '/' + f, False)


def main():
    path = raw_input('Enter the root path of your data: ')
    if path.find('\\'):  # 转换路径格式
        path = path.replace('\\', '/')
    if path == '':
        extract_length_feature(path_root='C:/ScriptData/RandForest', k=1, partition_num=1)
    else:
        extract_length_feature(path_root=path, k=1, partition_num=1)


if __name__ == '__main__':
    main()
