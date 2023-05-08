import json
import re
import numpy as np

# The entities in entity2id.txt are stored the entity_list in order.
entity_file_name = "./datasetProcess/newData/UOBM35/entity2id.txt"
entity_list = []
with open(entity_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n').split("\t")
        entity_list.append(line[0])
    entity_list = entity_list[1:]

# The relations in relation2id.txt are stored in the relation_list in order.
relation_file_name = "./datasetProcess/newData/UOBM35/relation2id.txt"
relation_list = []
with open(relation_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n').split("\t")
        relation_list.append(line[0])
    relation_list = relation_list[1:]


# Entity and relation and their corresponding embedding are stored in the dictionary.
# key: entity/relation  value: embedding
with open('./embed/transd_UOBM35_embed.vec','r',encoding='utf8') as fp:
    json_data = json.load(fp)

ent2embed_dict = {}
for idx, entity in enumerate(entity_list):
    ent2embed_dict[entity] = json_data['ent_embeddings.weight'][idx]

rel2embed_dict = {}
for idx, relation in enumerate(relation_list):
    rel2embed_dict[relation] = json_data['rel_embeddings.weight'][idx]


# Axioms and its axiomatic vector representations are stored in the dictionary.
# key: axiom  value: vector representation of axiom
UOBM35Axioms_file_name = "./datasetProcess/oriData/UOBM35allAxioms.txt"
UOBM35Axioms_list = []
with open(UOBM35Axioms_file_name, "r") as f:
    for line in f.readlines():
        line = line.strip('\n')
        UOBM35Axioms_list.append(line)

axiom2embedd_dict = {}
for axiom in UOBM35Axioms_list:
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
with open("./UOBM/UOBM35/MCS1") as f:
    K1 = f.read().split("\n\n")
    for axiom in K1:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS2") as f:
    K2 = f.read().split("\n\n")
    for axiom in K2:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS3") as f:
    K3 = f.read().split("\n\n")
    for axiom in K3:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS4") as f:
    K4 = f.read().split("\n\n")
    for axiom in K4:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS5") as f:
    K5 = f.read().split("\n\n")
    for axiom in K5:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS6") as f:
    K6 = f.read().split("\n\n")
    for axiom in K6:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS7") as f:
    K7 = f.read().split("\n\n")
    for axiom in K7:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS8") as f:
    K8 = f.read().split("\n\n")
    for axiom in K8:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS9") as f:
    K9 = f.read().split("\n\n")
    for axiom in K9:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS10") as f:
    K10 = f.read().split("\n\n")
    for axiom in K10:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS11") as f:
    K11 = f.read().split("\n\n")
    for axiom in K11:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS12") as f:
    K12 = f.read().split("\n\n")
    for axiom in K12:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS13") as f:
    K13 = f.read().split("\n\n")
    for axiom in K13:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS14") as f:
    K14 = f.read().split("\n\n")
    for axiom in K14:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS15") as f:
    K15 = f.read().split("\n\n")
    for axiom in K15:
        Kset.add(axiom)
    f.close()
with open("./UOBM/UOBM35/MCS16") as f:
    K16 = f.read().split("\n\n")
    for axiom in K16:
        Kset.add(axiom)
    f.close()

K = list(Kset)
mc_K = [K1,K2,K3,K4,K5,K6,K7,K8,K9,K10,K11,K12,K13,K14,K15,K16]
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