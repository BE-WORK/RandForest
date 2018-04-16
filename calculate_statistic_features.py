# coding: utf-8

import csv
import numpy as np
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


def statistic_features(path_root):
    """
    此函数分别为训练集和测试集计算所有流量文件的统计量。
    :param path_root:
    :return: none
    """
    path_train = path_root + '/tmp/train.csv'
    path_train_features = path_root + '/tmp/train_features.csv'
    path_test = path_root + '/tmp/test.csv'
    path_test_features = path_root + '/tmp/test_features.csv'
    path_train_features_scaled = path_root + '/tmp/train_features_scaled.csv'
    path_test_features_scaled = path_root + '/tmp/test_features_scaled.csv'

    # 处理训练集
    train_set = []
    train_label = []
    with open(path_train, 'rb') as file_obj:
        csv_reader = csv.reader(file_obj)
        cnt = 0  # 文件中每4行代表一个网页
        flows = []
        for order in csv_reader:
            if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
                order.pop()
            flows.append(''.join(order[:]))
            cnt = cnt + 1
            if cnt == 4:  # 一个网页的完整数据已读入
                features = calculate_statistic_features(flows[0], flows[1], flows[2])
                train_set.append(features)
                train_label.append(flows[3])
                flows = []
                cnt = 0

    # 处理测试集
    test_set = []
    test_label = []
    with open(path_test, 'rb') as file_obj:
        csv_reader = csv.reader(file_obj)
        cnt = 0  # 文件中每4行代表一个网页
        flows = []
        for order in csv_reader:
            if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
                order.pop()
            flows.append(''.join(order[:]))
            cnt = cnt + 1
            if cnt == 4:
                features = calculate_statistic_features(flows[0], flows[1], flows[2])
                test_set.append(features)
                test_label.append(flows[3])
                flows = []
                cnt = 0

    # 标准化之前写入文件
    with open(path_train_features, 'wb') as train_features_file:
        csv_writer = csv.writer(train_features_file)
        for i, train_features in enumerate(train_set):
            csv_writer.writerow(train_features + [train_label[i]])

    with open(path_test_features, 'wb')as test_features_file:
        csv_writer = csv.writer(test_features_file)
        for i, test_features in enumerate(test_set):
            csv_writer.writerow(test_features + [test_label[i]])

    # 标准化
    scaler = preprocessing.MinMaxScaler()
    train_set_scaled = scaler.fit_transform(np.array(train_set, dtype=float)).tolist()
    test_set_scaled = scaler.transform(test_set).tolist()

    # 标准化之后写入文件
    with open(path_train_features_scaled, 'wb') as file_obj:
        csv_writer = csv.writer(file_obj)
        for i, feature in enumerate(train_set_scaled):
            csv_writer.writerow(feature + [train_label[i]])
    with open(path_test_features_scaled, 'wb') as file_obj:
        csv_writer = csv.writer(file_obj)
        for i, feature in enumerate(test_set_scaled):
            csv_writer.writerow(feature + [test_label[i]])


def main():
    path = raw_input('Enter the root path of your data: ')
    if '' == path:
        path = 'C:/ScriptData/RandForest'
    elif path.find('\\') != -1:  # 转换路径格式
        path = path.replace('\\', '/')
    print 'Starting to calculate statistic features for train and test set...'
    statistic_features(path_root=path)
    print 'Calculating finished.'


if __name__ == '__main__':
    main()
