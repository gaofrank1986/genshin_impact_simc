import numpy as np
import json
import pickle
from copy import deepcopy
import logging

class Basic_Panel():
    def __init__(self):
        self.health = np.zeros(3)
        self.attack = np.zeros(9)
        self.defense = np.zeros(3)
        self.att_name = ['ba','ar','sa','cr','cd','edr','phr','em','ef']
        self.h_name = ['bh','hr','sh']
        self.d_name = ['bd','dr','sd']
        # self.enhance_rate = np.zeros(9) #7元素 1物理 1全伤
        # '元素伤害+物理伤害:  火   水   冰   雷   岩   风   草  物'
        # '                [0]  [1] [2]  [3]  [4]  [5]  [6]  [7]'
        # self.debuff = np.zeros(6)
        # self.em_name = ['em','ef']
        # self.elem_mastery = np.zeros(2) #EM EF

class weapon(Basic_Panel):
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

class relics(Basic_Panel):
    def __init__(self,star_level=5):
        super().__init__()
        self.buf = dict()

    def add(self,item,pos):
        for i in item:
            if i!='sh':
                self.attack[self.att_name.index(i)]+=item[i]
        self.buf[pos] = item
        #可以加重复报警

    def rm(self,item,pos):
        for i in item:
            if i!='sh':
                self.attack[self.att_name.index(i)]-=item[i]
        self.buf[pos] = None

    def load_json(self,path):
        with open(path, 'r') as fp:
            tmp = json.load(fp)
            for i in tmp:
                self.add(tmp[i],i)

    def save_json(self,path):
        with open(path, 'w') as fp:
            json.dump(self.buf,fp,indent = 4)