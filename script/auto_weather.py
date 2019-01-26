# -*- coding: utf-8 -*-
from aip import AipSpeech
import requests
import re
from bs4 import BeautifulSoup
import time
import os


def getAqi(url):
    resp = requests.get(url,)
    resp.encoding = 'utf-8'
    aqi = resp.json()
    aqi_text = '空气质量：' + aqi['text']
    return aqi_text


def getWeather(url):
    text = '%s，%s，气温%d℃，体感温度%d℃，降水%.1fmm，相对湿度%d%%，风向%s，风速%s。'
    resp = requests.get(url)
    resp.encoding = 'utf-8'
    json = resp.json()
    print(json)
    station = json['station']
    weather = json['weather']
    wind = json['wind']
    text = text % (station['city'], weather['info'], weather['temperature'], weather['feelst'],
                    weather['rain'], weather['humidity'], wind['direct'], wind['power'])

    return text

def getNow():
    text = '现在时间是%s。'%(time.strftime("%H:%M", time.localtime()))
    return text 

'''
用百度的AIP
把文字变成mp3文件
'''
def stringToMp3(strings_txt):
    APPID = '9127702'
    APIKey = 'dpWei1rMPNcGrzQIejZlRa0O'
    SecretKey = '3c6922a1ba33bc3cbc6953056cde02d8'

    aipSpeech = AipSpeech(APPID, APIKey, SecretKey)
    result = aipSpeech.synthesis(strings_txt, 'zh', '1',
                                 {'vol': 8,
                                  'per': 0,
                                  'spd': 5})
    if not isinstance(result, dict):
        with open('test_tmp.wav', 'wb') as f:
            f.write(result)


'''
执行的主函数
'''
def main():
    timestamp = int(time.time() * 1000)
    aqi_url = 'http://www.nmc.cn/f/rest/aqi/59287?_=%s' % timestamp
    w_url = 'http://www.nmc.cn/f/rest/real/59287?_=%s' % timestamp

    text = getNow() + getWeather(w_url) + getAqi(aqi_url)
    print(text)
    stringToMp3(text)
    os.system('aplay -D bluealsa test_tmp.wav')


if __name__ == '__main__':
    main()
