# -*- coding: utf-8 -*-

import csv
import datetime
from sklearn.ensemble import RandomForestClassifier


def train_model(path_root):
    """
    此函数加载此前计算出的统计特征量，训练随机森林分类器。
    :param path_root: 数据集所在的根目录。
    :return: 返回训练好的分类器。
    """
    path_train = path_root + '/tmp/train_features_scaled.csv'
    path_time_cost = path_root + '/tmp/time_cost.csv'

    # 加载训练数据
    with open(path_train, 'rb')as csv_read_file:
        csv_reader = csv.reader(csv_read_file)
        train_matrix = []
        train_label = []
        for line in csv_reader:
            train_data = map(float, line[:-1])
            train_matrix.append(train_data)
            train_label.append(line[-1])

    # 训练模型
    start_train = datetime.datetime.now()
    clf = RandomForestClassifier()  # criterion='gini',max_features='sqrt',n_estimators=3
    clf.fit(train_matrix, train_label)
    end_train = datetime.datetime.now()
    print 'Train: ' + '{value:f}'.format(value=(end_train - start_train).total_seconds())

    with open(path_time_cost, 'a') as output_train_cost:
        output_train_cost.write(
            'Train' + ',' + '{value:f}'.format(value=(end_train - start_train).total_seconds()) + '\n')

    return clf


def test_model(path_root, classifier):
    """
    此函数测试训练好的分类器。
    :param path_root: 数据集所在的根目录。
    :param classifier:训练阶段得到的分类器。
    :return:none
    """
    path_test = path_root + '/tmp/test_features_scaled.csv'
    path_time_cost = path_root + '/tmp/time_cost.csv'
    path_result = path_root + '/tmp/result.csv'

    # 加载测试数据
    csv_read_file = file(path_test, 'rb')
    csv_reader = csv.reader(csv_read_file)
    test_matrix = []
    test_label = []
    for line in csv_reader:
        test_data = map(float, line[:-1])
        test_matrix.append(test_data)
        test_label.append(line[-1])
    csv_read_file.close()

    # 分类
    start_test = datetime.datetime.now()
    res = classifier.predict(test_matrix)
    end_test = datetime.datetime.now()

    with open(path_result, 'wb') as csv_write_file:
        fieldnames = ['trueResult', 'identifyResult']
        writer = csv.DictWriter(csv_write_file, delimiter=',', fieldnames=fieldnames)
        for i in range(len(res)):
            writer.writerow({'trueResult': test_label[i], 'identifyResult': res[i]})

    with open(path_time_cost, 'a') as output_test_cost:
        print 'Test: ' + '{value:f}'.format(value=(end_test - start_test).total_seconds() / len(test_label))
        output_test_cost.write(
            'Test' + ',' + '{value:f}'.format(value=(end_test - start_test).total_seconds() / len(test_label)) + '\n')


def main():
    path = raw_input('Enter the root path of your data: ')
    if '' == path:
        path = 'C:/ScriptData/RandForest'
    elif path.find('\\') != -1:  # 转换路径格式
        path = path.replace('\\', '/')
    classifier = train_model(path_root=path)
    test_model(path_root=path, classifier=classifier)


if __name__ == '__main__':
    main()
