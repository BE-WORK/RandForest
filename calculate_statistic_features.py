# coding: utf-8

import csv
import numpy as np
from pandas import DataFrame
from sklearn import preprocessing


def calculate_statistic_features(incomes, outgoes, bidirections):
    """
    此函数计算单个流量文件的54个统计量。
    :param incomes: 存放目的地址为本机的数据包Length字段列表。
    :param outgoes: 存放源地址为本机的数据包Length字段列表。
    :param bidirections: 存放双向数据包Length字段列表。
    :return:none
    """
    if len(incomes) == 1 or len(incomes) == 0:
        incomes = [0, 0, 0]
    if len(outgoes) == 1 or len(outgoes) == 0:
        outgoes = [0, 0, 0]
    if len(bidirections) == 1 or len(bidirections) == 0:
        bidirections = [0, 0, 0]
    hist = {}
    incomes = incomes.split(' ')
    incomes = map(int, incomes[:-1])  # 最后一个元素是空字符串:''
    hist['incomes'] = {}
    for i in range(54, 1515):
        hist['incomes'][i] = 0
    for income in incomes:
        hist['incomes'][income] += 1
    result = hist['incomes'].values()

    outgoes = outgoes.split(' ')
    outgoes = map(int, outgoes[:-1])
    hist['outgoes'] = {}
    for i in range(54, 1515):
        hist['outgoes'][i] = 0
    for outgo in outgoes:
        hist['outgoes'][outgo] += 1
    result += hist['outgoes'].values()

    bidirections = bidirections.split(' ')
    bidirections = map(int, bidirections[:-1])
    hist['bidirections'] = {}
    for i in range(54, 1515):
        hist['bidirections'][i] = 0
    for key in hist['incomes']:
        hist['bidirections'][key] = hist['incomes'][key] + hist['outgoes'][key]
    result += hist['bidirections'].values()

    return result


def statistic_features():
    """
    此函数分别为训练集和测试集计算所有流量文件的统计量。
    :return: none
    """
    # 处理训练集
    file_obj = file('tmp/train.csv', 'rb')
    csv_reader = csv.reader(file_obj)
    features_file_train = file('tmp/features-train.csv', 'w')
    cnt = 0  # 文件中每4行代表一个网页
    flows = []
    for order in csv_reader:
        if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
            order.pop()
        flows.append(''.join(order[:]))
        cnt = cnt + 1
        if cnt == 4:  # 一个网页的完整数据已读入
            features = calculate_statistic_features(flows[0], flows[1], flows[2])
            for i in features:
                features_file_train.write(str(i) + ',')
            features_file_train.write(flows[3] + '\n')
            flows = []
            cnt = 0
    file_obj.close()
    features_file_train.close()

    # 处理测试集
    file_obj = file('tmp/test.csv', 'rb')
    csv_reader = csv.reader(file_obj)
    features_file_test = file('tmp/features-test.csv', 'w')
    cnt = 0  # 文件中每4行代表一个网页
    flows = []
    for order in csv_reader:
        if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
            order.pop()
        flows.append(''.join(order[:]))
        cnt = cnt + 1
        if cnt == 4:
            features = calculate_statistic_features(flows[0], flows[1], flows[2])
            # res = max_min_transform(feature)
            for i in features:
                features_file_test.write(str(i) + ',')
            features_file_test.write(flows[3] + '\n')
            flows = []
            cnt = 0
    file_obj.close()
    features_file_test.close()

    # 归一化统计量
    with open('tmp/features-train.csv', 'rb') as file_obj:  # 读取训练集统计量
        train_set = []
        train_label = []
        csv_reader = csv.reader(file_obj)
        for exampler in csv_reader:
            train_set.append(exampler[:-1])
            train_label.append(exampler[-1])
    with open('tmp/features-test.csv', 'rb') as file_obj:  # 读取测试集统计量
        test_set = []
        test_label = []
        csv_reader = csv.reader(file_obj)
        for exampler in csv_reader:
            test_set.append(exampler[:-1])
            test_label.append(exampler[-1])

    # Standardization: zero mean and unit variance
    # scaler = preprocessing.StandardScaler().fit(np.array(train_set, dtype=float))  # 实例化一个缩放器，让其拟合训练集数据
    scaler = preprocessing.MinMaxScaler().fit(np.array(train_set, dtype=float))
    train_set_scaled = scaler.transform(train_set)
    train_set_scaled = train_set_scaled.tolist()
    test_set_scaled = scaler.transform(test_set)
    test_set_scaled = test_set_scaled.tolist()

    with open('tmp/scaled-features-train.csv', 'wb') as file_obj:
        csv_writer = csv.writer(file_obj)
        for i, feature in enumerate(train_set_scaled):
            csv_writer.writerow(feature + [train_label[i]])
    with open('tmp/scaled-features-test.csv', 'wb') as file_obj:
        csv_writer = csv.writer(file_obj)
        for i, feature in enumerate(test_set_scaled):
            csv_writer.writerow(feature + [test_label[i]])


def main():
    print 'Starting to calculate statistic features for train and test set...'
    statistic_features()
    print 'Calculating finished.'


if __name__ == '__main__':
    main()
