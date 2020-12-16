import numpy as np
import json
import pickle
from copy import deepcopy
import logging
import os

from buff import Buff
from basic import weapon,relics
from character import character

'''环境，目前只有时间,考虑用毫秒计数的整数类型代替实数类型'''
class Env():
    def __init__(self):
        self.timer = 0
    def set_endtime(self,simtime):
        self.simtime = simtime
    def end(self):
        return (self.timer>self.simtime)
    def now(self):
        return(round(self.timer,2))
    def add(self,dif):
        # self.timer+=round(dif,2)
        return(self.timer+round(dif,2))
    def tick(self,dif):
        self.timer+=round(dif,2)










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


if __name__ == "__main__":

    # logging.basicConfig(level=logging.CRITICAL,format="%(levelname)s %(message)s")
    # logging.basicConfig(level=logging.INFO)
    os.remove("./main.log")
    logger = logging.getLogger('Main')
    logger.setLevel(level=logging.INFO)
    fh = logging.FileHandler('./main.log','w+')
    fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s",datefmt='%m-%d,%H:%M')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.propagate = False


    env = Env()
    env.set_endtime(20)

    diluc = character(6,6)
    diluc.load_from_json("./data/diluc.json")

    # for i in range(50000):
    #     if env.end():
    #         logger.info('end {} {}'.format(i,env.now()))
    #         break
    #     if diluc.atk_ready(env,['q']):
    #         diluc.generic_atk('q',env,logger)
    #     else:
    #         pass
    #         env.tick(0.1)
    #         logger.info("no q avail {} {:.2f}".format(i,env.now()))
    #     if diluc.atk_ready(env,['e']):
    #         for j in range(3): #e段数
    #             if  env.end() or diluc.atk_ready(env,['q']):
    #                 logger.info(" q ready")
    #                 break
    #             # if diluc.status['e'] == 'off':
    #             #     break
    #             for ii in range(diluc.multiple_e):
    #                 diluc.generic_atk('e',env,logger)
    #             for k in range(2):#普攻段数
    #                 if env.end() or  diluc.atk_ready(env,['e','q']):
    #                     logger.info(" q or e ready")
    #                     break
    #                 diluc.generic_atk('a',env,logger)
    #                 # env.timer+=0.1

    #     else:
    #         pass
    #         logger.info("no e avail {} {:.2f}".format(i,env.now()))
    for j in range(2):
        for i in range(len(diluc.action_seq)):
            action = diluc.action_seq[i]
            while True:
                if diluc.atk_ready(env,[action]):
                    break
                else:
                    # logger.info("{} is not ready,Tick 0.1 s.{}".format(action,env.now()))
                    # env.tick(0.1)
                    logger.info("{} is not ready, 平a补空.".format(action))
                    diluc.generic_atk('a',env,logger)


            diluc.generic_atk(action,env,logger)

    # ww = generate_relics3()

    # rls = relics()

    # save = 0
    # save4 = None
    # save2 = []
    # save3 = []
    # Nsim = 0


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


# https://nga.178.com/read.php?tid=23531553
#https://bbs.nga.cn/read.php?tid=23537886&rand=541
# https://bbs.nga.cn/read.php?tid=24038318&forder_by=postdatedesc&rand=475
# https://nga.178.com/read.php?tid=23537886