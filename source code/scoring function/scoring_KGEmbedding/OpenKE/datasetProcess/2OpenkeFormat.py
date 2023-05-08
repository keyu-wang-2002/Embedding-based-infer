# -*- coding: utf-8 -*-
# @author： Shiqi Zhou
# @date： 2022 - 03 - 04
# 将自己想要的数据集格式转换为openKE数据集格式
import random

# 读入原始数据集文件
oriPath = "./tsvData/Bio.tsv"  # 原始文件路径
# oriPath = "./oriData/yago15k.tsv"  # yago15k文件路径
# oriPath = "./oriData/yago60k.tsv"  # yago60k文件路径
# 输出转换格式后数据集
en2id = "./newData/Bio/entity2id.txt"  # 保存实体对应的id的文件路径
re2id = "./newData/Bio/relation2id.txt"  # 保存关系对应的id的文件路径
train2id = "./newData/Bio/train2id.txt"  # train2id文件路径
test2id = "./newData/Bio/test2id.txt"  # test2id文件路径
valid2id = "./newData/Bio/valid2id.txt"  # valid2id文件路径

# List分别存储实体、关系、三元组
ListEntity = []
ListRel = []
ListTri = []

# 读取文件内容
with open(oriPath, 'r', encoding='utf-8') as fOri:
    for line in fOri:
        # 读取一行后，末尾会有一个\n，用strip函数去掉
        line = line.strip('\n').split('\t')
        # 实体
        if line[0] not in ListEntity:
            ListEntity.append(line[0])
        if line[2] not in ListEntity:
            ListEntity.append(line[2])
        # 关系
        if line[1] not in ListRel:
            ListRel.append(line[1])
        # ！这里有一个问题，没有检查三元组是否重复
        ListTri.append(((ListEntity.index(line[0])), (ListEntity.index(line[2])), ListRel.index(line[1])))

# 输出转换格式后数据集
with open(en2id, 'w+', encoding='utf-8') as fEn2id:
    fEn2id.write(str(len(ListEntity)) + '\n')
    for i in iter(ListEntity):
        fEn2id.write(i + '\t' + str(ListEntity.index(i)) + '\n')
with open(re2id, 'w+', encoding='utf-8') as fRe2id:
    fRe2id.write(str(len(ListRel)) + '\n')
    for i in iter(ListRel):
        fRe2id.write(i + '\t' + str(ListRel.index(i)) + '\n')


def data_split(full_list, train_ratio, valid_ratio, shuffle):
    """
    :param full_list: 待拆分的列表
    :param train_ratio: 训练集比例
    :param valid_ratio: 验证集比例，剩下的为测试集
    :param shuffle: 是否需要打乱原来的列表顺序，true打乱
    :return: 按比例拆分好的子数据集sublist_train、sublist_valid、sublist_test
    """
    n_total = len(full_list)
    offset1 = int(n_total * train_ratio)
    offset2 = int(n_total * (train_ratio + valid_ratio))
    # 错误返回
    if n_total == 0 or offset1 < 1 or n_total == 0 or offset2 < 1:
        print("error")
        return [], [], full_list
    # 需要打乱原列表
    if shuffle:
        random.shuffle(full_list)
    sl_train = full_list[:offset1]
    sl_valid = full_list[offset1:offset2]
    sl_test = full_list[offset2:]
    return sl_train, sl_valid, sl_test


# 删除三元组中重复的三元组
ListTri = list(set(ListTri))
# 调用拆分函数
sublist_train, sublist_valid, sublist_test = data_split(full_list=ListTri, train_ratio=0.8, valid_ratio=0.1,
                                                        shuffle=True)
# 输出train2id文件
with open(train2id, 'w+', encoding='utf-8') as f_train2id:
    f_train2id.write(str(len(sublist_train)) + '\n')
    for i in iter(sublist_train):
        text = str(i).strip('(')
        text = str(text).strip(')')
        f_train2id.write(text.replace(', ', '\t') + '\n')
# 输出valid2id文件
with open(valid2id, 'w+', encoding='utf-8') as f_valid2id:
    f_valid2id.write(str(len(sublist_valid)) + '\n')
    for i in iter(sublist_valid):
        text = str(i).strip('(')
        text = str(text).strip(')')
        f_valid2id.write(text.replace(', ', '\t') + '\n')
# 输出test2id文件
with open(test2id, 'w+', encoding='utf-8') as f_test2id:
    f_test2id.write(str(len(sublist_test)) + '\n')
    for i in iter(sublist_test):
        text = str(i).strip('(')
        text = str(text).strip(')')
        # 特别注意这里的都好后面要加一个空格！！！
        f_test2id.write(text.replace(', ', '\t')+ '\n')
print("finish!")
