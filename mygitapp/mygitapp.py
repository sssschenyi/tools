# import linecache
import difflib
import sqlite3
import datetime
import os
import sys
import hashlib
import mygitappinit
#递交单个文件到数据库
databasefile = os.path.isfile(os.getcwd()+"\.mygitapp\mygit.db")
if databasefile:
	con = sqlite3.connect(os.getcwd()+r'\.mygitapp\mygit.db')
	# con = sqlite3.connect(r'F:\pythonCode\py3.7-code\mygitapp\.mygitapp\mygit.db')
	content_tablename = 'file_content'
	cur=con.cursor()
# elif not folder:
else:
	# help()
	print("Tips: not a mygitapp repository (Please use init command): .mygitapp")



#生成sha1
def comm_id():
	mytime = datetime.datetime.now()
	mytime = str(mytime)
	myt = bytes(mytime, encoding='utf-8')
	commit_id = hashlib.sha1(myt).hexdigest()
	return commit_id

# 把文件递交到数据库
def commit(getcommitfilename):
	try:
		fo = open(getcommitfilename, 'r',encoding='UTF-8')# encoding='UTF-8')
		line = fo.readlines()#读取文件全部行
		# print(list(line))
		sor_text = ''.join(line)#连接全部
		# print("sor_text",sor_text)
		commit_id = comm_id()#调用 comm_id 函数
		sum_list_id=len(list(line))#get 文件 总行数
		# print("sum_list_id ",sum_list_id)
		sum_byte=len(sor_text)#get 文件 字节 数
		# print("sum_byte ",sum_byte)
		nowdatetime  =datetime.datetime.now()#当前年月日时分秒
		filepath = os.getcwd()+"\\"+getcommitfilename #生成全路径
		sql = '''insert into file_content (commit_id,original_content,filepath,sum_list_id,update_time) 
		values(?,?,?,?,?)'''
		value = (commit_id,sor_text,filepath,sum_list_id,nowdatetime)
		cur.execute(sql, value)#这种格式可以防止特殊字符出错,可以插入代码文件
		con.commit()
	except OSError:
		# print('cannot open',getcommitfilename)
		print("ERROR:'",getcommitfilename,"' 与任何文件不匹配")
	else:
		fo.close()

#从数据取出数据并且写入到文件
def reset(com_id):
	selectsql = '''select original_content,filepath from file_content where commit_id like '{}%' '''.format(com_id)
	data= cur.execute(selectsql)
	for row in data:
		original_content = row[0]
		filepath = row[1]
		print("filename",filepath)
		filename = os.path.basename(filepath)
	fo = open(filename, "w+", encoding='UTF-8')
	print("文件名为: ", fo.name)
	# 用 fetchone()  和 fetchall 取回数据的是 元组 类型
	fo.write(original_content)
	fo.close()

def log():
	selectsqllog = '''select commit_id,filepath,update_time from file_content '''
	selectsqlcount = '''select count(*) from file_content'''
	logdata = cur.execute(selectsqlcount)
	# print(type(logdata))
	commit_sum = cur.fetchone()[0]
	print("递交的文件共有:",commit_sum,"个")

	if commit_sum <= 0:
		# print(len(commit_id_all))
		print("版本库是干净的,你还没有提交任何文件")		
	elif commit_sum >= 1:
		# print(len(commit_id_all))
		for row in cur.execute(selectsqllog):
			commit = row[0]
			filepath = row[1]
			uptatetime = row[2]
			filename=os.path.basename(filepath)
			print("commit:",commit)
			print("filename:",filename)
			print("modiffdate:",uptatetime)
			print("")

def status():
	print("扫描那些文件更新过")

def help():
	print("help command show help----查看所有帮助")
	print("reset [commit_id]----恢复到某个id版本")
	print("commit [filename] -m[]----递交单个文件到数据库")
	print("version command show version----查看当前版本号")
	print("log command show commit ver----查看递交的版本号")

def version():
	ver = "1.0.0"
	print(ver," author:https://github.com/sssschenyi")

while True:
	try:
		print("")
		print("mygitapp---",os.getcwd())
		getshell = input("mygitapp>>> ")
		folder = os.path.exists(os.getcwd()+"\.mygitapp") 
		shell = getshell.split(" ",1)#把getshell命令转换成长度是2位列表
		#判断结果
		if not folder:
			print("not a mygitapp repository (Please use init command): .mygitapp")
			if shell[0] == "init":
				mygitappinit.init()
		else:
			if shell[0] =="":
				print(end="")
			elif shell[0] == "init":
				mygitappinit.init()
			elif shell[0] == "help" or shell[0] == "?":
				help()
			elif shell[0] == "log":
				log()
			elif shell[0] == "commit":
				# 判断 commit 是否带参数了
				if len(shell) == 1:
					print("ERROR:commit 参数不能为空")	
				else:
					commit(shell[1])
			elif shell[0] == "version":
				version()
			elif shell[0] == 'reset':
				if len(shell) == 1:
					print("ERROR:reset 参数不能为空")	
				else:
					reset(shell[1])
			else:
				print("'",shell[0],"' is not a mygitapp command. See 'help'.")

	except KeyboardInterrupt as e:
		print("\nctrl +c 接收键盘中断，退出")
		sys.exit(1)

cur.close()
con.close()
