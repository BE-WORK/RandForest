# -*- coding: utf-8 -*-

import csv


def calculate_recall_precision_accuracy():
    """
    此函数统计最终的分类结果。
    :return: none
    """
    num_true_positive = {}  # 记录每个网页的真阳例数目
    num_test_sample = {}  # 记录每个网页真实存在的样本数
    num_prediction = {}  # 记录所有分类为当前网页的样本数

    page_true_positive_ratio = {}  # 每个网页的真阳率，等同于召回率
    page_false_positive_ratio = {}
    weight = {}  # 每个网页的样本数占整个测试集样本数的比重

    total_true_positive = 0  # 所有的真阳例数目
    total_sample = 0  # 测试集上的总样本数

    csv_read_file = file('tmp/result.csv', 'rb')
    csv_write_file = file('tmp/recall_precision_accuracy.csv', 'ab')
    column_name = ['page_name',
                   'page_sample',
                   'page_prediction',
                   'page_truth',
                   'page_TPR',
                   'page_FPR',
                   'precision',
                   'recall',
                   'page_weight']
    writer = csv.DictWriter(csv_write_file, delimiter=',', fieldnames=column_name)
    writer.writerow(
        {'page_name': 'page name',
         'page_sample': 'sample',
         'page_prediction': 'prediction',
         'page_truth': 'truth',
         'page_TPR': 'page TPR',
         'page_FPR': 'page FPR',
         'precision': 'precision',
         'recall': 'recall',
         'page_weight': 'weight'})
    csv_reader = csv.reader(csv_read_file, delimiter=',')
    for true_page_name, classify_result in csv_reader:
        if true_page_name not in num_test_sample:
            num_test_sample[true_page_name] = 0
            num_true_positive[true_page_name] = 0

        if true_page_name not in num_prediction:
            num_prediction[true_page_name] = 0

        if classify_result not in num_prediction:
            num_prediction[classify_result] = 0

        if true_page_name == classify_result:  # 真阳例
            num_true_positive[true_page_name] = num_true_positive[true_page_name] + 1
            total_true_positive = total_true_positive + 1

        num_test_sample[true_page_name] = num_test_sample[true_page_name] + 1
        num_prediction[classify_result] = num_prediction[classify_result] + 1
        total_sample = total_sample + 1
    csv_read_file.close()

    accuracy = total_true_positive * 1.0 / total_sample

    for key in num_test_sample:
        page_true_positive_ratio[key] = 1.0 * num_true_positive[key] / num_test_sample[
            key]  # 计算真阳率：被预测为正的正样本数/正样本实际数（TPR=TP/TP+FN）
        try:
            page_precision = 1.0 * num_true_positive[key] / num_prediction[key]
        except Exception, e:
            page_precision = 0
            print Exception, ':', e, key, num_prediction[key]
        page_recall = 1.0 * num_true_positive[key] / num_test_sample[key]

        page_false_positive_ratio[key] = 1.0 * (num_prediction[key] - num_true_positive[key]) / (
                total_sample - num_test_sample[key])  # 计算假阳率：被预测为正的负样本数/负样本实际数（FPR=FP/FP+TN）
        weight[key] = 1.0 * num_test_sample[key] / total_sample
        writer.writerow(
            {'page_name': key,
             'page_sample': num_test_sample[key],
             'page_prediction': num_prediction[key],
             'page_truth': num_true_positive[key],
             'page_TPR': page_true_positive_ratio[key],
             'page_FPR': page_false_positive_ratio[key],
             'precision': page_precision,
             'recall': page_recall,
             'page_weight': weight[key]})
    writer.writerow({'page_name': 'accuracy',
                     'precision': accuracy})
    writer.writerow({})


def main():
    calculate_recall_precision_accuracy()


if __name__ == '__main__':
    main()
