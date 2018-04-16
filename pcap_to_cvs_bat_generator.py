# -*- coding: utf-8 -*-

import os


def pcap_to_csv_bat_generator(path_root):
    """
    此函数为从pcap文件中提取部分字段至csv文件生成BAT脚本，同时提前创建好存放csv的目录树，此目录树和pcap数据相同。
    :param path_root: 数据集所在的根目录。
    :return: none
    """
    path_pcap = path_root + '/data_pcap'
    path_csv = path_root + '/data_csv'

    if not os.path.exists(path_csv):
        os.mkdir(path_csv)

    # 从pcap文件提取目标字段至csv文件，存放csv文件的目录树和存放pcap文件的相同
    with open(path_root + '/pcap_to_csv.bat', 'w') as bat_file:
        bat_file.write('@echo off')
        bat_file.write('\n')
        goods = os.listdir(path_pcap)
        for g in goods:  # 遍历一级目录
            if not os.path.exists(path_csv + '/' + g):
                os.mkdir(path_csv + '/' + g)
            pages = os.listdir(path_pcap + '/' + g + '/')
            for p in pages:  # 遍历二级目录
                if not os.path.exists(path_csv + '/' + g + '/' + p):
                    os.mkdir(path_csv + '/' + g + '/' + p)
                fetchs = os.listdir(path_pcap + '/' + g + '/' + p + '/')
                for f in fetchs:  # 遍历三级目录
                    bat_file.write(
                        'tshark -r data_pcap/' + g + '/' + p + '/' + f + ' -Y "tcp && ip" -T fields -e _ws.col.No. -e _ws.col.Time -e _ws.col.Source -e _ws.col.Destination -e _ws.col.Protocol -e _ws.col.Length -E header=n -E separator=, -E quote=d -E occurrence=f > data_csv/' + g + '/' + p + '/' + '-'.join(
                            f.split('.')[:-1]) + '.csv')
                    bat_file.write('\n')
                    # bat_file.write('pause')
                    # bat_file.write('\n')
        bat_file.write('echo finished!\n')
        bat_file.write('pause\n')


def main():
    path = raw_input('Enter the root path of your data: ')
    if '' == path:
        path = 'C:/ScriptData/RandForest'
    elif path.find('\\') != -1:  # 转换路径格式
        path = path.replace('\\', '/')
    pcap_to_csv_bat_generator(path_root=path)


if __name__ == '__main__':
    main()
