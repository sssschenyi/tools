# author: chenyi
# ide: notepad++
# date: 13:18 2022年10月11日

#返回一个指定的宽度 width 居中的字符串
# 对应的内置函数是 center()
def strcenter():
    s = 'aab'
    fillchar = '*' # 填充的字符
    width=8 # 字符的总宽带
    # 调用函数只需要更改上面 2 个变量
    ### 下面不用改
    start = (width - len(s)) // 2 # // 这个除法能取整
    newstr = ''
    a = 0
    while a <= width:
        newstr += fillchar
        a += 1
        if len(newstr) >= width:
            break
        if start == a:
            for i in s:
                newstr += i
                a += 1
    return newstr
 
 
# 检测字符串是否由字母和数字组成。 
def isstrnum():
    a = "1hello1212”"
    # 调用函数只需要更改上面 a 变量
    ### 下面不用改    
    l = len(a)
    n = 0
    for i in a :
        if n == l:
            n += 1
            break
        new_i = ord(i)
        if new_i >= 97 and new_i <= 122:
            r = True
        elif new_i >= 65 and new_i <= 90:
            r = True
        elif new_i >= 48 and new_i <= 57:
            r = True
        else:
            return False
        
    return r

if __name__ == '__main__':
    print(strcenter())
    print(isstrnum())