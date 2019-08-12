### 效果演示

![SVID_20190810_010334_1.gif](Chatbot\asset\SVID_20190810_010334_1.mp4.gif)





### 项目说明

- 本项目为用于查询股票相关信息的微信智能对话机器人
- 该对话机器人旨在利用微信，使得用户能够随时随地对股票的特定信息进行查询，并进行买进卖出的交易
- 智能对话机器人能够实现功能：
  - 日常问候
  - 输入电话号码登入交易系统
  - 回复股票的 最新价格、最新持有量、52周内最高价格 三种信息
  - 输入账号进行交易
  - 买进或卖出具体数量的股票

### 使用方法

- 使用pycharm等python编辑工具，运行main.py程序
- 跳出二维码后，用手机扫描，登录网页版微信（部分账号无法登陆，可通过其他账号尝试）
- 登录完成后，使用其他账号给已登录账号发送消息，即可开始与机器人的交互

### 重要函数库

- numpy 1.17.0
- rasa_nlu 0.15.1
- requests 2.22.0
- spacy 2.1.7
- spacy-model-en_core_web_md 2.1.0
- sklearn-crfsuite 0.3.6
- wxpy 0.3.9.8

### 文件结构信息

- config_spacy.yml 为定义spacy调用model与pipline的文件
- demo-rasa-noents.json 为自定义语义识别训练集（可自行添加）
- itchat.pkl与wxpy.pkl 为微信集成库
- main.py 则包括进行微信只能回复的全部代码，其中各个模块有具体注释
- 内有总结报告与视频演示
