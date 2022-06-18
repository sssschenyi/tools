import requests
import json
import js2py
import hashlib
import re
from bs4 import BeautifulSoup
import pyttsx3

# 播放查询单词声音
def tts(soykey):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.say(str(soykey))
    engine.runAndWait()



def youdaofanyi():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }# 设置请求的头部
    url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
    postdata = {'i':key,
                'from':'AUTO',
                'to':'AUTO',
               'doctype':'json'}
    response = requests.post(url=url,data=postdata,headers=headers)#模拟请求
    # response.content.decode("utf-8")
    # print(response.content)
    resJSON = response.json()
    # print(resJSON)
    if resJSON['errorCode'] == 0:
        # print(response.json()['translateResult'][0][0]['tgt'])
        return response.json()['translateResult'][0][0]['tgt']


def baidufangyi():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Mobile Safari/537.36",
        }
        # url ="https://fanyi.baidu.com/v2transapi?from=en&to=zh"
        # url = "http://fanyi.baidu.com/basetrans" # 手机翻译地址
        url = "https://fanyi.baidu.com/sug"
        postdata = {
            'kw': key
            }
        response = requests.post(url=url, data=postdata, headers=headers)  # 模拟请求
        # response = requests.post(url=url, headers=headers)
        html = json.loads(response.text)
        s = html['data'][0]['v']
        trandata = s.lstrip('n. ')
        # print(trandata)
        return trandata.lstrip() # sug addess
    except:
        return "sorry 百度未能翻译"

# 金山翻译参考 https://blog.csdn.net/yuankingping/article/details/112289212
def jinsanfanyi():
    try:
        fanyiStr = '6key_cibaifanyicjbysdlove1' + key     
        #6key_cibaifanyicjbysdlove1 是金山的加密文字
        a = hashlib.md5() #初始化MD5
        a.update(fanyiStr.encode(encoding='utf-8'))
        q = a.hexdigest()[0:16]#截取md5 前16位数字

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }
        url = "https://ifanyi.iciba.com/index.php?c=trans&m=fy&client=6&auth_user=key_ciba&sign=" + q
        postdata = {
        'form': 'auto',
        'to': 'auto',
        'q': key
        }
        response = requests.post(url=url, data=postdata, headers=headers)
        resJSON = response.json()
        return(resJSON['content']['out'])
    except:
        print('sorry 金山未能翻译')


# 360翻译请求头部必须带COOKIE 和 pro  参数
# 360翻译请求头部必须带COOKIE 和 pro  参数
def qihufangyi():
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    "cookie": "QiHooGUID=C99CC3DBDA192808142BB9F0A3F7C416.1650112546471",
    "pro": "fanyi",
    }


    # 判断eng 的参数是否为中文
    for _char in key:
        if key >='\u4e00' and  key <= '\u9fa5':
            e = 0
        else:
            e = 1

    url = "https://fanyi.so.com/index/search"
    postdata = {
    'eng': e,
    'query': key
    }
    #print(url)
    response = requests.post(url=url,data=postdata, headers=headers)

    html = response.json()
    return(html['data']['fanyi'])
def googlefangyi():
    try:
        headers ={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        } 
        # 设置请求的头部
        q = key.replace(' ','+')
        # 判断eng 的参数是否为中文,中文e等于0，英文e等于1
        for _char in key:
            if key >='\u4e00' and  key <= '\u9fa5':
                #e = 0
                #中译英
                url = 'https://translate.google.cn/m?sl=zh-CN&tl=en&hl=zh-CN&q='+q
            else:
                #e = 1
                #英译中
                url = 'https://translate.google.cn/m?sl=en&tl=zh-CN&hl=zh-CN&q='+q
    
        #print("url is",url)
        res = requests.get(url, headers=headers)
        html = res.text
        soup = BeautifulSoup(html,'html.parser')
        val=soup.find(class_='result-container').text
        return(val)
    except:
        return "google 未能翻译"




def microsoftfangyi():
    #get 地址栏的IG值
    def get_Value():
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'} #设置请求头
        url = 'https://cn.bing.com/translator/'
        result=requests.get(url,headers=headers)
        global IG_value    
        global token_value
        global key_value    
        #查找 IG 的值
        ig =re.search(',IG:"(.*?)",',result.text)
        IG_value = ig.group(1)
        #查找 token 和 key 的值，token 和 key的变量放在 params_RichTranslateHelper 这里
        find_token_v = result.text.split('params_RichTranslateHelper =')[1]# 截取params_RichTranslateHelper后面的字符
        get_token_Str=find_token_v[1:84]#得到一个字符串
        get_token_Str = get_token_Str.replace('[','').replace(']','').replace('"','')#替换  [ “ 字符
        change_getoken_value = get_token_Str.split(",")#把get_token_List转换成列表
        key_value  = change_getoken_value[0]#获得key变量的值
        token_value= change_getoken_value[1]#获得token变量的值


    get_Value()#初始化函数

    # 判断 输入的 key  的是否为中文，中文e等于0，英文e等于1
    for _char in key:
        if key >='\u4e00' and  key <= '\u9fa5':
            #e = 0
            fromLang = 'en'
        else:
            #e = 1
            fromLang = 'zh-Hans'



    IID_value = 'translator.5023.3'
    url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG='+IG_value+'&IID='+IID_value
    #print('url',url)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'} #设置请求头
    post_data={'fromLang':'auto-detect','text':key,'to':fromLang,"token": token_value,'key':key_value} #设置请求参数
    #print('post_data',post_data)
    result=requests.post(url,post_data,headers=headers) #发出请求并将请求数据转换为str格式
    resuJSON = result.json()
    #print(result.status_code)
    #print(resuJSON)
    return (resuJSON[0]['translations'][0]['text'])




