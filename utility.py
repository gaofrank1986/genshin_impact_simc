import numpy as np
import json
import pickle
from copy import deepcopy
from basic import Articraft
from character import Character
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


def generate_articrafts(N,luck):
    assert(isinstance(N,int))
    assert(isinstance(luck,int))

    alist = ['head','glass','cup','flower','feather']
    blist=[['cr','cd'],'ar','edr','sh','sa']

    basic_main_rate = 31.1#满爆率

    prop_list = ['ar','edr','cr','cd','phr','sa','sh']
    trans_ratio = [1.5,1.5,1,2,1.875,10,153.7]
    ratio_main = {prop_list[i]:trans_ratio[i] for i in range(len(prop_list))}

    ans = dict()
    for i in alist:
        tmp = blist[alist.index(i)]
        if isinstance(tmp,list):
            ans[i] = []
            for j in tmp:
                tmp = dict()
                tmp[j] = round(basic_main_rate*ratio_main[j],2)
                ans[i].append(tmp.copy())
        else:
            ans[i] = {tmp:round(basic_main_rate*ratio_main[tmp],2)}
            

    ans['sub'] = []
    luck = 3
    total_sub = 31.1*luck
    precision = N
    dist = np.linspace(0,1,precision)
    for i in range(precision):
        for j in range(precision-i):
            tmp =dict()
            tmp['cr'] = total_sub*dist[i]
            tmp['cd'] = total_sub*ratio_main['cd']*dist[j]
            tmp['ar'] = total_sub*ratio_main['ar']*dist[precision-i-j-1]
            ans['sub'].append(tmp)

    with open('./tmp/articraft_run_list.json', 'w') as fp:
        json.dump(ans, fp,indent = 4)

    return(ans)

def get_best_articraft(c,N=50,luck=3):
    assert(isinstance(c,Character))
    ww = generate_articrafts(N,luck)
    diluc = deepcopy(c)
    rls = Articraft()

    save = 0
    for head in ww['head']:
        rls.add(head,'head')
        glass = ww['glass']
        cup = ww['cup']
        flower = ww['flower']
        feather = ww['feather']
        rls.add(glass,'glass')        
        rls.add(cup,'cup')
        rls.add(flower,'flower')
        rls.add(feather,'feather')
        
        for sub in ww['sub']:
            rls.add(sub,'sub')
            diluc.put_on(rls)
            tmp = diluc.damage_output({},"")
            if tmp>save:
                save=tmp
                save4=rls.buf.copy()
            diluc.take_off(rls)
            rls.rm(sub,'sub')
        rls.rm(feather,'feather')
        rls.rm(flower,'flower')
        rls.rm(cup,'cup')
        rls.rm(glass,'glass')
        rls.rm(head,'head')
        
    with open('./data/articrfat.json', 'w') as fp:
        json.dump(save4, fp,indent = 4)
    
        
def translate(RR):
        A=('自然','普通','重击','战技','爆发','被击','满层','普通重击战技爆发','普通重击','战技爆发','重击泄能','自然被击','断流爆','断流斩','终结','激活','普通停止')
        B=('特效增伤','平A增伤','重击增伤','E增伤','Q增伤','Q冷却按秒','E冷却按秒','Q冷却百分比','E冷却百分比','平A增速')#attack
        C=('全伤害','基础攻','固定攻','比例攻','基础防','固定防','比例防','基础血','固定血','比例血','爆率','爆伤','元素精通','元素充能','角色元素种类编号','草风岩雷冰水火物') #data
        '''RR=[触发方式，消耗类别，特效类型，帧数，持续时间，CD，伤害触发次数，BUFF初始层数，BUFF堆叠次数，触发间隔，data类别(AR)，data数据，attack类别(EQ)，attack数据，易伤类别，易伤数据，平A元素附魔，伤害类型，伤害数据]
                     0              1            2              3           4           5            6                        7                    8                      9             10                  11                12                     13                14                  15             16             17             18'''    
# def generate_relics3():

#     alist = ['head','glass','cup','flower','feather']
#     blist=[['ar','cr','cd'],['ar'],['ar','edr'],['sh'],['sa']]

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

#     ans['sub'] = []
#     luck = 3
#     total_sub = 31.1*luck
#     precision = 50
#     dist = np.linspace(0,1,precision)
#     for i in range(precision):
#         for j in range(precision-i):
#             tmp =dict()
#             tmp['cr'] = total_sub*dist[i]
#             tmp['cd'] = total_sub*ratio_main['cd']*dist[j]
#             tmp['ar'] = total_sub*ratio_main['ar']*dist[precision-i-j-1]
#             ans['sub'].append(tmp)

#     with open('relics3.json', 'w') as fp:
#         json.dump(ans, fp,indent = 4)

#     return(ans)

    # def json_generator(path,na,ne):
    #     tmp = dict()
    #     tmp['name'] = ''
    #     tmp['level'] = ''
    #     tmp['elem_class'] = ''
    #     tmp['constellation'] = ''

    #     tmp['basic_health'] = 0
    #     tmp['basic_attack'] = 0
    #     tmp['basic_defense'] = 0
    #     tmp['break_thru'] = {'cr':0}

    #     name =['a','e','q']
    #     num = [na,ne,1]

    #     for i in range(3):
    #         tmp[name[i]] = dict()
    #         tmp[name[i]]['n'] = na
    #         tmp[name[i]]['atk_type'] = ''
    #         for j in range(1,num[i]+1):
    #             tmp[name[i]]['ratio_'+str(j)] =()
    #         tmp[name[i]]['time'] = (0,)*num[i]

    #     tmp['a']['atk_type'] = 'physic'
    #     tmp['e']['reset_a'] = 'no'
    #     tmp['q']['reset_a'] = 'yes'

    #     with open(path, 'w') as fp:
    #         json.dump(tmp, fp,indent = 4)

    # for head in ww['head']:
    #     rls.add(head,'head')
    #     for glass in ww['glass']:
    #         rls.add(glass,'glass')
    #         for cup in ww['cup']:
    #             rls.add(cup,'cup')
    #             for flower in ww['flower']:
    #                 rls.add(flower,'flower')
    #                 for feather in ww['feather']:
    #                     rls.add(feather,'feather')
    #                     for sub in ww['sub']:
    #                         rls.add(sub,'sub')
    #                         Nsim+=1
    #                         print(Nsim)
    #                         diluc.equip(rls)

    #                         tmp = diluc.damage_output()
    #                         if tmp>save:
    #                             save=tmp
    #                             save4=(tmp,diluc.attack.copy(),rls.attack.copy(),rls.buf.copy())
    #                         save2.append(tmp)
    #                         save3.append((tmp,diluc.attack.copy(),rls.attack.copy(),rls.buf.copy()))

    #                         if(len(save3)%1e4==0)and(len(save3)>0):
    #                                 with open("result.pk", "ab") as f:
    #                                     pickle.dump(save2, f)
    #                                     pickle.dump(save3, f)

    #                         diluc.de_equip(rls)
    #                         rls.rm(sub,'sub')
    #                     rls.rm(feather,'feather')
    #                 rls.rm(flower,'flower')
    #             rls.rm(cup,'cup')
    #         rls.rm(glass,'glass')
    #     rls.rm(head,'head')