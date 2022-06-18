import os
import time
# import update_findFile_to_databases

###############
#查找本地文件的应用
#功能：
#文件全名查找，文件名模糊查找，后缀名查找，创建日期查找
#遍历文件插入数据库，从数据库查找。数据库每天下午5点auto更新
###############



'''
def get_file_path(root_path,findstr):
    for curDir, dirs, files in os.walk(root_path, topdown=True):    
        # print("现在的目录：" + curDir)
    #False
    #print("该目录下包含的子目录：" + str(dirs))
    # print(dirs)
        for dir in dirs:
            fullpath = os.path.join(curDir,dir)    
            if fullpath.find(findstr) >=0:
                print(" <DIR>",fullpath)
        for file in files:
            fullpath = os.path.join(curDir,file)    
            if fullpath.find(findstr) >=0:
                print(" <FILE>",fullpath)
    #print("该目录下包含的文件：" + str(files))
 '''   
def find_dir(root_path,findstr):
    for curDir, dirs, files in os.walk(root_path, topdown=True):    
        for dir in dirs:
            if dir.find(findstr) >=0:
                print(" <DIR>",os.path.join(curDir,dir)) 
       
  

def find_file(root_path,findstr):
    for curDir, dirs, files in os.walk(root_path, topdown=True):    
        for file in files:
            if file.find(findstr) >=0:
                showFile = os.path.join(curDir,file)
                # 获取文件最后修改时间
                xiugaitime = time.strftime("%Y-%m-%d %H:%M",time.gmtime(os.path.e(showFile)))
                print(xiugaitime,end='')
                print(" <FILE>",showFile)

def find_suffix(root_path,findstr):
    for curDir, dirs, files in os.walk(root_path, topdown=True):
        #print("files",files)
        for file in files:
            #os.path.splitext(file)[1] 提取file 的后缀名 suffix
            if os.path.splitext(file)[1] == findstr:
                showFile = os.path.join(curDir,file)
                # 获取文件最后修改时间
                xiugaitime = time.strftime("%Y-%m-%d %H:%M",time.gmtime(os.path.getmtime(showFile)))
                print(xiugaitime,end='')
                print(" <FILE>",showFile)

    


                
def help():
    print("help               查看所有帮助")
    print(r"find -f str       查找文件")
    print(r"find -d str       查找文件夹")
    print(r"updatedb          更新文件数据库")
    print(r"find -s str       根据后缀名查找")
    print("version            查看当前版本号")

def version():
	ver = "1.0.0"
	print(ver," author:https://github.com/sssschenyi")    
    
    
if __name__ == "__main__":
    while True:
        # findstr = input("请输入文件名:")
        #根目录路径
        # root_path = r"F:\pythonCode\py3.7-code\my_Translator"
        root_path = "F:\\"
        findstr = input(">>>")
        command = findstr.split(" ",3)
        if command[0] == "help":
            help()
        elif command[0] == "version":
            version()
        elif command[0] == "updatedb":
            pass
        elif command[0] == "find":
            if command[1] == "-d":
                if command[2] != " ":
                    #print(type(command[2]))
                    find_dir(root_path,command[2])
            elif command[1] == "-f":
                if command[2] != " ":
                    find_file(root_path,command[2])
            elif command[1] == "-s":
                if command[2] != " ":
                    find_suffix(root_path,command[2])
            else:
                print("命令输入有误")
        else:
            print("没有这个命令")