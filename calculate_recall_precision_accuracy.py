# -*- coding: utf-8 -*-

import csv


def calculate_recall_precision_accuracy():
    """
    此函数统计最终的分类结果。
    :return: none
    """
    page_true_positive = {}  # 记录每个网页的真阳例数目
    page_true = {}  # 记录每个网页真实存在的样本数
    page_all = {}  # 记录所有分类为当前网页的样本数

    page_true_positive_ratio = {}  # 每个网页的真阳率，等同于召回率
    page_false_positive_ratio = {}
    weight = {}  # 每个网页的样本数占整个测试集样本数的比重

    total_true_positive = 0  # 所有的真阳例数目
    total_sample = 0  # 测试集上的总样本数

    csv_read_file = file('tmp/result.csv', 'rb')
    csv_write_file = file('tmp/recall_precision_accuracy.csv', 'ab')
    column_name = ['page name', 'page TPR', 'page FPR', 'precision', 'recall', 'weight']
    writer = csv.DictWriter(csv_write_file, delimiter=',', fieldnames=column_name)
    writer.writerow({'page name': 'page name', 'page TPR': 'page TPR',
                     'page FPR': 'page FPR', 'precision': 'precision', 'recall': 'recall',
                     'weight': 'weight'})
    csv_reader = csv.reader(csv_read_file, delimiter=',')
    for true_page_name, classify_result in csv_reader:
        if true_page_name not in page_true:
            page_true[true_page_name] = 0
            page_true_positive[true_page_name] = 0

        if true_page_name not in page_all:
            page_all[true_page_name] = 0

        if classify_result not in page_all:
            page_all[classify_result] = 0

        if true_page_name == classify_result:  # 真阳例
            page_true_positive[true_page_name] = page_true_positive[true_page_name] + 1
            total_true_positive = total_true_positive + 1

        page_true[true_page_name] = page_true[true_page_name] + 1
        page_all[classify_result] = page_all[classify_result] + 1
        total_sample = total_sample + 1
    csv_read_file.close()

    accuracy = total_true_positive * 1.0 / total_sample

    for key in page_true:
        page_true_positive_ratio[key] = 1.0 * page_true_positive[key] / page_true[key]  # 计算真阳率：被预测为正的正样本数/正样本实际数
        try:
            page_precision = 1.0 * page_true_positive[key] / page_all[key]
        except Exception, e:
            page_precision = 0
            print Exception, ':', e, key, page_all[key]
        page_recall = 1.0 * page_true_positive[key] / page_true[key]
        page_false_positive_ratio[key] = 1.0 * (page_all[key] - page_true_positive[key]) / page_true[
            key]  # 计算假阳率：被预测为正的负样本数/负样本实际数
        weight[key] = 1.0 * page_true[key] / total_sample
        writer.writerow(
            {'page name': key, 'page TPR': page_true_positive_ratio[key],
             'page FPR': page_false_positive_ratio[key], 'precision': page_precision, 'recall': page_recall,
             'weight': weight[key]})
    writer.writerow({'page name': 'accuracy', 'precision': accuracy})
    writer.writerow({})


def main():
    calculate_recall_precision_accuracy()


if __name__ == '__main__':
    main()
