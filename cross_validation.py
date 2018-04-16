# -*- coding: utf-8 -*-

import partition_data_set
import extract_packet_length
import calculate_statistic_features
import train_and_test
import calculate_recall_precision_accuracy
import os
import shutil
import re
import datetime


def main():
    path_root = raw_input('Enter the root path of your data: ')
    if '' == path_root:
        path_root = 'C:/ScriptData/RandForest'
    elif path_root.find('\\') != -1:  # 转换路径格式
        path_root = path_root.replace('\\', '/')

    path_average_result = path_root + '/result'  # 存放最终结果的文件夹
    path_tmp = path_root + '/tmp'
    path_rec_pre_acc = path_root + '/tmp/recall_precision_accuracy.csv'
    path_time_cost = path_root + '/tmp/time_cost.csv'

    start = datetime.datetime.now()
    print 'Start: ' + start.strftime('%Y-%m-%d, %H:%M:%S.%f')

    # 先清除之前的数据
    if os.path.exists(path_tmp):
        shutil.rmtree(path_tmp)

    k = 1  # 进行5次交叉验证
    n = 5  # 5-折
    n_instance = 30  # 每个网页的示例数
    for i in range(1, k + 1):
        partition_data_set.partition_data_set(path_root=path_root, n_instance=n_instance, k=i, n=n)
        for j in range(1, n + 1):
            extract_packet_length.extract_length_feature(path_root=path_root, k=i, partition_num=j)
            calculate_statistic_features.statistic_features(path_root=path_root)
            classifier = train_and_test.train_model(path_root=path_root)
            train_and_test.test_model(path_root=path_root, classifier=classifier)
            calculate_recall_precision_accuracy.calculate_recall_precision_accuracy(path_root=path_root)

    # 创建存放最终结果的文件夹
    if not os.path.exists(path_average_result):
        os.mkdir(path_average_result)

    # 计算平均准确率
    with open(path_rec_pre_acc) as file_accuracy:
        lines = [line for line in file_accuracy if re.search('accuracy', line)]  # 筛选出所有记录accuracy的行
    accuracies = [float(item.split(',')[6]) for item in lines]  # 筛选出所有的accuracy值
    sum_accuracies = 0.0
    for accuracy in accuracies:
        sum_accuracies += accuracy
    average_accuracy = sum_accuracies / len(accuracies)

    with open(path_average_result + '/average_accuracy.csv', 'a') as file_average_accuracy:  # 将accuracy均值写入文件
        file_average_accuracy.write(str(average_accuracy) + '\n')

    # 计算平均训练时间和测试时间
    with open(path_time_cost) as file_time_cost:
        lines_all = file_time_cost.readlines()
        # print lines_all
        lines_train = [line[:-1] for line in lines_all if line.startswith('Train')]
        lines_test = [line[:-1] for line in lines_all if line.startswith('Test')]

    time_costs_train = [line.split(',')[-1] for line in lines_train]
    sum_time_costs_train = 0.0
    for cost_train in time_costs_train:
        sum_time_costs_train += float(cost_train)
    average_time_cost_train = sum_time_costs_train / len(time_costs_train)

    time_costs_test = [line.split(',')[-1] for line in lines_test]
    sum_time_costs_test = 0.0
    for cost_test in time_costs_test:
        sum_time_costs_test += float(cost_test)
    average_time_cost_test = sum_time_costs_test / len(time_costs_test)

    with open(path_average_result + '/average_time_cost.csv', 'a') as file_average_time_cost:
        file_average_time_cost.write(str(average_time_cost_train))
        file_average_time_cost.write(',')
        file_average_time_cost.write(str(average_time_cost_test))
        file_average_time_cost.write('\n')

    # # 清除临时数据
    # if os.path.exists(path_tmp):
    #     os.removedirs(path_tmp)

    end = datetime.datetime.now()
    print 'End: ' + end.strftime('%Y-%m-%d, %H:%M:%S.%f')
    print 'Time duration: ' + str(end - start)


if __name__ == '__main__':
    main()
