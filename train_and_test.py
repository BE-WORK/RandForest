# -*- coding: utf-8 -*-

import csv
import datetime
from sklearn.ensemble import RandomForestClassifier


def train_model():
    """
    此函数加载此前计算出的统计特征量，训练随机森林分类器。
    :return: 返回训练好的分类器。
    """
    # 加载训练数据
    csv_read_file = file('features-train.csv', 'rb')
    csv_reader = csv.reader(csv_read_file)
    train_matrix = []
    train_label = []
    for line in csv_reader:
        train_data = map(float, line[:-1])
        train_matrix.append(train_data)
        train_label.append(line[-1])
    csv_read_file.close()

    # 训练模型
    start_train = datetime.datetime.now()
    clf = RandomForestClassifier()  # criterion='gini',max_features='sqrt',n_estimators=3
    clf.fit(train_matrix, train_label)
    end_train = datetime.datetime.now()
    output_train_cost = file('time-cost.txt', 'a')
    output_train_cost.write('Train time duration: ' + str(end_train - start_train) + '\n')
    output_train_cost.close()

    return clf


def test_model(classifier):
    """
    此函数测试训练好的分类器。
    :param classifier:训练阶段得到的分类器。
    :return:none
    """
    # 加载测试数据
    csv_read_file = file('features-test.csv', 'rb')
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

    csv_write_file = file('result.csv', 'wb')
    fieldnames = ['trueResult', 'identifyResult']
    writer = csv.DictWriter(csv_write_file, delimiter='\t', fieldnames=fieldnames)
    for i in range(len(res)):
        writer.writerow({'trueResult': test_label[i], 'identifyResult': res[i]})
    csv_write_file.close()
    output_test_test = file('time-cost.txt', 'a')
    output_test_test.write('Test time duration: ' + str(end_test - start_test) + '\n')
    output_test_test.close()


def main():
    classifier = train_model()
    test_model(classifier)


if __name__ == '__main__':
    main()
