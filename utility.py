import numpy as np
import json
import pickle

# def gen_sub_dist(l,n):
#     if l==1:
#         return([n])
#     if n==0:
#         return([np.zeros(l)])
#     buf=[]
#     tmp = np.zeros(l)
#     for i in range(0,n+1):
#         tmp[0] = i
#         for j in gen_sub_dist(l-1,n-i):
#             tmp[1:] = j
#             buf.append(tmp.copy())
#     return(buf)

# def generate_relics():
#     # alist = ['理之冠'，'时之沙',,'空之杯','生之花','死之羽'] #311
#     # glass_list = ['ar','dr','hr','ef','em']
#     # cup_list = ['ar','dr','hr','edr','phr','em']
#     # head_list = ['ar','dr','hr','cr','cd','cure_r','em']
#     # sub_list = ['cr','hr','ar','ef','dr','cd','sa','sd','em','sh']
#     # trans_ratio = [2.7,4.1,4.1,4.5,5.1,5.4,14,16,16,209]

#     alist = ['head','glass','cup','flower','feather']
#     blist=[['ar','cr','cd'],['ar'],['ar','edr'],['sh'],['sa']]

#     basic_main_rate = 31.1#满爆率

#     sub_level = np.array([2.7,3.1,3.5,3.9])
#     basic_sub_rate = sub_level[0]#满爆率

#     sub_list= ['ar','cr','cd','sa']

#     prop_list = ['ar','edr','cr','cd','phr','sa','sh']
#     trans_ratio = [1.5,1.5,1,2,1.875,10,153.7]
#     ratio_main = {prop_list[i]:trans_ratio[i] for i in range(len(prop_list))}


#     ans = dict()
#     for i in alist:
#         ans[i] = []
#         for j in blist[alist.index(i)]:
#             tmp = dict()
#             tmp[j] = round(basic_main_rate*ratio_main[j],2)

#             roll_list = sub_list.copy()
#             if j in roll_list:
#                 roll_list.remove(j)
#             random_list = gen_sub_dist(len(roll_list),5)
#             for k in random_list:
#                 for l in roll_list:
#                     factor = k[roll_list.index(l)]+1
#                     tmp[l] = round(basic_sub_rate*ratio_main[l]*factor,2)
#                     # tmp[l] = factor
#                 ans[i].append(tmp.copy())

#     with open('relics.json', 'w') as fp:
#         json.dump(ans, fp,indent = 4)

#     return(ans)

# def generate_relics2():

#     alist = ['head','glass','cup','flower','feather']
#     blist=[['ar','cr','cd'],['ar'],['ar','edr'],['sh'],['sa']]
#     # blist=[['ar','cr','cd'],['ar'],['ar','edr','phr'],['sh'],['sa']]

#     basic_main_rate = 31.1#满爆率

#     prop_list = ['ar','edr','cr','cd','phr','sa','sh']
#     trans_ratio = [1.5,1.5,1,2,1.875,10,153.7]
#     ratio_main = {prop_list[i]:trans_ratio[i] for i in range(len(prop_list))}

#     ans = dict()
#     for i in alist:
#         ans[i] = []
#         for j in blist[alist.index(i)]:
#             tmp = dict()
#             tmp[j] = round(basic_main_rate*ratio_main[j],2)
#             ans[i].append(tmp.copy())

#     with open('relics2.json', 'w') as fp:
#         json.dump(ans, fp,indent = 4)

#     return(ans)

def generate_relics3():

    alist = ['head','glass','cup','flower','feather']
    blist=[['ar','cr','cd'],['ar'],['ar','edr'],['sh'],['sa']]

    basic_main_rate = 31.1#满爆率

    prop_list = ['ar','edr','cr','cd','phr','sa','sh']
    trans_ratio = [1.5,1.5,1,2,1.875,10,153.7]
    ratio_main = {prop_list[i]:trans_ratio[i] for i in range(len(prop_list))}

    ans = dict()
    for i in alist:
        ans[i] = []
        for j in blist[alist.index(i)]:
            tmp = dict()
            tmp[j] = round(basic_main_rate*ratio_main[j],2)
            ans[i].append(tmp.copy())

    ans['sub'] = []
    luck = 3
    total_sub = 31.1*luck
    precision = 50
    dist = np.linspace(0,1,precision)
    for i in range(precision):
        for j in range(precision-i):
            tmp =dict()
            tmp['cr'] = total_sub*dist[i]
            tmp['cd'] = total_sub*ratio_main['cd']*dist[j]
            tmp['ar'] = total_sub*ratio_main['ar']*dist[precision-i-j-1]
            ans['sub'].append(tmp)

    with open('relics3.json', 'w') as fp:
        json.dump(ans, fp,indent = 4)

    return(ans)