from django.shortcuts import render, redirect, HttpResponseRedirect
from datetime import date
from aip import AipSpeech
import numpy as np
import pyaudio
import wave
import json
from . import models
import requests
import re
# 语音播报模块
import pyttsx3
from django.http import JsonResponse
# aiff文件转换成mp3编码文件模块
# from pydub import AudioSegment
from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
import sqlite3
from DeviceInformation.views import getApMac

"""
用户信息登录判断
获得所有用户信息密码键值对
"""

nameAndPasswd = {}
nameAndEmail = {}


def update_sql():
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql = 'select * from Home_userinfo'
    try:
        cur.execute(sql)
        # 获取所有数据
        person_all = cur.fetchall()
        # print(person_all)
        # 遍历
        for p in person_all:
            # 创建一组组新的用户信息字典 放入peopleInfo 用户名:密码
            peopleInfo = {p[1]: p[3]}
            # 创建用户名:邮箱
            peopleEmail = {p[1]: p[2]}
            # 将每个字典更新到nameAndPasswd 做成所有用户信息合集
            nameAndPasswd.update(peopleInfo)
            nameAndEmail.update(peopleEmail)

            # print(p)
    except Exception as e:
        print(e)
        print('查询失败')
    finally:
        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        print('用户数据加载完成')


update_sql()

"""
注册，登录，注销
"""


def admin(request):
    return render(request, 'Home/intro.html')


nameSignIN = ""


# 登录
def Sign(request):
    if request.method == 'POST':

        # 获取页面填写的信息
        global nameSignIN
        nameSignIN = request.POST.get('accountSignIn')
        passwordSignIN = request.POST.get('passwordSignIn')

        # 登录

        if nameAndPasswd.get(nameSignIN) == passwordSignIN:
            return render(request, 'Home/overview1.html')
            # print("密码正确")
        else:
            return render(request, 'Home/Sign_IN&UP.html')
            # print("密码错误")
        # if nameSignIN == 'huawei' and passwordSignIN == 'huawei':
        #     return render(request, 'Home/overview.html')
    return render(request, 'Home/Sign_IN&UP.html')


# 注册
def register(request):
    # 获取页面填写的信息
    userIdSignUp = request.POST.get('userIdSignUp')
    passwordSignUp = request.POST.get('passwordSignUp')
    confirmPasswordSignUp = request.POST.get('confirmPasswordSignUp')
    emailSignUp = request.POST.get('emailSignUp')
    # 注册
    if passwordSignUp == confirmPasswordSignUp:
        models.UserINFO.objects.create(username=userIdSignUp, password=passwordSignUp,
                                       email=emailSignUp)
        update_sql()
        return redirect('/Sign_IN&UP.html')

    print("注册失败")
    return redirect('/Sign_IN&UP.html')


# 获得个人信息

def getUserInfo(request):
    if request.method == 'POST':
        UserGetEmail = nameAndEmail.get(nameSignIN)

        return JsonResponse({"username": nameSignIN, "email": UserGetEmail})


# 修改个人信息
def infoChange(request):
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()

    if request.method == 'POST':
        useName = nameSignIN
        useNameChange = request.POST.get('username')
        emailChange = request.POST.get('email')
        cur.execute('UPDATE Home_userinfo set email=?,username=? where username=? ',
                    (emailChange, useNameChange, useName))
        con.commit()

        # 关闭游标
        cur.close()
        # 关闭连接
        con.close()
        return JsonResponse({"username": useNameChange, "email": emailChange})


# 返回
def overview1(request):
    return render(request, 'Home/overview1.html')


# def twoone(request):
#     return render(request, 'Home/2.1.html')

# Create your views here.


'''
语音输入模块
'''
APP_ID = "24814153"
API_KEY = "3qg6j5shEOUdfBMENNashNqQ"
SECRET_KEY = "Frs4HSY2h9wD5gtt3L8gXnAMz7hzF2cA "

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 5
warn = [0]  # 0不用发告警邮件 1发告警邮件


