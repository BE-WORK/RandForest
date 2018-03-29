# -*- coding: utf-8 -*-

import datetime
import os
import csv


def extract_packet_length(csv_file, is_train_data):
    """
    此函数处理单个传入的csv文件，抽取数据包Length字段。
    :param csv_file: 传入的csv文件路径。
    :param is_train_data: 传入的标示，用于判断当前处理的是训练集数据还是测试集数据。
    :return:none
    """
    if is_train_data:
        length_file = file('tmp/train.csv', 'a')
    else:
        length_file = file('tmp/test.csv', 'a')

    file_obj = file(csv_file, 'rb')
    csv_reader = csv.reader(file_obj)
    file_name = csv_file.split('/')[-1]
    page_name = file_name[:file_name.rfind('-')]
    # print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Start loading ' + file_name + '...'
    incoming = []
    outgoing = []
    bidirectional = []

    ipv4 = '172.29.23.168'  # 我电脑的ipv4地址
    ipv6 = '2001:250:1002:2512:bccf:e8de:66d7:85d6'
    for order, date, src, dst, pro, length, content in csv_reader:
        if dst.find(ipv4) != -1 or dst.find(ipv6) != -1:
            incoming.append(length)
        if src.find(ipv4) != -1 or src.find(ipv6) != -1:
            outgoing.append(length)
        if length.find('Length') == -1:
            bidirectional.append(length)

    # print len(incoming), len(outgoing), len(bidirectional)

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

    file_obj.close()
    length_file.close()


def extract_length_feature():
    """
    此函数分别为训练集和测试集数据抽取数据包Length字段。
    :return: none
    """
    # 处理训练集
    if os.path.exists('tmp/train.csv'):  # 先清除之前的数据
        os.remove('tmp/train.csv')
    path_train = 'tmp/data_train'
    files_of_train = os.listdir(path_train)
    for file_train in files_of_train:
        extract_packet_length(path_train + '/' + file_train, True)

    # 处理测试集
    if os.path.exists('tmp/test.csv'):
        os.remove('tmp/test.csv')
    path_test = 'tmp/data_test'
    files_of_test = os.listdir(path_test)
    for file_test in files_of_test:
        extract_packet_length(path_test + '/' + file_test, False)


def main():
    extract_length_feature()


if __name__ == '__main__':
    main()
