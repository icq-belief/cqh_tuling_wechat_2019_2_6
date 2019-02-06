# -*- coding:utf-8 -*-
from __future__ import unicode_literals
import getemotion
import json
import itchat
import requests
import platform
import os
import re
import random
import threading
# 登录和初始化

# 设置已回复人员列表,限制刷消息的人
replied = {}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    itchat.auto_login(enableCmdQR=2 ,hotReload=True)
    itchat.run()


def checkapi():
    try:
        inf = open('api.inf', 'r')
        api = inf.readline().replace('\n','')
        inf.close()
    except:
        print('请前往 http://www.tuling123.com 申请机器人API，并填写在相同目录下的“api.inf”文件首行！')
        input()


# 图灵机器人回复部分

def talk(info, userid=None):
    url = 'http://www.tuling123.com/openapi/api'
    inf = open('api.inf', 'r')
    api = inf.readline()
    inf.close()
    param = json.dumps(
        {"key": api, "info": info, "userid": userid})
    callback = requests.post(url, data=param)
    result = eval(callback.text)
    code = result['code']
    if code == 100000:
        recontent = result['text']
    elif code == 200000:
        recontent = result['text'] + result['url']
    elif code == 302000:
        recontent = result['text'] + result['list'][0]['info'] + \
            result['list'][0]['detailurl']
    elif code == 308000:
        recontent = result['text'] + result['list'][0]['info'] + \
            result['list'][0]['detailurl']
    else:
        recontent = '[我的助理Neo暂时还不会回应你的这句话.Sad Face.]'
    return recontent


# userid通过用户名的md5产生
# 用于用户名的加密
def md5(str):
    import hashlib
    md = hashlib.md5()
    md.update(str.encode('utf-8'))
    return md.hexdigest()


# 注册微信消息,对于微信接受到的文字消息的回复,设置了每个人每天4次的回复频率
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # reply = talk(msg['Text'], md5(msg['FromUserName']))
    reply = u"[Master陈不在 我是助理Neo 有事请留言]  {}".format(talk(msg['Text']), md5(msg['FromUserName']))
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s悄悄对您说：%s' % (NickName, msg['Text']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')

    if not replied.get(md5(msg['FromUserName']+'_TEXT')):
        # 当消息不是由自己发出的时候
        replied[md5(msg['FromUserName']+'_TEXT')] = 1
        return reply
        # 回复给好友
    elif replied[md5(msg['FromUserName']+'_TEXT')] < 4:
        replied[md5(msg['FromUserName']+'_TEXT')] += 1
        return reply
    elif replied[md5(msg['FromUserName']+'_TEXT')] > 4:
        pass
    else:
        replied[md5(msg['FromUserName']+'_TEXT')] += 1
        return u"[主人不让我多跟你聊天.So,have a nice day!]"


# 对于地图分享的回复,每天只会回复每人一次
@itchat.msg_register(itchat.content.MAP)
def map_reply(msg):
    reply = talk(msg['Text'], md5(msg['FromUserName']))
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s向您分享了地点：%s' % (NickName, msg['Text']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_MAP')):
        replied[md5(msg['FromUserName'] + '_MAP')] = 1
        return u"[%s,在%s玩得开心.就不要调戏我的助理Neo了.航留.] " % (NickName, msg['Text'])
    else:
        pass


