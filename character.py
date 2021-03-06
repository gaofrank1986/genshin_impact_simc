import numpy as np
import json
import pickle
from copy import deepcopy
import logging
from buff import Buff
from basic import Basic_Panel
import os

class Character(Basic_Panel):
    def __init__(self,skill_level,c_level,main_logger):
        assert(isinstance(main_logger,logging.Logger))
        super().__init__()
        self.name = ''

        self.skill = dict()
        self.skill_level = [skill_level]*3
        self.constellation = c_level
        self.elem_class = ''

        '''人物自带初始5暴击，50暴伤'''
        self.attack[3] = 5
        self.attack[4] = 50

        self.action_seq = ''

        self.main_logger = main_logger
        #-------------
        self.multiple_e = 1 #可莉砂糖E可以放两次
        # self.e_time_out = 3 #迪卢克多段e间隔时间
        self.e_count = 0
        self.e_save = None
        self.guarantee_gap = None
        #------------------
        self.equipment=[]



        #------


        self.acc ={'e':0,'a':0,'q':0}
        self.next_atk = {'e':0.0,'a':0.0,'q':0.0}
        self.last_atk = {'e':0.0,'a':0.0,'q':0.0}

        # self.status['e'] = 'on'

        self.activated_buff =['q','e']
        self.buff_stack = []

        self.dmg = np.zeros(4) # AD HD E Q     '元素伤害 ED?
        self.dmg2 = np.zeros(2) #physic elem



    def put_on(self,a):
        self.health = self.health+a.health
        self.attack = self.attack+a.attack
        self.defense = self.defense+a.defense

    def take_off(self,a):
        self.health = self.health-a.health
        self.attack = self.attack-a.attack
        self.defense = self.defense-a.defense

    def add_buff(self,b):
        # self.buff_stack.append(deepcopy(b))
        self.buff_stack.append(b)

    def load_from_json(self,path):
        buff_name={'c1':'1命','c2':'2命','c4':'4命','c6':'6命','q':'元素爆发','e':'元素战技'}
        skill_name=['n','ratio','time','cd','ele','reset_a']
        atk_name = ['a','e','q']

        for i in range(1,self.constellation+1):
            self.activated_buff.append("c"+str(i))
        with open(path, 'r', encoding='UTF-8') as fp:
            data = json.load(fp)

        self.name = data['name']
        self.elem_class = data['elem_class']

        self.health[0] = data['basic_health']
        self.defense[0] = data['basic_defense']
        self.attack[0] = data['basic_attack']
        self.load_att(data['break_thru'])

        '''3命，5命对应技能等级+3'''
        if 'c3' in self.activated_buff:
            self.skill_level[atk_name.index('e')]+=3
        if 'c5' in self.activated_buff:
            self.skill_level[atk_name.index('q')]+=3

        '''从 json文件中读取信息，建立self.skill信息'''
        for i in atk_name:
            tmp2 =[]
            for j in range(data[i]['n']):
                tmp2.append(data[i]['ratio_'+str(j+1)][self.skill_level[atk_name.index(i)]-1])
            self.skill[i] = [data[i]['n'],tuple(tmp2),tuple(data[i]['time']),data[i]['cooldown'],data[i]['atk_type'],data[i]['reset_a']]

        '''加载激活的buff'''
        for i in data['skills'].keys():
            if i in self.activated_buff:
                if len(data['skills'][i][0])!=0:
                    self.main_logger.info("加载 2类 {} {} {} ".format(self.name,buff_name[i],data['skills'][i][2]))
                    self.add_buff(Buff(data['skills'][i][0],data['skills'][i][1],"{}_{}".format(self.name,buff_name[i]),data['skills'][i][2]))
                else:
                    self.main_logger.info("加载 1类 {} {} {} ".format(self.name,buff_name[i],data['skills'][i][2]))
                    self.load_att(data['skills'][i][1])


        '''buff logger初始化'''
        # 初始删除所有log
        #--------------
        directory = "./tmp"
        files_in_directory = os.listdir(directory)
        filtered_files = [file for file in files_in_directory if file.endswith(".log")]
        for file in filtered_files:
            path_to_file = os.path.join(directory, file)
            os.remove(path_to_file)
        #----------
        self.init_buff_logger
        for i in self.buff_stack:
            
            i.logger = self.init_buff_logger('Buff.'+i.name,'./tmp/'+i.name+'_buff.log')
            # i.logger.setLevel(logging.DEBUG)
            i.logger.setLevel(logging.INFO)
            i.logger.info(i.cmt)

        self.dlogger = self.init_buff_logger('Dmg','./tmp/damage.log')
        self.dlogger.setLevel(logging.DEBUG)

        '''改变相应的控制开关'''
        for i in data['switch']:
            # if j in self.activated_buff:
                t = data['switch'][i]
                self.skill[t[0]][skill_name.index(t[1])] = self.switch(self.skill[t[0]][skill_name.index(t[1])])

        '''可累积e次数的设定'''
        self.multiple_e = data['multiple_e']
        if self.multiple_e > 1:
            self.e_save = [0.0]*(self.multiple_e-1)
        self.guarantee_gap = data["guarantee_gap"]
        self.action_seq = data['attack_seq']

    def init_buff_logger(self,a,b):
        # assert(isinstance(i,Buff))
        tmp = logging.getLogger(a)
        fh = logging.FileHandler(b,'w+')
        fmt = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s",datefmt='%m-%d,%H:%M')
        fh.setFormatter(fmt)
        tmp.addHandler(fh)
        tmp.propagate = False

        return tmp


    def load_att(self,info):
        assert(isinstance(info,dict))
        for i in info:
            if i in self.att_name:
                self.attack[self.att_name.index(i)]+=info[i]
            else:
                print(i,"is not loaded to the character")

    def switch(self,a):
        assert(a in ['yes','no'])
        if a == 'yes':
            return 'no'
        else:
            return 'yes'
    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------

    def load_weapon_from_json(self,path,name):

        with open(path, 'r', encoding='UTF-8') as fp:
            data = json.load(fp)
        found = False
        
        for wp in data:
            if wp == name:
                found = True
                self.equipment.append((data[wp]['name'],data[wp]['refine']))
                self.attack[0] += data[wp]['basic_attack']
                self.load_att(data[wp]['effect'])

                '''加载激活的buff'''
                for i in data[wp]['special'].keys():
                        if len(data[wp]['special'][i][0])!=0:
                            self.main_logger.info("加载 2类 {} {} {} ".format(data[wp]['name'],"武器效果",data[wp]['special'][i][2]))
                            self.add_buff(Buff(data[wp]['special'][i][0],data[wp]['special'][i][1],"{}_{}".format(data[wp]['name'],"武器效果"),data[wp]['special'][i][2]))
                            self.buff_stack[-1].logger = self.init_buff_logger('Buff.'+self.buff_stack[-1].name,'./tmp/'+self.buff_stack[-1].name+'_buff.log')
                            self.buff_stack[-1].logger.setLevel(logging.INFO)
                            self.buff_stack[-1].logger.info(self.buff_stack[-1].cmt)
                            self.activated_buff.append(i)

                        else:
                            if len(data[wp]['special'][i][1])!=0:
                                self.main_logger.info("加载 1类 {} {} {} ".format(data[wp]['name'],"武器效果",data[wp]['special'][i][2]))
                                self.load_att(data[wp]['special'][i][1])
                                self.activated_buff.append(i)
                break
        assert(found)
        # if not(found):
        #     raise WeapnNotFoundError

    def load_articraft_effect(self,name):
        
        path ="./data/articraft_effects.json"

        with open(path, 'r', encoding='UTF-8') as fp:
            data = json.load(fp)
        found = False
        
        for wp in data:
            if wp == name:
                found = True
                self.equipment.append(data[wp]['name'])

                '''加载激活的buff'''
                for i in data[wp]['special'].keys():
                        if len(data[wp]['special'][i][0])!=0:
                            self.main_logger.info("加载 2类 {} {} {} ".format(data[wp]['name'],"圣遗物效果",data[wp]['special'][i][2]))
                            self.add_buff(Buff(data[wp]['special'][i][0],data[wp]['special'][i][1],"{}_{}".format(data[wp]['name'],"圣遗物效果"),data[wp]['special'][i][2]))
                            self.buff_stack[-1].logger = self.init_buff_logger('Buff.'+self.buff_stack[-1].name,'./tmp/'+self.buff_stack[-1].name+'_buff.log')
                            self.buff_stack[-1].logger.setLevel(logging.INFO)
                            self.buff_stack[-1].logger.info(self.buff_stack[-1].cmt)
                            self.activated_buff.append(i)

                        else:
                            if len(data[wp]['special'][i][1])!=0:
                                self.main_logger.info("加载 1类 {} {} {} ".format(data[wp]['name'],"圣遗物效果",data[wp]['special'][i][2]))
                                self.load_att(data[wp]['special'][i][1])
                                self.activated_buff.append(i)
                break
        assert(found)
        # if not(found):
        #     raise WeapnNotFoundError

    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------

    def damage_output(self,ans,atk_type,ele,ctl=False):
        assert(isinstance(ans,dict))
        atk = deepcopy(self.attack)
        
 
        for i in ans:
            if i in self.att_name:
                atk[self.att_name.index(i)]+=ans[i]
            else:
                pass
        
        #第一乘区
        area1 = atk[0]*(1+atk[1]/100)+atk[2]
        #第二乘区
        if self.attack[3]>100:#暴击率不超过1
            area2 = 1 + 1*atk[4]/100
        else:
            area2 = 1 + atk[3]/100*atk[4]/100
        #第三乘区
        if ele != 'physic':
            area3 = 1 + atk[5]/100
            
            if ctl:
                self.dlogger.debug("----------------------{}---------------------------".format(atk_type))    
                self.dlogger.debug(ans)
                self.dlogger.debug("现有第一区{} 最终第一区{}".format(self.attack[0:3],atk[0:3]))
                self.dlogger.debug("现有第二区{} 最终第二区{}".format(self.attack[3:5],atk[3:5]))
                self.dlogger.debug("现有第三区{:.2f}".format(area3))

            for i in ans:
                if i in ['ed','alld',atk_type]:
                    area3 += ans[i]/100
        else:
            area3 = 1
            if ctl:
                self.dlogger.debug("----------------------{}---------------------------".format(atk_type))    
                self.dlogger.debug(ans)
                self.dlogger.debug("现有第一区{} 最终第一区{}".format(self.attack[0:3],atk[0:3]))                
                self.dlogger.debug("现有第二区{} 最终第二区{}".format(self.attack[3:5],atk[3:5]))
                self.dlogger.debug("现有第三区{:.2f}".format(area3)) 
                   
            for i in ans:    
                if i in ['alld',atk_type]:                
                    area3 += ans[i]/100
        
        if ctl:
            self.dlogger.debug("最终第三区{:.2f}".format(area3))
            self.dlogger.debug("无倍率期望输出 {:.2f}".format(area1*area2*area3))
        

        return(area1*area2*area3)


    #===============================================================================================
    def check_e_time_out(self):
        # if self.skill[atk_typ]['n']>1 and time_out(env)
        #  self.acc[atk_type]=0
        pass

    def generic_atk(self,atk_type,env,logger = None):

        if isinstance(logger,logging.Logger):
            logger.debug('----------------{}开始({:.2f})--------------------'.format(atk_type,env.now()))

        self.acc[atk_type] = self.acc.get(atk_type,0)
        N = 1
        ele=0
        s=0

        ans=dict()
        activate_evnts = ['hitted','auto']
        activate_evnts.append(atk_type)
        chckout_evnts = ['auto']
        chckout_evnts.append(atk_type)


        for i in self.buff_stack:

            i.logger.info("********  attack {} ({}) ***********".format(atk_type,env.now()))
            i.activate(activate_evnts,env)
            ans_one = i.checkout(chckout_evnts,env)

            for j in ans_one:
                ans[j] = ans.get(j,0)+ans_one[j]
                if j == 'enchant' and ans_one[j] == 1:
                    ans[j] == 1 #没加入切换角色前只能自属性附魔


        if atk_type=='a': # 平A注意速度和附魔
            speed = ans.get('speed',0)
            if ans.get('enchant',0) == 1:
                ele = self.elem_class
            else:
                ele = self.atk_elem(atk_type)
            
        else:
            speed = 0
            ele = self.atk_elem(atk_type)
        

        D=self.damage_output(ans,atk_type,ele,True) #计算总伤害

        if self.acc[atk_type]==self.skill[atk_type][0]: # 如果多段攻击已经累积数目达到最大重置计数
            self.acc[atk_type]=0


        self.acc[atk_type] +=1
        pos = self.acc[atk_type]-1

        ratio = self.skill[atk_type][1][pos] #读取倍率
        lapse = 1/((1/self.skill[atk_type][2][pos])*(1+speed/100))#计算消耗时间，平a计入攻速考虑
        D = D*ratio/100

        if self.acc[atk_type] == 1: #对于多段攻击，只有初始时候激发cd,参考姥爷 e 3段数， 平a目前不影响，因为cd=0
            if atk_type in ['q','a']:
                self.next_atk[atk_type] = env.add(self.skill[atk_type][3])
            if atk_type in ['e']:#没有测试，累积e
                if self.multiple_e > 1:
                    self.next_atk['e'] = self.e_save.pop(0)
                    self.e_save.append(env.add(self.skill[atk_type][3]))
                else:
                    self.next_atk['e'] = env.add(self.skill[atk_type][3])

        # if atk_type in ['e']:
        # logger.info("{} {} {}".format(self.next_atk[atk_type],self.acc[atk_type],self.skill[atk_type][3]))




        # 平A多攻速输出
        if (atk_type!='a'):
            logger.info("{} {}计数: {},start: {:.2f} ,冷却到期:{:.2f}, {} D= {:.2f} 倍率 {:.2f} 消耗时间 {:.2f} ".format(self.name,atk_type,self.acc[atk_type],env.now(),self.next_atk[atk_type],ele,D,ratio,lapse))

        else:
            logger.info("{} {}计数: {},start: {:.2f} ,冷却到期:{:.2f}, {} D= {:.2f} 倍率 {:.2f} 消耗时间 {:.2f}  攻速: {}".format(self.name,atk_type,self.acc[atk_type],env.now(),self.next_atk[atk_type],ele,D,ratio,lapse,speed))

        self.last_atk[atk_type] = env.now()
        env.tick(lapse) #环境时间更新，迭代量为技能时间
        self.dmg[['a','h','e','q'].index(atk_type)]+=round(D,2)
        if ele == 'physic':
            self.dmg2[0]+=round(D,2)
        else:
            self.dmg2[1]+=round(D,2)
        # '''TODO a 释放完超过一定时间多段攻击会被重置         '''
        if atk_type=='q':
            self.acc['a'] = 0
            logger.info("q 重置 a 计数")
        if atk_type=='e' and self.skill['e'][4] == 'yes': #e的skill属性里检查是否要重置a段数，diluc 6命有用
            self.acc['a'] = 0
            logger.info("e 重置 a 计数")
        # '''姥爷3段e,每一段之间空档期有限制，没有编入程序'''
        return()

    def atk_ready(self,env,alist,mode=1):
        for i in alist:
            if mode == 1:
                if self.acc[i] < self.skill[i][0]: #这个不对
                    return True
            if env.now()>=self.next_atk[i]:
                return True
            else:
                pass
        return False

    def atk_elem(self,atk_type):
        if self.skill[atk_type][4] == 'elem':
            return self.elem_class
        else:
            return "physic"