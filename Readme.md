## 原神伤害模拟器

------------------

现有人物数据 : diluc

完成部分:

1. diluc 各项效果校对
2. 人物攻击序列校对，空白用a补充



待完成：

1. 伤害数值重写
2. 圣遗物信息加载

--------

使用说明：

直接运行主程序 Gmi_v1.2.py

结果为主目录 main.log 以及/datat文件夹下各buff的log



```python
  env.set_endtime(20)

  diluc = character(6,6,logger)

  diluc.load_from_json("./data/diluc.json"）
```

主程序需要设定位置

set_endtime(结束时间)

character(技能等级，命座（1-6），logger)

diluc.json 人物信息json

------------------------

2020/12/16 : 加入可累积e的部分，加入人物动作序列，空白阶段平A补充，输出主日志,修正时间轴更新位置，加入git版本控制