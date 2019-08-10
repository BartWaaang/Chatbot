# 关键库引用
from rasa_nlu.training_data import load_data
from rasa_nlu.config import RasaNLUModelConfig
from rasa_nlu.model import Trainer
from rasa_nlu import config
import requests
import random

# 引用训练集
trainer = Trainer(config.load("config_spacy.yml"))
training_data = load_data('demo-rasa-noents.json')
interpreter = trainer.train(training_data)

# 特定回复语句
keywords = {
            'greet': ['hello:)', 'hi:)', 'hey:)', 'nice yo meet you:)'],
            'thankyou': ['thank', 'thx'],
            'goodbye': ['bye :)', 'farewell :)', 'see you later:)']
           }



responses = ["I'm sorry :( I couldn't find anything like that",
             '{} is a great hotel!',
             '{} or {} would work!',
             '{} is one option, but I know others too :)']


# 股票名称获取
def get_stock(message):
  entities = interpreter.parse(message)["entities"] #实体获取
  params = {}
  if len(entities)!=0:
     for ent in entities:
       params[ent["entity"]] = str(ent["value"])
     return params['stock']
  else:
      return None

# 股票信息获取
def stock_info(stock, type):
    start = 'https://cloud.iexapis.com/stable/stock/'
    end = '/quote?token=pk_5b4b75ef0e6c4d6c9bbf32925604b841'
    Stock = stock
    r = requests.get(start + Stock + end)#api获取数据
    dic = r.json()
    return dic[type]


# 语句理解
def interpret(message):
    data = interpreter.parse(message)#训练后语义获取
    return data



# 状态表建立

INIT=0   # 状态定义
AUTHED=1
CHOOSE_STOCK=2
ASKING=3
AUTHED2=4
BUYING=5
SELLING=6
ORDERED=7
TRADE=8

policy_rules = {
    (INIT, "greet"):(INIT, random.choice(keywords['greet']), None),
    (INIT, "goodbye"): (INIT,random.choice(keywords['goodbye']), None),
    (INIT, "first_ask"): (INIT, "Hi, i'm a chatbot to help you get information about stock market",None),
    (INIT, "stock_search"): (INIT, "Sorry :(, you have to log in first, may i have your phone number please?", AUTHED),
    (INIT, "number"): (AUTHED, "Welcome back!",None),
    (AUTHED, "stock_search"): (ASKING, "Well, which stock are you interested in?", None),
    (ASKING, "stock_search"): (ASKING, "What information do you want to know?", None),
    (ASKING, "latestprice_search"): (ASKING, "Got it! Its latest price is", None),
    (ASKING, "latestvolume_search"): (ASKING, "Well, its latest price is", None),
    (ASKING, "week52high_search"): (ASKING, "OK, its highest price in 52 weeks is", None),
    (ASKING, "change_ask"): (ASKING, "Sure, what else do you want to know", None),
    (AUTHED, "goodbye"): (INIT,random.choice(keywords['goodbye']), None),
    (ASKING, "goodbye"): (INIT,random.choice(keywords['goodbye']), None),
    (ASKING, "buy_stock"): (ASKING,"No problem, may i have your account please?", AUTHED2),
    (ASKING, "sell_stock"): (ASKING,"No problem, may i have your account please?", AUTHED2),
    (ASKING, "number"): (AUTHED2, "Welcome back!", None),
    (AUTHED2, "buy_stock"): (BUYING, "So how many do you want to buy?", None),
    (AUTHED2, "sell_stock"): (SELLING, "So how many do you want to sell?",None),
    (BUYING, "number"): (ORDERED, "Alright, the trade is finished, remember to check your account :)", None),
    (SELLING, "number"):(ORDERED, "Alright, the trade is finished, remember to check your account :)", None),
    (ORDERED, "goodbye"): (INIT,random.choice(keywords['goodbye']), None),
    (ORDERED, "stock_search"):(ASKING, "What information do you want to know?", None),
    (ORDERED, "buy_stock"): (BUYING, "So how many do you want to buy?",None),
    (ORDERED, "sell_stock"):(SELLING, "So how many do you want to sell?", None)

}


# 回复函数建立
stock_all=[]


def send_message(state, pending, message, answer):

    if get_stock(message)!=None:            #股票名存储
        stock_all.append(get_stock(message))
    if len(stock_all) == 0:
        stock = None
    else: stock =stock_all[-1]
    data = interpret(message)
    print("USER:{}".format(message))
    new_state, response, pending_state = policy_rules[(state, interpret(message)["intent"]["name"])]
    print("BOT:{}".format(response))
    answer.append(response)   #回复消息存储


    if pending is not None:
        new_state, response, pending_state = policy_rules[pending]
        print("BOT:{}".format(response))
        answer.append(response)
        pending = None
    if pending_state is not None:
        pending = (pending_state, interpret(message)["intent"]["name"])
    if (new_state == ASKING) & (interpret(message)["intent"]["name"]=="latestprice_search"):
        print("BOT:{}".format(stock_info(stock, 'latestPrice')))
        answer.append(stock_info(stock, 'latestPrice'))
    if (new_state == ASKING) & (interpret(message)["intent"]["name"]=="latestvolume_search"):
        print("BOT:{}".format(stock_info(stock, 'latestVolume')))
        answer.append(stock_info(stock, 'latestVolume'))
    if (new_state == ASKING) & (interpret(message)["intent"]["name"]=="week52high_search"):
        print("BOT:{}".format(stock_info(stock, 'week52High')))
        answer.append(stock_info(stock, 'week52High'))
    return new_state, pending

# 总体回复函数建立
state = INIT  #全局变量建立
pending = None
answer = []

def send_messages(messages):
    global state #通过函数改变全局变量
    global pending
    global answer
    answer = []
    state, pending = send_message(state, pending, messages, answer)





# 微信集成代码
from wxpy import *

bot = Bot(cache_path=True) #定义机器人


sender = bot.search('王宇桁')[0] #特定对象获取


@bot.register()  # 用于注册消息配置
def recv_send_msg(recv_msg):
    print('收到的消息：', recv_msg.text)  # recv_msg.text取得文本
    # recv_msg.sender 就是谁给我发的消息这个人
    if recv_msg.sender == sender:
        print(stock_info("aapl", 'latestPrice'))
        send_messages(recv_msg.text)
        print(len(answer))
        if len(answer) == 1: #回复只有一句则直接回复，两句以上则合并后回复
          ms = answer[-1]
          print(ms)
        if len(answer) >= 2:
          ms = answer[-2] + ' ' +str(answer[-1])
    return ms  # 回复


embed() # 进入交互式的 Python 命令行界面，并堵塞当前线程支持使用 ipython, bpython 以及原生 python







