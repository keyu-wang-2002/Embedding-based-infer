# -*- coding: utf-8 -*-
# @author： Shiqi Zhou
# @date： 2022 - 03 - 04
# 合并两个文档，测试版本

oriPath1 = "./oriData/oriTest1.tsv"  # 原始文件1路径
oriPath2 = "./oriData/oriTest2.tsv"  # 原始文件2路径
mergePath = "./oriData/merge.tsv"  # 合并后文件路径
# 读入数据集文件位置
file1 = open(oriPath1, 'r', encoding='utf-8')
file2 = open(oriPath2, 'r', encoding='utf-8')
file3 = open(mergePath, 'w+', encoding='utf-8')

lines = len(file1.readlines())
print('原来的1的数量：' + str(lines))
lines = len(file2.readlines())
print('原来的2的数量：' + str(lines))

file1.seek(0)  # 指针回到文件开头
file2.seek(0)  # 指针回到文件开头

f1 = file1.read()
file3.write(f1)
file3.write('\n')
f2 = file2.read()
file3.write(f2)

file3.seek(0)  # 指针回到文件开头
lines = len(file3.readlines())
print('合并后的数量：' + str(lines))


# with open(mergePath, "w+", encoding="utf-8") as mergeFile, open(oriPath1, mode="r", encoding="utf-8") as file1, open(oriPath2, mode="r", encoding="utf-8") as file2:
#
#     lines = len(file2.readlines())
#     print('原来的2的数量：' + str(lines))
#     for line in file1:
#         print("进入第一个for循环")
#         print(line)
#         mergeFile.write(line)
#     for line in file2:
#         print("进入第二个for循环")
#         print(line)
#         mergeFile.write(line)
#     # lines = len(mergeFile.readlines())
#     # print('合并后的数量：' + str(lines))


# with open(mergePath, mode="w+", encoding="utf-8") as mergeFile:
#     with open(oriPath1, mode="r", encoding="utf-8") as file1:
#         lines = len(file1.readlines())
#         print('原来的1的数量：' + str(lines))
#         for line in file1:
#             print(line)
#             mergeFile.write(line)
#     with open(oriPath2, mode="r", encoding="utf-8") as file2:
#         lines = len(file2.readlines())
#         print('原来的2的数量：' + str(lines))
#         for line in file2:
#             print(line)
#             mergeFile.write(line)
#     lines = len(mergeFile.readlines())
#     print('合并后的数量：' + str(lines))

file1.close()
file2.close()
file3.close()