import numpy as np
import json
import pickle
from copy import deepcopy
import logging
import os

from buff import Buff
from basic import Articraft,Env
from character import Character
from utility import get_best_articraft


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
    env.set_endtime(200)
    cycle = 20
    c = Character(6,6,logger)
    a = Articraft()
    c.load_from_json("./data/diluc.json")
    c.load_weapon_from_json("./data/claymore.json","lm")

    # get_best_articraft(c)

    a.load_json("./data/articraft.json")
    c.put_on(a)



    # input()

    exit_flag = False
    for j in range(cycle):
        if exit_flag:
            break
        for i in range(len(c.action_seq)):
            
            action = c.action_seq[i]
            # if action=='w':
            #     env.tick(0.2)
            #     logger.info("wait 0.2s")
            #     continue
            if len(c.guarantee_gap)>0 and action in c.guarantee_gap and c.acc['e']>0:
                # if(env.now()<diluc.last_atk[action]+diluc.guarantee_gap[action]):
                next_time = c.last_atk[action]+c.guarantee_gap[action]
                if(env.not_yet(next_time)):
                    logger.info("Time tick {:.2f} to guarantee gap for {}".format(next_time-env.now(),action))
                    env.set(c.last_atk[action]+c.guarantee_gap[action])
                    
            while True:
                if env.end():
                    logger.info("time is up.")
                    exit_flag = True
                    break
                if c.atk_ready(env,[action]):
                    break
                else:
                    # logger.info("{} is not ready,Tick 0.1 s.{}".format(action,env.now()))
                    # env.tick(0.1)
                    logger.info("{} is not ready, 平a补空.".format(action))
                    c.generic_atk('a',env,logger)
            if exit_flag:
                break

            c.generic_atk(action,env,logger)
    logger.info("DPS：{}".format(c.dmg.sum()/env.now()))
    logger.info("damage dist1：{}".format(c.dmg))
    logger.info("damage dist2：{}".format(c.dmg2))

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


# Referenc:
#
# https://nga.178.com/read.php?tid=23531553
#https://bbs.nga.cn/read.php?tid=23537886&rand=541
# https://bbs.nga.cn/read.php?tid=24038318&forder_by=postdatedesc&rand=475
# https://nga.178.com/read.php?tid=23537886