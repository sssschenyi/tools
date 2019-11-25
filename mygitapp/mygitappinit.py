import sqlite3
import os
import time

# 字节bytes转化kb\m\g
def formatSize(bytes):
    try:
        bytes = float(bytes)
        kb = bytes / 1024
    except:
        print("传入的字节格式不对")
        return "Error"
    if kb >= 1024:
        M = kb / 1024
        if M >= 1024:
            G = M / 1024
            return "%0.2fG" % (G)
        else:
            return "%0.2fM" % (M)
    else:
        return "%0.2fkb" % (kb)
# 获取文件大小
def getDocSize(path):
    try:
        size = os.path.getsize(path)
        return formatSize(size)
    except Exception as err:
        print(err)


def startgit(path):
    #判断目录是否存在
    #存在：True
    #不存在：False
    folder = os.path.exists(path)
 
    #判断结果
    if not folder:
        #如果不存在，则创建新目录
        # os.makedirs(path, 0755)
        os.mkdir(path)        
        print('初始化成功')
        print('重新启动程序，方便载入数据')
    else:
        #如果目录已存在，则不创建，提示目录已存在
        print('\n版本库已经初始化,数据正在监控...')
        # print(path+'\n版本已经初始化,数据正在监控...')
# startgit(os.getcwd()+"\.mygitapp")#os.getcwd  获得当前目录

    con = sqlite3.connect(os.getcwd()+r'\.mygitapp\mygit.db')
    cur=con.cursor()
    create_table_content = '''CREATE TABLE IF NOT EXISTS "file_content" (
                "id"    INTEGER PRIMARY KEY AUTOINCREMENT,
                "commit_id" text,
                "original_content"  text,
                "filepath"  text,
                "diff_content"  text,
                "diff_list_id"  integer,
                "version_id"    integer,
                "sum_list_id"   integer,
                "update_time"   text
            )'''
    create_table_mygitapp = '''CREATE TABLE IF NOT EXISTS "mygitapp" (
            "file_size" integer,
            "create_file_datetime" TEXT,
            "file_path" TEXT,
            "file_name" TEXT,
            "modif_size" integer,
            "after_modif" TEXT,
            "md5_id" text
            );
            '''
    cur.execute(create_table_content)
    cur.execute(create_table_mygitapp)

    content_tablename = 'file_content'
    
    insertFileInfosql = '''insert into mygitapp (file_path,file_name,file_size,after_modif,create_file_datetime) 
    values(?,?,?,?,?)'''
    selectFileIfosql = '''select file_path from mygitapp;'''


    # 获得所有文件路径
    # file_path(os.getcwd())#os.getcwd()获取当前目录
    # def insert_file_info():
    for root, dirs, files in os.walk(os.getcwd(), topdown=False):
        for name in files:
            allfilename = os.path.join(root, name)#获得文件全路径信息
            # print("allfilename",len(list(allfilename)))
            filename = os.path.basename(allfilename)#获得文件名
            statinfo = os.stat(allfilename)#获得文件的信息数组
            modify_timeArray = time.localtime(statinfo.st_mtime)#最后修改时间
            modify_time = time.strftime("%Y-%m-%d %H:%M:%S",modify_timeArray)#格式化时间
            atimeArray = time.localtime(statinfo.st_atime)#最后访问时间
            atime = time.strftime("%Y-%m-%d %H:%M:%S",atimeArray)#格式化时间
            # print(allfilename,getDocSize(allfilename),modify_time,atime)            
            value = (allfilename,filename,getDocSize(allfilename),modify_time,atime)
            #保存文件信息到数据库
            cur.execute(insertFileInfosql, value)#这种格式可以防止特殊字符出错,可以插入代码文件
            # #更新文件列表
            # filelist = cur.execute(selectFileIfosql)#获取原有的文件信息
            # filelist = list(filelist)#创建一个列表
            # updatefilelist = sorted(set(filelist), key=filelist.index)#去重复
            # for i in updatefilelist:
            #     insert_file_info.value2 = (i,filename,getDocSize(allfilename),modify_time,atime)
            #     cur.execute(insertFileInfosql, insert_file_info.value2)#这种格式可以防止特殊字符出错,可以插入代码文件

    con.commit()
    cur.close()
    con.close()

# insert_file_info()
def init():
    startgit(os.getcwd()+"\.mygitapp")#os.getcwd  获得当前目录

