#encoding=utf-8  
import os
import time
import wave
import cv2
import urllib, urllib2, pycurl  
import base64  
import json
import StringIO  #这个用到里面的write函数
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

## get access token by api key & secret key      
def get_token(): #语音识别密钥 
    apiKey = "ILujDwEvFrGB1G4ROyBvLmEZ"  
    secretKey ="f510925c2d1147bdf5a879a2e7b0cf96"  
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey  
    res = urllib2.urlopen(auth_url)  
    json_data = res.read()  
    return json.loads(json_data)['access_token']

def get_token2(): #语音合成密钥
    apiKey = "WsUjLlrF4B7w3p6GrxQnEyoz"  
    secretKey ="e5802100d97fed06138e1c17470f6026"  
    auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey  
    res = urllib2.urlopen(auth_url)  
    json_data = res.read()  
    return json.loads(json_data)['access_token']
  
def dump_res(buf):#获取图灵机器人回答内容
    global duihua
    #print buf
    a=eval(buf)
    #print type(a)
    if a['err_msg']=='success.' :
      duihua=a['result'][0]
      return duihua

def getHtml(url):#图灵机器人网址

    page = urllib.urlopen(url)

    html = page.read()

    return html

 
def use_cloud(token):#语音识别内容上传  
    #  fp = wave.open('test.pcm', 'rb')  
    fp = wave.open('/home/pi/test2.wav', 'rb')  
    #  fp = wave.open('vad_1.wav', 'rb')  
    nf = fp.getnframes()  
    f_len = nf * 2  
    audio_data = fp.readframes(nf)  
  
    #mac addr  
    cuid = "11198201"  
    srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token  
    http_header = [  
        'Content-Type: audio/pcm; rate=16000',  
        #  'Content-Type: audio/pcm; rate=8000',  
        'Content-Length: %d' % f_len  
    ]  
  
    c = pycurl.Curl()  
    c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
    #c.setopt(c.RETURNTRANSFER, 1)
    c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict  
    c.setopt(c.POST, 1)
    c.setopt(c.CONNECTTIMEOUT, 30)  
    c.setopt(c.TIMEOUT, 30)  
    c.setopt(c.WRITEFUNCTION, dump_res)  
    c.setopt(c.POSTFIELDS, audio_data)  
    c.setopt(c.POSTFIELDSIZE, f_len)
    b = StringIO.StringIO()
    c.setopt(pycurl.WRITEFUNCTION, b.write) #把StringIO的写函数注册到pycurl的WRITEFUNCTION中，即pycurl所有获取的内容都写入到StringIO中，如果没有这一句，pycurl就会把所有的内容在默认的输出器中输出
    c.perform()
    back=b.getvalue()
    return dump_res(back)
    #c.perform() #pycurl.perform() has no return val  
    
def yuyinhecheng_api(tok,tex): #语音合成结果所在网址
    cuid = '11198201' 
    spd = '4' 
    url = 'http://tsn.baidu.com/text2audio?tex='+tex+'&lan=zh&cuid='+cuid+'&ctp=1&tok='+tok+'&per=3'
    #print url 
    #response = requests.get(url) 
    #date = response.read() 
    return url
    
if __name__ == "__main__":
    os.system('xset dpms force off')
    time.sleep(5)
    token = get_token()
    token2 = get_token2()
    flag = 0
    no=0
    key = '31586775b0f3460d93d6c00b4e43757c'

    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

    
while True:
    #url = yuyinhecheng_api(token2,'请说话')
    #os.system('mpg123 "%s"'%url)
    os.system('arecord -D "plughw:1,0" -r 16000 -f S16_LE -d 5 > /home/pi/test2.wav')
    #info = raw_input('我: ')
    
    word=use_cloud(token)
    info = word
    if info is not None:
        request = api + info 

        response = getHtml(request)

        dic_json = json.loads(response)

        #os.system('espeak -vzh '+dic_json['text'].encode('utf-8'))
        if flag == 1:
            if '视频' in info: #视频播放部分               
                if '换' in info:
                    no+=1
                if no > 1:
                    no=0
                os.system('omxplayer -r -o both /home/pi/testvideo'+str(no)+'.mp4')
    
            if '帽' in info:#试穿中的戴帽部分
                if '圣诞' in info:
                    os.system('python2 /home/pi/Desktop/hat.py 1')
                if '毛线' in info:
                    os.system('python2 /home/pi/Desktop/hat.py 2')
                if '女士' in info:
                    os.system('python2 /home/pi/Desktop/hat.py 3')
                if '兔耳' in info:
                    os.system('python2 /home/pi/Desktop/hat.py 4')
            if '眼镜' in info:#试穿中的戴眼镜部分
                if '蓝色' in info:
                    os.system('python2 /home/pi/Desktop/glass.py 1')
                if '黑色' in info:
                    os.system('python2 /home/pi/Desktop/glass.py 2')
                if '粉色' in info:
                    os.system('python2 /home/pi/Desktop/glass.py 3')
                if '棕色' in info:
                    os.system('python2 /home/pi/Desktop/glass.py 4')
            if '关闭' not in info and '视频' not in info and '帽' not in info and '眼镜' not in info:#对话部分
                url = yuyinhecheng_api(token2,dic_json['text'].encode('utf-8'))
                os.system('mpg123 "%s"'%url)
        if '关闭' in info:#关闭熄屏部分
            url = yuyinhecheng_api(token2,'好的，主人，有事再来找我')
            os.system('mpg123 "%s"'%url)
            os.system('xset dpms force off')
            flag = 0
        if '魔镜' in info and flag ==0:#启动部分
            os.system('xset dpms force on')
            url = yuyinhecheng_api(token2,'主人，需要我做些什么')
            os.system('mpg123 "%s"'%url)
            flag = 1
    else:
        if flag == 1:
            url = yuyinhecheng_api(token2,'没听到')
            os.system('mpg123 "%s"'%url)
            flag = 0
    
