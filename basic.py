import numpy as np
import json
import pickle
from copy import deepcopy
import logging


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


class Basic_Panel():
    def __init__(self):
        self.health = np.zeros(3)
        self.attack = np.zeros(9)
        self.defense = np.zeros(3)
        self.att_name = ['ba','ar','sa','cr','cd','ed','pd','em','ef']
        self.h_name = ['bh','hr','sh']
        self.d_name = ['bd','dr','sd']
        # self.enhance_rate = np.zeros(9) #7元素 1物理 1全伤
        # '元素伤害+物理伤害:  火   水   冰   雷   岩   风   草  物'
        # '                [0]  [1] [2]  [3]  [4]  [5]  [6]  [7]'
        # self.debuff = np.zeros(6)
        # self.em_name = ['em','ef']
        # self.elem_mastery = np.zeros(2) #EM EF

class Weapon(Basic_Panel):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.refine = 1

    def load(self,info):
        for i in info:
            if i in ['name','level','refine']:
                pass
            if i in ['bh']:
                self.health[0] = info[i]
            if i in ['bd']:
                self.defense[0] = info[i]
            if i in self.att_name:
                self.attack[self.att_name.index(i)]+=info[i]

class Articraft(Basic_Panel):
    def __init__(self,star_level=5):
        super().__init__()
        self.buf = dict()

    def add(self,item,pos):
        for i in item:
            if i in self.att_name:
                self.attack[self.att_name.index(i)]+=item[i]
            if i in self.h_name:
                self.health[self.h_name.index(i)]+=item[i]
            if i in self.d_name:
                self.defense[self.d_name.index(i)]+=item[i]
        self.buf[pos] = item
        #可以加重复报警

    def rm(self,item,pos):
        for i in item:
            if i in self.att_name:
                self.attack[self.att_name.index(i)]-=item[i]
            if i in self.h_name:
                self.health[self.h_name.index(i)]-=item[i]
            if i in self.d_name:
                self.defense[self.d_name.index(i)]-=item[i]
        self.buf[pos] = None

    def load_json(self,path):
        with open(path, 'r') as fp:
            tmp = json.load(fp)
            for i in tmp:
                self.add(tmp[i],i)
        self.attack = np.round(self.attack,2)

    # def save_json(self,path):
    #     with open(path, 'w') as fp:
    #         json.dump(self.buf,fp,indent = 4)