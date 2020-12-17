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
        self.simtime = int(simtime*100)
    def set(self,t):
        self.timer = int(t*100)
    def end(self):
        return (self.timer>self.simtime)
    def now(self):
        return(round(self.timer/100,2))
    def add(self,dif):
        return(round(self.timer/100,2)+dif)
    def tick(self,dif):
        self.timer+=int(dif*100)
    def on_time(self,v):
        return(int(v*100)<=self.timer)

    def not_yet(self,v):
        return(int(v*100)>self.timer)
    
    def over_time(self,v):
        return(int(v*100)<self.timer)

if __name__ == "__main__":


    os.remove("./main.log")
    logger = logging.getLogger('Main')
    logger.setLevel(level=logging.INFO)
    fh = logging.FileHandler('./main.log','w+')
    fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s",datefmt='%m-%d,%H:%M')
    fh.setFormatter(fmt)
    logger.addHandler(fh)
    logger.propagate = False


    env = Env()
    env.set_endtime(100)

    diluc = character(6,6,logger)
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
    for j in range(10):
        for i in range(len(diluc.action_seq)):
            action = diluc.action_seq[i]
            # if action=='w':
            #     env.tick(0.2)
            #     logger.info("wait 0.2s")
            #     continue
            if len(diluc.guarantee_gap)>0 and action in diluc.guarantee_gap and diluc.acc['e']>0:
                # if(env.now()<diluc.last_atk[action]+diluc.guarantee_gap[action]):
                next_time = diluc.last_atk[action]+diluc.guarantee_gap[action]
                if(env.not_yet(next_time)):
                    logger.info("Time tick {:.2f} to guarantee gap for {}".format(next_time-env.now(),action))
                    env.set(diluc.last_atk[action]+diluc.guarantee_gap[action])
                    
            while True:
                if diluc.atk_ready(env,[action]):
                    break
                else:
                    # logger.info("{} is not ready,Tick 0.1 s.{}".format(action,env.now()))
                    # env.tick(0.1)
                    logger.info("{} is not ready, 平a补空.".format(action))
                    diluc.generic_atk('a',env,logger)


            diluc.generic_atk(action,env,logger)
    input()
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


# Referenc:
#
# https://nga.178.com/read.php?tid=23531553
#https://bbs.nga.cn/read.php?tid=23537886&rand=541
# https://bbs.nga.cn/read.php?tid=24038318&forder_by=postdatedesc&rand=475
# https://nga.178.com/read.php?tid=23537886