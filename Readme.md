## 原神伤害模拟器

------------------

现有人物数据 : diluc

完成部分:

1. diluc 各项效果校对
2. diluc 伤害重写及调试
3. 武器信息加载
4. 圣遗物信息加载
5. 人物攻击序列校对，空白用a补充
6. 人物信息增加强制保证技能间隔（四命使用）



待完成：

Buff对象重新梳理





使用说明：

直接运行主程序 main.py

结果为主目录 main.log 以及/datat文件夹下各buff的log



```python
    cycle = 10
    diluc = character(6,6,logger)
    a = Articraft()
    
    diluc.load_from_json("./data/diluc.json")
    diluc.load_weapon_from_json("./data/claymore.json","lm")
    a.load_json("./data/articraft.json")

```

主程序需要设定位置

cycle = 攻击序列循环次数

character(技能等级，命座（1-6），logger)

diluc.json 人物信息json

------------------------

### 结果

迪卢克 6命 6技能等级(1精炼狼末不触发第二特效)
攻击序列 "eaaeaaeaaq",无魔女效果dps 2.16w, 有魔女4效果2.87w，满狼末3.08w, 满狼末(默认触发第二特效)3.42w,0命有魔女1.93w。
攻击序列q+3(eaaaa)有大就放dps 2.95w

2.87w 200s 伤害组成 普攻 287w,e 109w, q 178w, 按物理元素分 物理 6w,元素 568w

### 链接

  易用型全功能配装模拟器（https://bbs.mihoyo.com/ys/article/3218704）基于15s模型的excel版模拟器，比较方便使用，数据比较全

