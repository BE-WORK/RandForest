# coding: utf-8

import csv
import numpy as np
from sklearn import preprocessing
from pandas import DataFrame


def calculate_statistic_features(incomes, outgoes, bidirections):
    """
    此函数计算单个流量文件的54个统计量。
    :param incomes: 存放目的地址为本机的数据包Length字段列表。
    :param outgoes: 存放源地址为本机的数据包Length字段列表。
    :param bidirections: 存放双向数据包Length字段列表。
    :return:none
    """
    incomes = incomes.split(' ')
    if len(incomes) == 1 or len(incomes) == 0:
        incomes = [0, 0, 0]
    if len(outgoes) == 1 or len(outgoes) == 0:
        outgoes = [0, 0, 0]
    if len(bidirections) == 1 or len(bidirections) == 0:
        bidirections = [0, 0, 0]
    incomes = map(int, incomes[:-1])  # 最后一个元素是空字符串:''
    df = DataFrame(incomes)
    percentiles = []  # list of percentiles
    minimum = df.min()  # minimum，返回的是Series类型
    maximum = df.max()  # maximum
    mean = df.mean()  # mean
    mad = df.mad()  # median absolute deviation
    std = df.std()  # standard deviation
    var = df.var()  # variance
    skew = df.skew()  # skew
    kurt = df.kurt()  # kurtosis
    if np.isnan(std[0]):
        std[0] = 0.0
    if np.isnan(var[0]):
        var[0] = 0.0
    if np.isnan(skew[0]):
        skew[0] = 0.0
    if np.isnan(kurt[0]):
        kurt[0] = 0.0
    for i in range(10, 100, 10):
        percentiles.append(np.percentile(incomes, i))
    result = [minimum[0], maximum[0], mean[0], mad[0], std[0], var[0], skew[0], kurt[0],
              len(incomes) + len(outgoes) + len(bidirections)] + percentiles
    del percentiles[:]

    outgoes = outgoes.split(' ')
    outgoes = map(int, outgoes[:-1])
    df = DataFrame(outgoes)
    percentiles = []  # list of percentiles
    minimum = df.min()  # minimum
    maximum = df.max()  # maximum
    mean = df.mean()  # mean
    mad = df.mad()  # median absolute deviation
    std = df.std()  # standard deviation
    var = df.var()  # variance
    skew = df.skew()  # skew
    kurt = df.kurt()  # kurtosis
    if np.isnan(std[0]):
        std[0] = 0.0
    if np.isnan(var[0]):
        var[0] = 0.0
    if np.isnan(skew[0]):
        skew[0] = 0.0
    if np.isnan(kurt[0]):
        kurt[0] = 0.0

    for i in range(10, 100, 10):
        percentiles.append(np.percentile(outgoes, i))
    result = result + [minimum[0], maximum[0], mean[0], mad[0], std[0], var[0], skew[0], kurt[0],
                       len(incomes) + len(outgoes) + len(bidirections)] + percentiles
    del percentiles[:]

    bidirections = bidirections.split(' ')
    bidirections = map(int, bidirections[:-1])
    df = DataFrame(bidirections)
    percentiles = []  # list of percentiles
    minimum = df.min()  # minimum
    maximum = df.max()  # maximum
    mean = df.mean()  # mean
    mad = df.mad()  # median absolute deviation
    std = df.std()  # standard deviation
    var = df.var()  # variance
    skew = df.skew()  # skew
    kurt = df.kurt()  # kurtosis
    if np.isnan(std[0]):
        std[0] = 0.0
    if np.isnan(var[0]):
        var[0] = 0.0
    if np.isnan(skew[0]):
        skew[0] = 0.0
    if np.isnan(kurt[0]):
        kurt[0] = 0.0
    for i in range(10, 100, 10):
        percentiles.append(np.percentile(bidirections, i))
    result = result + [minimum[0], maximum[0], mean[0], mad[0], std[0], var[0], skew[0], kurt[0],
                       len(incomes) + len(outgoes) + len(bidirections)] + percentiles
    del percentiles[:]
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
    test_set_scaled = scaler.transform(np.array(test_set, dtype=float)).tolist()

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
