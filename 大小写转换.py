# author: chenyi
# ide: notepad++
# date: 13:18 2022年10月11日

#转换成大写
def upstr():
    a = "hello chenyi"
    new = ''
    # a=97,z=122, A=65,Z=90
    for i in a :
        if(ord(i) >=97 and ord(i)<=122):
            new += chr(ord(i)-32)
        else:
            new += chr(ord(i))            
    print(a,'转换后:',new)
    
    
# 转换成小写
def lowstr():
    a = "HELLO CHENYI"
    new = ''
    # a=97,z=122, A=65,Z=90
    for i in a :
        if(ord(i) >=65 and ord(i)<=90):
            new += chr(ord(i)+32)
        else:
            new += chr(ord(i))
    # return a,'转换后:',new
    print(a,'转换后:',new)

#单词首字符转换成大写
def strToUp():
    a = "welcome my red wolrd chenyi"
    # a = 'Bing helps you turn information into action,'
    ali = a.split( )
    new = ''
    # a=97,z=122, A=65,Z=90
    for i in ali:
        if(ord(i[0]) >=97 and ord(i[0])<=122):
            new += chr(ord(i[0])-32)
            new += i[1:]+' '
        else:
            new += chr(ord(i[0]))  
            new += i[1:]+' '
    # return a,'转换后:',new
    print(a,'转换后:',new)
    
if __name__ == '__main__':
    upstr()
    lowstr()
    strToUp()