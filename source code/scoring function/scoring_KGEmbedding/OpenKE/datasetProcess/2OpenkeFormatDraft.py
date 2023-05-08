# -*- coding: utf-8 -*-
# author： Shiqi Zhou
# @date： 2022 - 03 - 03
# 将自己想要的数据集格式转换为openKE数据集格式，测试版本

# 读入原始数据集文件
oriPath = "./oriData/oriTest.tsv"   # 原始文件路径
# fOri = open(oriPath,'r',encoding = 'utf-8')   # 打开文件

# 输出转换格式后数据集
newPath = "./newData/test.txt"   # train文件路径
en2id = "./newData/en2id.txt"   # 保存实体对应的id的文件路径
re2id = "./newData/re2id.txt"   # 保存关系对应的id的文件路径

# List分别存储实体、关系、三元组
ListEntity = []
ListRel = []
ListTri = []

#读取文件内容
# print(fOri.read())   # 测试，输出信息是否正确
with open(oriPath, 'r', encoding='utf-8') as fOri:
    for line in fOri:
        # 读取一行后，末尾一般会有一个\n，所以用strip函数去掉
        line = line.strip('\n').split('\t')
        # 实体
        if line[0] not in ListEntity:
            ListEntity.append(line[0])
        if line[2] not in ListEntity:
            ListEntity.append(line[2])
        # 关系
        if line[1] not in ListRel:
            ListRel.append(line[1])
        ListTri.append(((ListEntity.index(line[0])), (ListEntity.index(line[2])), ListRel.index(line[1])))
        # # 测试用
        # print(ListEntity.index(line[0]))
        # print(line[0])
        # # 测试，看拆分子项分别为什么
        # print(line[0])
        # print(line[1])
        # print(line[2])


# 输出转换格式后数据集
with open(en2id, 'w+', encoding='utf-8') as fEn2id:
    fEn2id.write(str(len(ListEntity)) + '\n')
    for i in iter(ListEntity):
        fEn2id.write(i + '\t' + str(ListEntity.index(i)) + '\n')
with open(re2id, 'w+', encoding='utf-8') as fRe2id:
    fRe2id.write(str(len(ListRel)) + '\n')
    for i in iter(ListRel):
        fRe2id.write(i + '\t' + str(ListRel.index(i)) + '\n')

# 删除重复元素
ListTri = list(set(ListTri))

# 输出新文件
with open(newPath, 'w+', encoding='utf-8') as newfile:
    # 输出列表长度
    newfile.write(str(len(ListTri)) + '\n')
    for i in iter(ListTri):
        text = str(i).strip('(')
        text = str(text).strip(')')
        newfile.write(text.replace(', ', '\t') + '\n')