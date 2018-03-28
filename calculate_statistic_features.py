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


def max_min_transform(features):
    """
    此函数将传入的统计量列表中的数据归一化至（0，1）范围内。
    :param features: 统计量列表。
    :return: none
    """
    features = np.array(features).reshape(-1, 1)
    np.nan_to_num(features)  # 转换NaN类型为0，无穷大为最大数（最小数）
    # print features
    min_max_scaler = preprocessing.MinMaxScaler()
    feature_minmax = min_max_scaler.fit_transform(features)  # 将特征值映射到范围(0,1)上
    np.nan_to_num(feature_minmax)  # transform nan
    return np.array(feature_minmax).reshape(1, -1)


def statistic_features():
    """
    此函数分别为训练集和测试集计算所有流量文件的统计量。
    :return: none
    """
    # 处理训练集
    file_obj = file("train.csv", 'rb')
    csv_reader = csv.reader(file_obj)
    features_file_train = file("features-train.csv", 'w')
    cnt = 0  # 文件中每4行代表一个网页
    flows = []
    for order in csv_reader:
        if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
            order.pop()
        flows.append(''.join(order[:]))
        cnt = cnt + 1
        if cnt == 4:  # 一个网页的完整数据已读入
            feature = calculate_statistic_features(flows[0], flows[1], flows[2])
            res = max_min_transform(feature)
            for i in res[0]:
                features_file_train.write(str(i) + ',')
            features_file_train.write(flows[3] + '\n')
            flows = []
            cnt = 0
    file_obj.close()
    features_file_train.close()

    # 处理测试集
    file_obj = file("test.csv", 'rb')
    csv_reader = csv.reader(file_obj)
    features_file_test = file("features-test.csv", 'w')
    cnt = 0  # 文件中每4行代表一个网页
    flows = []
    for order in csv_reader:
        if order[-1] == '':  # 由于之前写入数据的方式原因，需要检验最后一列是否为空
            order.pop()
        flows.append(''.join(order[:]))
        cnt = cnt + 1
        if cnt == 4:
            feature = calculate_statistic_features(flows[0], flows[1], flows[2])
            res = max_min_transform(feature)
            for i in res[0]:
                features_file_test.write(str(i) + ',')
            features_file_test.write(flows[3] + '\n')
            flows = []
            cnt = 0
    file_obj.close()
    features_file_test.close()


def main():
    print 'Starting to calculate statistic features for train and test set...'
    statistic_features()
    print 'Calculating finished.'


if __name__ == "__main__":
    main()
