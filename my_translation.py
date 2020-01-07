import requests
import json
import js2py
import pyttsx3

# 播放查询单词声音
def tts(soykey):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-50)
    engine.say(str(soykey))
    engine.runAndWait()

while True:
    getTK = js2py.EvalJs() # 实例化一个执行js的环境对象
    googleTk = '''
    function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;
        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";
        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };
    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
'''

    # print('''1:google翻译\n2:百度翻译\n3:有道翻译\n4:金山翻译\n5:查看全部''')
    # getMenu = input("请选翻译引擎:")
    # getMenu = int(getMenu)
    print("\t|-----------translation-------------|")
    print("\t|   welcome use ssss translation    |")
    print("\t|autho:https://github.com/sssschenyi|")
    print("\t|-----------------------------------|")
    key=input("请输入需要翻译的文字:")

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

    def googlefangyi():
        getTK.execute(googleTk) # 传递js_str,执行js
        tk = getTK.TL(key)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
        }  # 设置请求的头部
        url ="https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&tk={}&q={}".format(tk, key)
        # print("url is",url)
        res = requests.get(url, headers=headers)
        html = json.loads(res.text)
        # print(tk,html[0][0][0])
        # print(html)
        return html[0][0][0]

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
            return "翻译出错，请重新输入"

    def jinsanfanyi():
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
        }
        url = "http://fy.iciba.com/ajax.php?a=fy"
        postdata = {
            'f': 'auto',
            't': 'auto',
            'w': key
            }
        response = requests.post(url=url, data=postdata, headers=headers)
        # resJSON = response.json()
        # return response.json()['content']['word_mean'][0]
        html = json.loads(response.text)
        # print(html)
        if html['status'] == 0:
            s = html['content']['word_mean'][0]
            return s
        elif html['status'] ==1:
            s = html['content']['out']
            return s

    def so360fanyi():
        try:
            headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
            }
            url = "http://fanyi.so.com/index/search?eng=1&validate=&ignore_trans=0&query={}".format(key)
            response = requests.post(url=url, headers=headers)
            html = json.loads(response.text)
            # print(html['data']['fanyi'])
            s = html['data']['fanyi']
            return s
        except Exception as e:
            print(e)

    paging = "================================================"
    tts(key)
    print(paging)
    print("youdao 翻译结果--->", youdaofanyi())
    print(paging)
    print("jinsan 翻译结果--->", jinsanfanyi())
    print(paging)
    print("  360  翻译结果--->", so360fanyi())
    print(paging)
    print("google 翻译结果--->",googlefangyi())
    print(paging)
    print(" baidu 翻译结果--->",baidufangyi())
    print(paging)


    # if getMenu == 1:
    #     print("google 翻译结果--->",googlefangyi())
    #     print('\n')
    # elif getMenu == 2:
    #     print("baidu 翻译结果--->",baidufangyi())
    #     print('\n')
    # elif getMenu == 3:
    #     print("youdao 翻译结果--->", youdaofanyi())
    #     print('')
    # elif getMenu == 4:
    #     print("google 翻译结果--->",googlefangyi())
    #     print('')
    #     print("baidu 翻译结果--->",baidufangyi())
    #     print('')
    #     print("youdao 翻译结果--->", youdaofanyi())