def get_Value():
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'} #设置请求头
    url = 'https://translate.alibaba.com/'
    result=requests.get(url,headers=headers)

    global csrf_value    

    #查找 token 和 key 的值，token 和 key的变量放在 params_RichTranslateHelper 这里
    find_token_v = result.text.split('_csrf :')[1]# 截取_csrf :后面的字符
    get_token_Str=find_token_v[1:40]#得到一个字符串
    get_token_Str = get_token_Str.replace('\'','').replace('\n','')#替换  [ “ 字符
    change_getoken_value = get_token_Str.split(",")#把get_token_List转换成列表
    csrf_value  = change_getoken_value[0]#获得key变量的值
    #print("csrf_value",change_getoken_value)


get_Value()#初始化函数

def alifangyi():
    try:
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        'cookie': 'xman_us_f=x_l=1; xman_t=rFjNqyz0hvtmBfEuogdS51HLUX13Vp0/UloE3PGN9bCPXDWn6kfsRZaBY3nCwVDl; acs_usuc_t=acs_rt=17dbe6bd997b45ff98c03799f1dd1266; xman_f=d6Ni2ci5PuAPP1gGp+acEatvR5DO9mX6TcKVvQzPVNxDjE9MiBQg2MWTbHKG/H/hOX/sVYBkOpxPeS7dVwTIYgfHR7/HfhYfOyD668QnTaV40O3jcVnqiA==; __itrace_wid=c2905f91-d846-4b72-2c11-98e2d2cdb424; cna=A1XgGqtSpwcCAXWZhNCjYHjG; xlly_s=1; acs_t=OyCHWPuDRIiIoloFZC4z8Xd5A84Mak5Kr9UzoFm8YLkGo1egj22Tc1PpQxg/Rdbl; tfstk=c4kRBOvMDEYkUXqxbbdmYEZ9V6xdCRO8-E4Npvng3ehhOIELAx1ccADOMo60XPzJD; l=eBaZBCYnLuP_GfFWBO5ZKurza77t2LAjGNFzaNbMiInca1yhxUIA0OC3d85MIdtjgt5fE9-y52gX3RE2-x4LRE6k-M2eg_rpnd9MRe1..; isg=BKqqItxyvDhbCTBVnRh_jZfI-xBMGy51pFu82DRpYf3NZ14hf6pjhQXR95P7y6YN',
        }# 设置请求的头部
        url = 'https://translate.alibaba.com/api/translate/text'
        # 判断 输入内容是否为中文,中文e等于0，英文e等于1
        for _char in key:
            if key >='\u4e00' and  key <= '\u9fa5':
                #e = 0
                tatLang = 'en'
            else:
                #e = 1
                tatLang = 'zh'
        
        # 自动检测中英文
        if tatLang == 'en':
            src = 'zh'
        else:
            src = 'en'
        postdata = {"srcLang":src,
                    "tgtLang":tatLang,
                   "domain":"general",
                   "query":key,
                   "_csrf":csrf_value
                   }


        #print("key:",key,"tatlang",tatLang)
        response = requests.post(url=url,data=postdata,headers=headers)#模拟请求
        #print("postdata",postdata)
        #print(response.content.decode("utf-8"))
        #print(response.status_code)
        #print("postdata is",response.text)
        resJSON = response.json()
        #print(resJSON)
        return resJSON['data']['translateText']
    except:
        print('sorry 阿里未能翻译')


#微软翻译

#'''

while True:
    # getMenu = int(getMenu)
    print("\t|-----------translation--------------|")
    print("\t|   welcome use ssss translation     |")
    print("\t|author:https://github.com/sssschenyi|")
    print("\t|------------------------------------|")
    key=input("请输入需要翻译的文字:")
    #tts(key) # 调用函数，播放语音
    if key == "-q" or key == "-Q":
        break
    else :
        print("youdao 翻译结果-->", youdaofanyi(),"\n")
        print("jinsan 翻译结果-->", jinsanfanyi(),"\n")
        print("  360  翻译结果-->", qihufangyi(),"\n")
        print("google 翻译结果-->",googlefangyi(),"\n")
        print(" baidu 翻译结果-->",baidufangyi(),"\n")
        print("aliba  翻译结果-->",alifangyi(),"\n")
        print("micro  翻译结果-->",microsoftfangyi(),"\n")

#'''