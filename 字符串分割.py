# author: chenyi
# ide: notepad++
# date: 19:45 2022年10月11日

# 把字符串分割成列表
def strplit():
    s = "this is string example he"
    restr = " "  #指定分隔符对字符串进行切片
    # 调用函数只需要更改上面 2 个变量
    
    ### 下面不用改
    s2 = ''
    new = []
    for i in s:
        # print(i)
        if i != restr:
            s2 += i
        elif i == restr:
            new.append(s2)
            s2 = ''
    new.append(s2)
    return new
    
if __name__ == '__main__':
    print(strplit())