# user = [0]  # 1的时候跳转界面


def wav2pcm(wavfile, pcmfile, data_type=np.int16):
    f = open(wavfile, "rb")
    f.seek(0)
    f.read(44)
    data = np.fromfile(f, dtype=data_type)
    data.tofile(pcmfile)


def rec(file_name):
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("开始录音,请说话......")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束！")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(file_name, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def json_send():  # 发送函数
    url = 'http://47.106.23.116:7788'  # 改为服务器Ip
    header = {
        'Content-Type': 'application/json; charset=utf-8'
    }
    requests.post(url, headers=header)


def voice_play(voice_str):
    content = voice_str
    try:
        # 输出文件格式
        outFile = 'out.aiff'

        print('准备开始语音播报...')

        # 设置要播报的Unicode字符串
        engine.say(content)

        # 等待语音播报完毕
        engine.runAndWait()

        # 将文字输出为 aiff 格式的文件
        # engine.save_to_file(content, outFile)

        # 将文件转换为mp3格式
        # AudioSegment.from_file(outFile).export("Python.mp3", format="mp3")
    except Exception:
        print("出现错误")


def voice_recognition(voice_file):  # 语音识别
    keyword_warm = '检测'
    # keyword_user = '用户'

    # text_txt = json.loads(voice_file)

    # ----检测字符串中是否 有 检测  等关键词--------------------------
    if keyword_warm in voice_file:
        print('开始检测')
        # s = re.findall("\d+", voice_file)
        warn[0] = 1
    # if keyword_user in voice_file:
    #     user[0] = 1
    #     print(user)
    #     print('跳转页面')


# json_send //发送至服务器
# json_send()
engine = pyttsx3.init()


# def touserlist(request):
#     # 跳转用户界面
#     return render(request, 'Home/userlist.html')


def voice_detect(request):
    rec("1.wav")
    wav2pcm("1.wav", "1.pcm")
    with open("1.pcm", 'rb') as fp:
        file_context = fp.read()
    res = client.asr(file_context, 'pcm', 16000, {
        'dev_pid': 1537,
    })

    print(res['result'][0])  # 提取字典中 result 后信息
    res_str = res["result"][0]

    print(res_str)
    voice_recognition(res_str)  # 数据处理

    color = 'greenyellow'
    if warn[0] == 1:
        warning()
        warn[0] = 0

        # 返回语音对应页面url
    url = False
    AI = False
    url_dict = {'用户': '/userlist.html', '设备': '/other.html', '检测': '/errorDetect.html'}
    for i in url_dict.keys():
        if i in res_str:
            url = url_dict[i]
    ai = ['原因', '我', '设备情况', '优化']

    for i in range(len(ai)):
        if ai[i] in res_str:
            AI = ai[i]
            url = False

    return JsonResponse({'url': url, 'voice_detect': res_str, 'color': color, 'AI': AI})


# voice_detect(requests)  # 测试语音服务

'''
语音输入模块结束
'''

'''
邮箱告警模块
'''


def send_email(SMTP_host, from_addr, password, to_addrs, subject, content):
    """
    port = 587
    在登陆邮箱前加上email_client.starttls()这句话
    """
    email_client = SMTP(SMTP_host, 587)
    email_client.starttls()
    email_client.login(from_addr, password)

    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')  # subject
    msg['From'] = from_addr
    msg['to'] = ''.join(to_addrs)
    email_client.sendmail(from_addr, to_addrs, msg.as_string())

    email_client.quit()


def warning():
    # qq发送qq
    apMac = getApMac()
    mailPass = 'veqvfodwwfnhbdgd'
    receiver = ["943996316@qq.com"]
    send_email("smtp.qq.com", "943996316@qq.com", mailPass, receiver, "异常告警", "发现深圳站点的" + apMac + "出现流量异常")
