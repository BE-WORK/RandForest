# -*- coding: utf-8 -*-

import partition_data_set
import select_test_set
import extract_packet_length
import calculate_statistic_features
import train_and_test
import calculate_recall_precision_accuracy
import os
import shutil


def main():
    # 先清除之前的数据
    if os.path.exists(r'time-cost.txt'):
        os.remove(r'time-cost.txt')
    if os.path.exists(r'recall_precision_accuracy.csv'):
        os.remove(r'recall_precision_accuracy.csv')
    if os.path.exists(r'tmp'):
        shutil.rmtree(r'tmp')

    k = 5  # 进行5次交叉验证
    n = 5  # 5-折
    for i in range(1, k + 1):
        partition_data_set.partition_data_set(i, n)
        for j in range(1, n + 1):
            select_test_set.select_test_set(i, j)
            extract_packet_length.extract_length_feature()
            calculate_statistic_features.statistic_features()
            classifier = train_and_test.train_model()
            train_and_test.test_model(classifier)
            calculate_recall_precision_accuracy.calculate_recall_precision_accuracy()

    # 清除临时数据
    # if os.path.exists(r'tmp'):
    #     os.removedirs(r'tmp')


if __name__ == '__main__':
    main()