# 对于名片分享的回复,每天只会回复每人一次
@itchat.msg_register(itchat.content.CARD)
def card_reply(msg):
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])

    reply = '[%s,助理Neo代主人谢谢你的推荐,我们会成为好朋友的!今天就不再回复你的名片推荐了,谢谢. ] ' % NickName
    print('------------------------------------------------------------------------------')
    print('%s向您推荐了%s' % (NickName, msg['Text']['NickName']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_CARD')):
        replied[md5(msg['FromUserName'] + '_CARD')] = 1
        return reply
    else:
        pass


@itchat.msg_register(itchat.content.NOTE)
def note_reply(msg):
    print(msg)


# 对于分享的文章或者链接进行回复,进行一些次数的限制
@itchat.msg_register(itchat.content.SHARING)
def sharing_reply(msg):
    # reply = talk(msg['Text'], md5(msg['FromUserName']))
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    reply = u"[%s,助理Neo代主人感谢你的分享,陈主人会在闲暇时间查看你分享的内容的.今天Neo就不再回复你的内容分享了,谢谢.] " % NickName
    print('------------------------------------------------------------------------------')
    print('%s向您分享了链接：%s' % (NickName, msg['Text']))
    print('AI帮您回复%s：%s' % (NickName, reply))
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_SHARING')):
        replied[md5(msg['FromUserName'] + '_SHARING')] = 1
        return reply
    else:
        pass


# 收到别人的私聊图片时候,回复爬取到的斗图啦上的图片,只会回复5次
@itchat.msg_register(itchat.content.PICTURE)
def pic_reply(msg):
    # msg['Text']('./images/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s给您发送了一个表情/图片，已经存入img目录，文件名：%s' % (NickName, msg['FileName']))
    print('AI帮您回复%s默认表情default.gif' % NickName)
    print('------------------------------------------------------------------------------')

    path_list = return_image_path()
    res_path = './images/%s' % (path_list[random.randint(0, (len(path_list)-1))])

    # res_path = getemotion.getRandomEmoticon()
    res_path = '@img@./%s' % res_path

    if not replied.get(md5(msg['FromUserName']+'_PICTURE')):
        # 当消息不是由自己发出的时候
        replied[md5(msg['FromUserName']+'_PICTURE')] = 1
        return u"[主人暂时不在.继续发送图片,助理Neo将会与你斗一下图.Don't be so serious.] "
        # 回复给好友
    elif replied[md5(msg['FromUserName']+'_PICTURE')] < 5:
        replied[md5(msg['FromUserName']+'_PICTURE')] += 1
        return res_path
    elif replied[md5(msg['FromUserName']+'_PICTURE')] > 5:
        pass
    else:
        replied[md5(msg['FromUserName']+'_PICTURE')] += 1
        return u"[主人让我斗图让着你.Neo就不发了.See you!] "


# @itchat.msg_register(itchat.content.RECORDING)
# def rec_reply(msg):
#     # 是否开启语音识别，需要安装ffmpeg和pydub
#     enable_voice_rec = False
#     msg['Text']('./records/' + msg['FileName'])
#     User = itchat.search_friends(userName=msg['FromUserName'])
#     if User['RemarkName'] == '':
#         NickName = User['NickName']
#     else:
#         NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
#
#     if enable_voice_rec:
#         msg['Text']('./records/' + msg['FileName'])
#         from beta import wav2text
#         wav2text.transcode('./records/' + msg['FileName'])
#         filename = msg['FileName'].replace('mp3','wav')
#         text = wav2text.wav_to_text('./records/' + filename)
#         reply = talk(text, md5(msg['FromUserName']))
#         print('------------------------------------------------------------------------------')
#         print('%s给您发送了一条语音，已经存入records目录，文件名：%s' % (NickName, msg['FileName']))
#         print('智能识别该消息内容为：%s' % text)
#         print('AI帮您回复%s：%s' % (NickName, reply))
#         print('------------------------------------------------------------------------------')
#         return reply
#     else:
#         print('------------------------------------------------------------------------------')
#         print('%s给您发送了一条语音，已经存入records目录，文件名：%s' % (NickName, msg['FileName']))
#         print('AI帮您回复%s默认表情default.gif' % NickName)
#         print('------------------------------------------------------------------------------')
#         return '@img@./records/default.gif'


@itchat.msg_register(itchat.content.ATTACHMENT)
def att_reply(msg):
    # msg['Text']('./attachments/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s给您发送了一个文件，已经存入attachments目录，文件名：%s' % (NickName, msg['FileName']))
    print('AI帮您回复% s：这是什么东西？我收下了。' % NickName)
    print('------------------------------------------------------------------------------')
    if not replied.get(md5(msg['FromUserName']+'_ATTACHMENT')):
        replied[md5(msg['FromUserName'] + '_ATTACHMENT')] = 1
        return '[%s,给我家主人发送的%s. Neo代为收下了.今天就不再回复你的文件分享了.谢谢] ' % (NickName, msg["FileName"])
    else:
        pass


# 别人发送的视频时,自动回复视频,视频事先从抖音上爬取好了
@itchat.msg_register(itchat.content.VIDEO)
def video_reply(msg):
    # msg['Text']('./videos/' + msg['FileName'])
    User = itchat.search_friends(userName=msg['FromUserName'])
    if User['RemarkName'] == '':
        NickName = User['NickName']
    else:
        NickName = '%s(%s)' % (User['NickName'], User['RemarkName'])
    print('------------------------------------------------------------------------------')
    print('%s给您发送了一个视频，已经存入videos目录，文件名：%s' % (NickName, msg['FileName']))
    print('AI帮您回复% s默认表情default.gif' % NickName)
    print('------------------------------------------------------------------------------')
    path_list = return_video_path()
    res_path = './videos/%s' % (path_list[random.randint(0, (len(path_list)-1))])

    if not replied.get(md5(msg['FromUserName']+'_VIDEO')):
        # 当消息不是由自己发出的时候
        replied[md5(msg['FromUserName']+'_VIDEO')] = 1
        return u"[陈主人暂时不在.继续发送视频.助理Neo将会发送一些小视频给你.Don't be so serious.] "
        # 回复给好友
    elif replied[md5(msg['FromUserName']+'_VIDEO')] < 4:
        replied[md5(msg['FromUserName']+'_VIDEO')] += 1
        itchat.send_video(res_path, msg['FromUserName'])
    elif replied[md5(msg['FromUserName']+'_VIDEO')] > 4:
        pass
    else:
        replied[md5(msg['FromUserName']+'_VIDEO')] += 1
        return u"[福利 are not free.发送红包后继续.Have a nice day & See you!] "

    # res_path = './videos/40.mp4'

    # itchat.send_video(res_path, msg['FromUserName'])
    # print(itchat.send_video(res_path, msg['FromUserName']))


def return_image_path():
    s = os.listdir('./images')
    # print(s)
    return_s = []
    for i in s:
        if re.findall('(^\d+\.gif)|(^\d+\.jpg)', i):
            return_s.append(i)
        else:
            pass
    return return_s


def return_video_path():
    s = os.listdir('./videos')
    return_s = []
    for i in s:
        if i[-4:] != '.mp4':
            pass
        else:
            return_s.append(i)
    return return_s


def del_pic():
    s = os.listdir('./images')
    for i in s:
        if (re.findall('(^\d+\.jpg)|(^\d+\.gif)',i)):
            file_path = os.path.join(BASE_DIR, 'images',i)
            os.remove(file_path)
            # print(file_path)


# 设置定时器,每12个小时清理图片缓存,不再回复列表清单
def fun_timer():
    replied.clear()
    del_pic()
    for i in range(1,200):
        getemotion.getRandomEmoticon()
    global timer
    timer = threading.Timer(43200, fun_timer)
    timer.start()


# @itchat.msg_register(itchat.content.FRIENDS)
# def fri_reply(msg):
#     itchat.add_friend(**msg['Text'])
#     itchat.send_msg('你好，我的人类朋友！', msg['RecommendInfo']['UserName'])


# @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
# def group_reply(msg):
#     if msg['isAt']:
#         reply = talk(msg['Content'], md5(msg['ActualUserName']))
#         print(
#             '------------------------------------------------------------------------------')
#         print('%s在群聊中对您说：%s' % (msg['ActualNickName'], msg['Content'].replace('\u2005',' ')))
#         print('AI帮您回复%s：%s' % (msg['ActualNickName'], reply))
#         print(
#             '------------------------------------------------------------------------------')
#
#         if not replied.get(md5(msg['ActualUserName'] + '_GROUPTEXT')):
#             # 当消息不是由自己发出的时候
#             replied[md5(msg['ActualUserName'] + '_GROUPTEXT')] = 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人不在.助理Neo会开始回复你.Don't be serious.]"), msg['FromUserName'])
#             # 回复给好友
#         elif replied[md5(msg['ActualUserName'] + '_GROUPTEXT')] < 3:
#             replied[md5(msg['ActualUserName'] + '_GROUPTEXT')] += 1
#             itchat.send('@%s %s' % (msg['ActualNickName'],u"[陈主人不在.暂时由助理Neo回复你] " + reply), msg['FromUserName'])
#         elif replied[md5(msg['ActualUserName'] + '_GROUPTEXT')] > 3:
#             pass
#         else:
#             replied[md5(msg['ActualUserName'] + '_GROUPTEXT')] += 1
#             # return u"[陈主人不让我太闹腾.Neo就不再回复你了.See you!] "
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人不让我太闹腾.Neo就不再回复你了.See you!] "), msg['FromUserName'])
    # else:
    #     print(
    #         '------------------------------------------------------------------------------')
    #     print('%s在群聊中说：%s' % (msg['ActualNickName'], msg['Content']))
    #     print(
    #         '------------------------------------------------------------------------------')


# @itchat.msg_register(itchat.content.PICTURE, isGroupChat=True)
# def grouppic_reply(msg):
#         # msg['Text']('./images/group/' + msg['FileName'])
#         print('------------------------------------------------------------------------------')
#         print('%s在群聊中发了一个表情/图片，已经帮您存入images/group目录，文件名为：%s' % (msg['ActualNickName'], msg['FileName']))
#         print('------------------------------------------------------------------------------')
#         res_path = getemotion.getRandomEmoticon()
#         res_path = '@img@./%s' % res_path
#
#         if not replied.get(md5(msg['ActualNickName']+'_GROUPPICTURE')):
#             # 当消息不是由自己发出的时候
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] = 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人不在.助理Neo会开始与你斗一下图.Don't be serious.]"), msg['FromUserName'])
#             # 回复给好友
#         elif replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] < 4:
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] += 1
#             itchat.send(res_path, msg['FromUserName'])
#         elif replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] > 4:
#             pass
#         else:
#             replied[md5(msg['ActualNickName']+'_GROUPPICTURE')] += 1
#             itchat.send('@%s %s' % (msg['ActualNickName'], u"[陈主人让我斗图让着你.Neo就不发了.See you!]"), msg['FromUserName'])
#
#             # return u"[主人让我斗图让着你.Neo就不发了.See you!] "
#
#         # itchat.send(res_path, msg['FromUserName'])

if __name__ == '__main__':
    checkapi()
    main()
    timer = threading.Timer(1, fun_timer)
    timer.start()
    # return_video_path()
