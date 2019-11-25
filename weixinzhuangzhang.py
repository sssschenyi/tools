import sqlite3
import datetime
import pyttsx3
#pyttsx3 请自行安装,安装命令
#pip install pyttsx3
# 充值到账的声音
def tts(sounddata):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.say("充值成功,您的账户到账"+str(sounddata)+"元")
    engine.runAndWait()
#修改user_journal 数据库,添加now balance字段
#修改test1000 数据库,添加 register_time 字段,查看用户注册和最后登录的时间
#修改查询个人信息为 方法名
#添加 bankJournal 数据库表,类似于银行的数据库接口
# 模仿微信转账
# zhuangzhang 转账功能文件
con = sqlite3.connect(r'F:\pythonCode\py3.7-code\weixinzhuangzhang\Databases.db')
userinfotable     = 'test1000'
userjournaltable  = 'user_journal'
bankjournaltable  = 'bankJournal'
#数据库结构请看weixinzhuangzhang.sql 文件

c=con.cursor()

#打印10条用户数据
def showalluser():
    cursor =c.execute("select id,name,salary,mobileID from '{}' where mobileID != '{}' limit 10 ".format(userinfotable,register_tel))#
    print("id    name    money          mobile")
    for row in cursor:
        print(row[0],"   ",row[1],' ',"余额",round(row[2],2),'    ',row[3])
        #user1Name = row[0]
        #user2Name = row[1]

#打印个人信息
def showotherinfo(getmobileID):
    privateInfo1=c.execute("select id,name,salary from '{}' where mobileID='{}'".format(userinfotable,getmobileID))
    #print("privateInfo1.row[1]",privateInfo1.fetchone()[1])
    shoujihaoshifoucunzai = privateInfo1.fetchall()
    if len(shoujihaoshifoucunzai) == 1:
        for row in privateInfo1:
            print(row[0],"   ",row[1],' ',"余额",round(row[2],2))       
        print("===========全部交易记录===========")
        privateInfo2=c.execute("select create_time,journal,now_balance,name from '{}' where u_id='{}'".format(userjournaltable,getmobileID))
        print("日期:\000用户:","\000帐单")
        for row in privateInfo2:
            # a = round(row[2],2)
            # print("row[2]",type(a))            
            print(row[0][0:19],"\000",row[3],"\000",row[1],"剩余",round(row[2],2))#row[0:19]是切割字符串
    else:
        print("你输入的",getmobileID,"用户不存在")
#设置变量信息
def setuserinfo(get_register_tel,get_register_password):
    global register_tel
    global register_bank_balance
    global register_pay_passoword
    global register_bankcard_id
    global register_username
    global loginOK  
    loginOK = "loginOK"
    global is_login 
    is_login =""    
    user_info=c.execute('''select mobileID,salary,login_password,name,bank_id,login_password from '{}' where mobileID = '{}' and login_password ='{}' '''.
            format(userinfotable,get_register_tel,get_register_password))
    for row in user_info:
        register_tel =   row[0]#获取登陆者电话
        register_bank_balance = row[1]#获取登陆者余额
        register_pay_passoword = row[2]#获取登陆者支付密码 
        register_username =row[3]#获取登陆者的名字
        register_bankcard_id = row[4]#获取登陆者银行卡号
        register_login_password = row[5]#获取登陆者登陆密码
        is_login = loginOK #登陆ok

