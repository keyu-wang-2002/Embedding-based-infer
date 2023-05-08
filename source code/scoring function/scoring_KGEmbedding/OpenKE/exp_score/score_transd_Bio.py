import json
import re
import numpy as np


entity_file_name = "./datasetProcess/newData/Bio/entity2id.txt"
entity_list = []
with open(entity_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n').split("\t")
        entity_list.append(line[0])
    entity_list = entity_list[1:]


relation_file_name = "./datasetProcess/newData/Bio/relation2id.txt"
relation_list = []
with open(relation_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n').split("\t")
        relation_list.append(line[0])
    relation_list = relation_list[1:]


with open('./embed/transd_Bio_embed.vec','r',encoding='utf8') as fp:
    json_data = json.load(fp)

ent2embed_dict = {}
for idx, entity in enumerate(entity_list):
    ent2embed_dict[entity] = json_data['ent_embeddings.weight'][idx]

rel2embed_dict = {}
for idx, relation in enumerate(relation_list):
    rel2embed_dict[relation] = json_data['rel_embeddings.weight'][idx]



BioAxioms_file_name = "./datasetProcess/oriData/BioallAxioms.txt"
BioAxioms_list = []
with open(BioAxioms_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n')
        BioAxioms_list.append(line)

axiom2embedd_dict = {}
for axiom in BioAxioms_list:
    axiom_vec = [[0.0]*200, [0.0]*200, [0.0]*200]
    for entity in entity_list:
        if re.match(entity, axiom):
            axiom_vec[0] = ent2embed_dict[entity]
        elif re.search(entity, axiom):
            axiom_vec[2] = ent2embed_dict[entity]
        else:
            continue
    for relation in relation_list:
        if re.search(relation, axiom):
            axiom_vec[1] = rel2embed_dict[relation]
    axiom2embedd_dict[axiom] = np.array(axiom_vec).reshape(-1)


# ===================================================================================
# ===================================================================================
# ===================================================================================
Kset = set()
with open("./BioMCS/MCS1") as f:
    Kt = f.read().split("\n\n")
    K1 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K1.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS2") as f:
    Kt = f.read().split("\n\n")
    K2 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K2.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS3") as f:
    Kt = f.read().split("\n\n")
    K3 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K3.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS4") as f:
    Kt = f.read().split("\n\n")
    K4 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K4.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS5") as f:
    Kt = f.read().split("\n\n")
    K5 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K5.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS6") as f:
    Kt = f.read().split("\n\n")
    K6 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K6.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS7") as f:
    Kt = f.read().split("\n\n")
    K7 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K7.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS8") as f:
    Kt = f.read().split("\n\n")
    K8 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K8.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS9") as f:
    Kt = f.read().split("\n\n")
    K9 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K9.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS10") as f:
    Kt = f.read().split("\n\n")
    K10 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K10.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS11") as f:
    Kt = f.read().split("\n\n")
    K11 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K11.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS12") as f:
    Kt = f.read().split("\n\n")
    K12 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K12.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS13") as f:
    Kt = f.read().split("\n\n")
    K13 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K13.append(axiom)
        Kset.add(axiom)
    f.close()
with open("./BioMCS/MCS14") as f:
    Kt = f.read().split("\n\n")
    K14 = []
    for axiom in Kt:
        axiom = axiom.strip("\n")
        K14.append(axiom)
        Kset.add(axiom)
    f.close()

K = list(Kset)
mc_K = [K1,K2,K3,K4,K5,K6,K7,K8,K9,K10,K11,K12,K13,K14]
print("data loaded!")

# import time
# start1 = time.time()

mat = [([0] * len(K)) for i in range(len(K))]
sent_index = {}
index_sent = {}
index = 0
embeds = []
for sentence in K:
    sentence = sentence.strip("\n")
    sent_index[sentence] = index
    index_sent[index] = sentence
    index += 1
    embeds.append(axiom2embedd_dict[sentence])


def cos_sim(v1, v2):
    cos_dist = sum(v1 * v2) / ((sum(v1**2)**0.5) * (sum(v2**2)**0.5))  
    return (1 + cos_dist) / 2

def euc_sim(v1, v2):
    euc_dist = sum((v1 - v2) ** 2) ** 0.5
    return 1 / (1 + euc_dist)


for i in range(len(K)):
    for j in range(i, len(K)):
        mat[i][j] = cos_sim(embeds[i], embeds[j])

for i in range(len(K)):
    for j in range(i):
        mat[i][j] = mat[j][i]

# end1 = time.time()
# print("cosine similarity calculation time: {0}".format(end1-start1))

print("Cosine Similarity ")
######################### Method 1 ###################################

def agg_all(Ki, alpha):
    res = 0
    for beta in Ki:
        res += mat[sent_index[beta]][sent_index[alpha]]
    return res / len(Ki)

def mc_all(alpha):
    return sum([(agg_all(Ki, alpha)) for Ki in mc_K])

def score_all(Ki):
    res = 0
    for alpha in Ki:
        mc = mc_all(alpha)
        res += mc
    return res


# start2 = time.time()
cnt = 1
for Ki in mc_K:
    print("Method 1 K{0}  score: {1}".format(cnt, score_all(Ki)))
    cnt += 1
# end2 = time.time()
# print("Cos M1 time:  {0}".format(end2-start2))

######################### Method 2 ###################################

def equalHead(alpha, beta):
    if len(alpha) == 0 and len(beta) == 0:
        return True
    if len(alpha) == 0 or len(beta) == 0:
        return False
    return alpha.split()[0] == beta.split()[0]

def equalTail(alpha, beta):
    if len(alpha) == 0 and len(beta) == 0:
        return True
    if len(alpha) == 0 or len(beta) == 0:
        return False
    return alpha.split()[-1] == beta.split()[-1]

def H(Ki, alpha):
    h = []
    for beta in Ki:
        if equalHead(beta, alpha):
            h.append(beta.strip("\n"))
    return h

def T(Ki, alpha):
    t = []
    for beta in Ki:
        if equalTail(beta, alpha):
            t.append(beta.strip("\n"))
    return t

def agg_local_H(Ki, alpha):
    h = H(Ki, alpha)
    if len(h) == 0:
        return 0
    else:
        return sum([mat[sent_index[alpha.strip("\n")]][sent_index[beta.strip("\n")]] for beta in h]) / len(h)

def agg_local_T(Ki, alpha):
    t = T(Ki, alpha)
    if len(t) == 0:
        return 0
    else:
        return sum([mat[sent_index[alpha.strip("\n")]][sent_index[beta.strip("\n")]] for beta in t]) / len(t)


def mc_local(alpha):
    res = 0
    for Ki in mc_K:
        if alpha in Ki:
            res += ((agg_local_H(Ki, alpha)+agg_local_T(Ki, alpha))/2 + 1)
    return res

def score_local(Ki):
    res = 0
    for alpha in Ki:
        mc = mc_local(alpha)
        res += mc
    return res


# start3 = time.time()
cnt = 1
for Ki in mc_K:
    print("Method 2 K{0}  score: {1}".format(cnt, score_local(Ki)))
    cnt += 1
# end3 = time.time()
# print("COS M2 time {0}".format(end3 - start3))


##############################################################################################

# start4 = time.time()

for i in range(len(K)):
    for j in range(i, len(K)):
        mat[i][j] = euc_sim(embeds[i], embeds[j])

for i in range(len(K)):
    for j in range(i):
        mat[i][j] = mat[j][i]

# end4 = time.time()
# print("euclidean calculation time {0}".format(end4 - start4))
print("Euclidean Similarity")
######################### Method 1 ###################################

def agg_all(Ki, alpha):
    res = 0
    alpha = alpha.strip("\n")
    for beta in Ki:
        beta = alpha.strip("\n")
        res += mat[sent_index[beta]][sent_index[alpha]]
    return res / len(Ki)

def mc_all(alpha):
    return sum([(agg_all(Ki, alpha) + 1) for Ki in mc_K])

def score_all(Ki):
    res = 0
    for alpha in Ki:
        mc = mc_all(alpha)
        res += mc
    return res

start5 = time.time()
cnt = 1
for Ki in mc_K:
    print("Method 1 K{0}  score: {1}".format(cnt, score_all(Ki)))
    cnt += 1
end5 = time.time()
print("EUC M1: {0}".format(end5 - start5))

######################### Method 2 ###################################

def equalHead(alpha, beta):
    if len(alpha) == 0 and len(beta) == 0:
        return True
    if len(alpha) == 0 or len(beta) == 0:
        return False
    return alpha.split()[0] == beta.split()[0]

def equalTail(alpha, beta):
    if len(alpha) == 0 and len(beta) == 0:
        return True
    if len(alpha) == 0 or len(beta) == 0:
        return False
    return alpha.split()[-1] == beta.split()[-1]

def H(Ki, alpha):
    h = []
    for beta in Ki:
        if equalHead(beta, alpha):
            h.append(beta.strip("\n"))
    return h

def T(Ki, alpha):
    t = []
    for beta in Ki:
        if equalTail(beta, alpha):
            t.append(beta.strip("\n"))
    return t

def agg_local_H(Ki, alpha):
    h = H(Ki, alpha)
    if len(h) == 0:
        return 0
    else:
        return sum([mat[sent_index[alpha.strip("\n")]][sent_index[beta.strip("\n")]] for beta in h]) / len(h)

def agg_local_T(Ki, alpha):
    t = T(Ki, alpha)
    if len(t) == 0:
        return 0
    else:
        return sum([mat[sent_index[alpha.strip("\n")]][sent_index[beta.strip("\n")]] for beta in t]) / len(t)


def mc_local(alpha):
    res = 0
    for Ki in mc_K:
        if alpha in Ki:
            res += ((agg_local_H(Ki, alpha)+agg_local_T(Ki, alpha))/2 + 1)
    return res

def score_local(Ki):
    res = 0
    for alpha in Ki:
        mc = mc_local(alpha)
        res += mc
    return res


# start6 = time.time()
cnt = 1
for Ki in mc_K:
    print("Method 2 K{0}  score: {1}".format(cnt, score_local(Ki)))
    cnt += 1
# end6 = time.time()
# print("EUC M2  {0}".format(end6 - start6))