# author: chenyi
# ide: notepad++
# date: 22:26 2022/10/11

#返回子字符串在字符串中出现的次数。
def fun():
    s = "this is string example he"
    sub ="x" # 查找的字符
    # 调用函数只需要更改上面 2 个变量
    
    ### 下面不用改
    n = 0
    for i in s:
        if sub == i:
            n += 1
    return n

# 查找单纯出现的次数
        
    
if __name__ == '__main__':
    print(fun())
