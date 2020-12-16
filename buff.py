import numpy as np
import json
import pickle
from copy import deepcopy
import logging
logging.basicConfig(level=logging.INFO)

class Buff():
    def __init__(self,a,effect,name='',cmt=''):

        prop_name = ['event','chckout_evnt','type','lead_in','duration','cooldown','dmg_tnum','cscd_init','cscd_max','chckout_delay']
        #多段可以加一个,time_out,time_out之内没进行二段重置段数，检查cd
        ##'data_ty','data','atk_ty','atk','debuf_ty','debuf','enchant','dmg_ty','dmg']
        # p1 = ['alld','ba','sa','ar','bd','sd','dr','bh','sh','hr','cr','cd','em','ef','ele','c','v','r','t','i','w','f','p']
        # p2 = ['0','a','h','e','q','reduced_time_e','reduced_time_q','reduced_perc_e','reduced_perc_q','speed']
        # element = ['fire','thunder','water','ice','wind','rock','grass']
        # Delement = ['D'+i for i in element]

        self.name = name

        self.prop = {prop_name[i]:a[i] for i in range(len(prop_name))}
        self.cmt = cmt

        # if effect == None:
        #     # self.bonus= dict()
        #     # self.bonus[p1[a[10]]] = a[11]
        #     # if a[12]!= 0:
        #     #     self.bonus[p2[a[12]]] = a[13]
        #     # self.bonus[Delement[a[14]]] = a[15]
        #     # self.bonus['enchant'] = a[16]
        #     pass
        # else:
        self.bonus = effect



        self.status = 'off'
        self.start_time = []
        self.end_time = []
        self.next_avail = 0
        self.next_chckout = []
        self.cscd_num = 0
        self.expired =[]
        self.valid = []
        self.logger = None
        self.MAX_B = 10#最高存储10层

    def record(self,env):
        ans = [self.start_time[-1],self.end_time[-1],self.next_avail,self.next_chckout[-1],env.timer,0]
        ans = np.array(ans)
        ans = np.round(ans,2)
        return(ans)

    def expire(self,env):
        tmp = self.valid.pop(0)
        tmp[-1] = env.now()
        self.expired.append(tmp)

    def check_status(self,env):
        while True:
            if len(self.start_time)!=0 and env.now()>self.end_time[0]:
                self.logger.info("Buff状态检查 有效期结束 第一层Buff失效,开始时间: {:.2f} 结束时间 {:.2f} 当前时间 {:.2f} ".format(self.start_time[0],self.end_time[0],env.now()))
                # self.expired.append((self.start_time,self.end_time,env.timer))
                # tmp = self.valid.pop(0)
                # tmp[-1] = env.timer
                # self.expired.append(tmp)
                if(len(self.valid)>0):
                    self.expire(env)
                    if len(self.next_chckout)>0:
                        self.next_chckout.pop(0)

                self.end_time.pop(0)
                self.start_time.pop(0)
                if self.cscd_num>=1:
                    self.cscd_num-=1
            if len(self.start_time) == 0:
                if self.status == 'on':
                    self.status = 'off'
                    self.logger.info("Buff状态检查 buff状态 切换关闭")
                    self.next_chckout = [] #对么？？

                break
            if len(self.start_time) > self.MAX_B:
                self.end_time.pop(0)
                self.start_time.pop(0)
                if(len(self.valid)>0):
                    self.logger.info("Buff状态检查  存储超限 buff 失效")
                    self.expire(env)
                    if len(self.next_chckout)>0:
                        self.next_chckout.pop(0)

            if env.now() <= self.end_time[0]:
                        break

    def activate(self,event_list,env):
        assert(self.logger!=None)
        self.logger.debug('--------buff activating({})-----------------------'.format(env.now()))
        if self.prop['event'] in event_list:
            if self.prop['type'] == 0:

                self.check_status(env)

                '''cd 结束'''
                if env.now() >= self.next_avail:
                        '''此时层数为0'''
                        if self.cscd_num ==0:
                            '''如果初始层数不为0：1.用光了 2.还没激活过'''
                            if self.prop['cscd_init']!=0:
                                self.cscd_num = self.prop['cscd_init']
                                #检查条件
                                self.reset_time()

                        self.status = 'on'
                        self.cscd_num += 1
                        self.start_time.append(env.now())
                        self.end_time.append(env.add(self.prop['duration']))
                        self.next_avail = env.add(self.prop['cooldown'])


                        '''如果存在结算延迟下次可以结算时间记录，否则下次可结算时间为当前时间'''
                        if (self.prop['chckout_delay']>0):
                            self.next_chckout.append(env.add(self.prop['chckout_delay']))
                        else:
                            self.next_chckout.append(env.now())

                        # '''如果最大只有一层 而且时间累计超出，自动刷新'''
                        # if self.prop['cscd_max'] == 1 and len(self.start_time)>1:
                        #     self.end_time.pop(0)
                        #     self.start_time.pop(0)
                        #     logger.info(self.name+"自动刷新")
                        # print(self.cscd_num,"层数")

                        '''如果层数超出上限，刷新'''
                        if self.cscd_num > self.prop['cscd_max']:
                            self.cscd_num = self.prop['cscd_max']
                            # if self.prop['cscd_max'] > 1 and
                            if self.prop['cscd_max']!=self.prop['cscd_init']: #直接设置初始，激活后增加一层，如果超过最大，不用刷新
                                if len(self.start_time) - len(self.next_chckout)>0:#根据2命修改的0,4命没有问题  如果不消耗可以一直堆valid buff到 MAX_B,2命消耗以后，堆叠次数不能超过cscd_max,4命不消耗，可以继续堆
                                    self.end_time.pop(0)
                                    self.start_time.pop(0)
                                    self.logger.info("层数溢出,刷新(第一层失效)")
                                    self.expire(env)

                        # if self.prop['event'] in ['e']:
                        #     if len(self.start_time)>1:
                        #         self.end_time.pop(0)
                        #         self.start_time.pop(0)
                        #         self.logger.info("限制技能buff共存,刷新")
                        #         self.expire(env)
                        #         # self.next_chckout.pop(0)





                        self.logger.info("Buff生效 层数:{},开始时间: {:.2f} 结束时间 {:.2f} 下次激活时间 {:.2f} 下次可结算时间：{:.2f}".format(self.cscd_num,self.start_time[-1],self.end_time[-1],self.next_avail,self.next_chckout[-1]))#结算第一层
                        # self.valid.append((self.start_time[-1],self.end_time[-1],self.next_avail,self.next_avail,self.next_chckout[-1],env.timer))
                        # print("record",self.record(env))
                        self.valid.append(self.record(env))
                else:
                    '''若无激活,这里需要么？'''
                    # self.next_chckout.append(env.timer)
                    pass
        pass
        self.logger.debug("start_time  :{} status {}".format(self.start_time,self.status))
        self.logger.debug("next chckout:{}".format(self.next_chckout))
        self.logger.debug("valid buff  :{}".format(self.valid))
        self.logger.debug("expired buff:{}".format(self.expired))

    def reset_all(self):
        self.status = 'off'
        self.start_time = []
        self.end_time = []
        self.next_avail = 0
        self.next_chckout = 0
        self.cscd_num = 0

    def reset_time(self):
        self.status = 'off'
        self.start_time = []
        self.end_time = []

    def checkout(self,event_list,env):
        assert(self.logger!=None)
        self.logger.debug('--------buff checking out({})-----------------------'.format(env.now()))
        ans = dict()
        if self.prop['chckout_evnt'] in event_list:
            if self.prop['type'] == 0:
                self.check_status(env)
                if self.status== 'on':
                    # '''激活一次可以多次结算的情况，本次没激活但仍有buff是激活状态时候，chckout没有记录'''
                    if len(self.next_chckout) == 0:
                        self.next_chckout.append(env.now())
                    '''如果可结算 而且 当前时间大于可结算时间(最新？)'''
                    if len(self.next_chckout) >0 and env.now()>=self.next_chckout[0]:#if不是尺骨剑


                        if self.prop['chckout_evnt'] == 'auto':
                            # if self.cscd_num > 1:
                            for i in self.bonus:
                                ans[i] = self.bonus[i]*self.cscd_num
                            # else:
                            #     ans = self.bonus
                            # return ans
                        elif self.prop['chckout_evnt'] in ['e','q','a']:
                            '''6命现在可以有两层同时valid的情况要改么？TODO'''
                            # self.logger.info("Buff结算 层数:{},开始时间: {:.2f} 结束时间 {:.2f} 下次激活时间 {:.2f} 下次可结算时间：{:.2f}".format(self.cscd_num,self.start_time[-1],self.end_time[-1],self.next_avail,self.next_chckout[-1]))

                            ans = self.bonus
                            self.cscd_num -= 1 #4命结算消耗层数，2命结算不消耗

                            if self.cscd_num == 0:
                                # '''只有6命情况，会有eqe的情况，因为buff=off所以第二段没启发作用，需要再看下valid同时有两个buff存在'''
                                self.status = 'off'
                                self.expire(env)
                                tmp = self.start_time.pop(0)
                                self.end_time.pop(0)
                                self.logger.info("Buff结算后失效 层数:{},消耗层开始时间: {:.2f},有效堆叠: {}".format(self.cscd_num,tmp,len(self.start_time)))


                        else:
                            pass
                        '''消耗结算一次,如果消耗结算次数'''
                        self.next_chckout.pop(0)

                else:
                    pass

        self.logger.debug("start_time  :{}".format(self.start_time))
        self.logger.debug("next chckout:{}".format(self.next_chckout))
        self.logger.debug("valid buff  :{}".format(self.valid))
        self.logger.debug("expired buff:{}".format(self.expired))
        if len(ans) > 0:
            self.logger.info("Buff结算  :{}".format(ans))

        return ans