# 转账函数
def zhuanzhang(getothermobileID):
    global otherpartyName
    global otherpartyMoney
    global othermobileID
    global register_bank_balance
    checkID = c.execute("select name,salary,mobileID from '{}' where mobileID={}".format(userinfotable,getothermobileID))
    #设置变量
    for row in checkID:                            
        otherpartyName = row[0] #otherpartyName 对方的名字
        otherpartyMoney = row[1]  #otherpartyMoney 对方账户的钱
        othermobileID = row[2] #otherparty 对方id
        #print("otherpartyName",otherpartyName)
        #print("othermobileID",othermobileID)
    if int(getothermobileID) == register_tel:
        print("++++++++++++")
        print("不能给自己转账")
        print("++++++++++++")
    elif int(getothermobileID) == othermobileID:
        GETzhuangzhangjine = input("输入转账金额: ")
        GETzhuangzhangjine = float(GETzhuangzhangjine)
        #if float(GETzhuangzhangjine):
        #修改转账金额能精确到分
        if GETzhuangzhangjine > 0:
            zhuangzje = round(GETzhuangzhangjine,2)
            print('你输入的金额被四舍五入:￥',(zhuangzje))
            print("register_bank_balance",register_bank_balance)
            if zhuangzje <= register_bank_balance :
                register_bank_balance -= zhuangzje
                otherpartyMoney += zhuangzje
                zhuanzhangMoney = str(zhuangzje)
                fukuan     = '付款给'
                laizi      = '来自'
                #datetime.datetime.now() #当前年月日时分秒
                fukuanJournal = fukuan+str(otherpartyName)+'-'+zhuanzhangMoney
                laiziJournal  = laizi +str(register_username)+'+'+zhuanzhangMoney 
                #print("zhuangzje :",zhuangzje)
                print(register_username,"的余额:",round(register_bank_balance,2))
                print(otherpartyName,"的余额:",round(otherpartyMoney,2))
                c.execute(" update '{}' set salary={} where mobileID={} ".format(userinfotable,register_bank_balance,register_tel))
                c.execute(" update '{}' set salary={} where mobileID={} ".format(userinfotable,otherpartyMoney,othermobileID))
                #插入付款记录
                c.execute("insert into '{}'(u_id,name,create_time,journal,now_balance) values('{}','{}','{}','{}','{}')".format(userjournaltable,register_tel,register_username,datetime.datetime.now(),fukuanJournal,register_bank_balance))
                #插入来自收款的记录
                c.execute("insert into '{}'(u_id,name,create_time,journal,now_balance) values('{}','{}','{}','{}','{}')".format(userjournaltable,othermobileID,otherpartyName,datetime.datetime.now(),laiziJournal,otherpartyMoney))
                con.commit()
                print("++++++++++++++")
                print("    转账成功  -_-")
                print("++++++++++++++")
                #showalluser()
            else:
                print("+++++++++++++++++++++++++++")
                print("转账失败,转账金额不能大于余额,当前余额:",register_bank_balance)
                print("+++++++++++++++++++++++++++")
        else:
            print("输入转账金额错误")
    else:
        print("++++++++++++++")
        print("收款人ID不存在")
        print("++++++++++++++")

# 提现函数
def tixian(get_tixian_money):
    global register_bank_balance
    get_tixian_money = float(get_tixian_money)
    if get_tixian_money > register_bank_balance :
        print("提现金额不能大于本金")
    elif get_tixian_money <= 0 :
        print("提现金额不能少于本金")
    elif get_tixian_money <= register_bank_balance and get_tixian_money >0 :
        register_bank_balance -= get_tixian_money#自己的社交账户减去提现金额
        # otherpartyMoney += get_tixian_money#自己的银行账户增加提现的金额
        c.execute(" update '{}' set salary={} where mobileID={} ".format(userinfotable,round(register_bank_balance,2),register_tel))
        
        #往bankJournal表里插入提现的记录 
        #这里提现金额是不能和银行同步的,权限的问题,需要写个触发器同步数据,银行才能看到数据       
        tixianJournal = "提现"
        c.execute("insert into '{}' (wx_mobile_id,user_bank_id,name,draw_amount,create_time,journal) values('{}','{}','{}','{}','{}','{}')".
            format(bankjournaltable,register_tel,register_bankcard_id,register_username,round(get_tixian_money,2),datetime.datetime.now(),tixianJournal))
        print("提现成功")
        #往user_journal表里插入提现日志记录.
        strtixian = str(get_tixian_money)
        tixianJournal = "提现"+ strtixian
        c.execute("insert into '{}'(u_id,name,create_time,journal,now_balance) values('{}','{}','{}','{}','{}')".
            format(userjournaltable,register_tel,register_username,datetime.datetime.now(),tixianJournal,round(register_bank_balance,2)))
        con.commit()

#menu 功能
def showmenu():
    print("=======欢迎'{}'微信转账信息查看系统========".format(register_username))
    print("    menu-菜单")
    print("    1:转账")
    print("    2:查看全部好友信息")
    print("    3:查看其他用户信息")
    print("    4:充值")
    print("    5:提现")
    print("    6:查看我的信息")
    print("    886:退出")

#============
login = True
while login:
    print("     菜单")
    print("    1:注册微信")
    print("    2:我要登陆")#
    getloginmenu = input("请选择菜单功能:")
    getloginmenu = int(getloginmenu)
    if getloginmenu == 1 :
        print("register weixin")
        register= {"gettel":"","getlogin_password1":"","getlogin_password2":""}
        register["gettel"] = input("输入电话号码:")
        register["getage"]  = input("输入年龄:")
        regage = int(register["getage"])#转换变量为INT型
        register["getlogin_password1"] = input("密码:")
        register["getlogin_password2"] = input("确认密码:")
        str(register["getlogin_password1"])
        str(register["getlogin_password2"])
        regtel=len(register["gettel"])
        if regtel != 11:
            print("手机号输入有误")             
        elif regage < 0 or regage > 150 :
            print("年龄输入有误")
        elif register["getlogin_password1"] != register["getlogin_password2"]:
            print("确认密码输入不一致")
        else :
            li = list(register.values())#转换字典成列表           
            if all(li):                
                print(li)
                #插入用户注册的信息和注册日期
                c.execute('''insert into '{}'(mobileID,age,login_password,register_time,salary) 
                    values('{}','{}','{}','{}','{}')'''.
                    format(userinfotable,
                    register["gettel"],
                    register["getage"],                
                    register["getlogin_password2"],
                    datetime.datetime.now(),
                    0 #设置注册默认金额为 0 
                    ))
                con.commit()
                login = False #注册成功,退出while 循环
            else:
                print("注册失败,有空值")
    elif getloginmenu == 2 :
        print("my login weixin")        
        get_register_tel = input("请输入手机号:")#获取登陆者wei xin
        get_register_password = input("请输入登陆密码:")
        setuserinfo(get_register_tel,get_register_password)
        if is_login == loginOK:
            print("login ok") 
            #更新用户登陆的日期
            c.execute('''update '{}' set the_login_time = '{}' where mobileID ='{}'
                    '''.
                    format(userinfotable,
                    datetime.datetime.now(),
                    get_register_tel                  
                    ))
            con.commit()  
            while True:
                try:
                    setuserinfo(get_register_tel,get_register_password)
                    showmenu()
                    getmenu = input("请选择菜单功能:")
                    getmenu = int(getmenu)
                    if getmenu == 1 :
                        print('=============开始转账===============')
                        print('当前用户:{},微信余额:{}'.format(register_username,register_bank_balance))
                        getothermobileID = input("输入对方的手机号开始转账:")# 收款人手机号
                        zhuanzhang(getothermobileID) # start zhuanzhang
                    elif getmenu == 2 :
                        showalluser()            
                    elif getmenu == 3 :
                        getmobileID=input("输入手机号开始查找...: ")
                        showotherinfo(getmobileID)   
                    elif getmenu == 4 :
                        print("充值") 
                        print(type(register_bankcard_id))
                        if register_bankcard_id:
                            print("start money 开始充值")
                            get_money = input("请输入金额:")
                            cz_journal= "来自银行卡充值+"+get_money
                            #print("float(round(get_money",float(round(get_money,2)))
                            chongzhi_newmoney=register_bank_balance + float(get_money)#更新余额
                            c.execute('''update '{}' set salary={} where mobileID = '{}'; '''.
                                format(userinfotable,round(chongzhi_newmoney,2),register_tel))
                            #插入日志
                            c.execute("insert into '{}'(u_id,name,create_time,journal,now_balance) values('{}','{}','{}','{}','{}')".
                                format(userjournaltable,register_tel,register_username,datetime.datetime.now(),cz_journal,round(chongzhi_newmoney,2)))
                            con.commit()
                            print("充值成功...请重新 login 查看")
                            tts(get_money)#开始播放语音
                            showmymoney=c.execute("select name,salary from '{}' where mobileID='{}'".format(userinfotable,register_tel))
                            for row in showmymoney:
                                print("昵称:",row[0],' ',"余额",round(row[1],2))
                        else:
                            print("请绑定bankcard_id")
                            get_user_bankcard_id = input("请输入银行卡号:")
                            #开始绑定银行卡
                            c.execute('''update '{}' set bank_id={} where mobileID = '{}'; '''.
                                format(userinfotable,get_user_bankcard_id,register_tel))
                            con.commit()
                        #if register_bankcard_id 
                    elif getmenu == 5 :
                        get_tixian_money=input("输入提现金额:")
                        tixian(get_tixian_money)
                    elif getmenu == 6 :
                        #打印我的个人信息
                        showotherinfo(register_tel)       
                    elif getmenu == 886:
                        print("Bye-bye")
                        break
                    else:
                        print("菜单命令输入错误")

                except Exception as e:
                    print(e)
                    print("++++++++++++++")
                    print("你输入ID不对")
                    print("++++++++++++++")
                finally:
                    pass

        else:
            print("手机号或密码不对")
    else:
        print("命令输入非法")
#==========

c.close()
con.close()
