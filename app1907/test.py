import random

import itchat
import time
from itchat.content import *




gname = '柏菲特定制门窗'

context = '这是一条我设定群的群发消息，微信正式处于托管状态。大家可以忽略'

#{'MemberList': <ContactList: []>, 'Uin': 0, 'UserName': '@102743bc3c795e7b68de31981eb44236e1230e9d38ff24e4b539f8409dc090ac', 'NickName': 'nyggl', 'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=636753186&username=@102743bc3c795e7b68de31981eb44236e1230e9d38ff24e4b539f8409dc090ac&skey=@crypt_b9b909ac_43db78e4f904b46962afe346bcde63d5', 'ContactFlag': 3, 'MemberCount': 0, 'RemarkName': '黄仁坤', 'HideInputBarFlag': 0, 'Sex': 1, 'Signature': '', 'VerifyFlag': 0, 'OwnerUin': 0, 'PYInitial': 'NYGGL', 'PYQuanPin': 'nyggl', 'RemarkPYInitial': 'HRK', 'RemarkPYQuanPin': 'huangrenkun', 'StarFriend': 0, 'AppAccountFlag': 0, 'Statues': 0, 'AttrStatus': 102501, 'Province': '', 'City': '', 'Alias': '', 'SnsFlag': 1, 'UniFriend': 0, 'DisplayName': '', 'ChatRoomId': 0, 'KeyWord': '', 'EncryChatRoomId': '', 'IsOwner': 0}

def Sendfriend(game,context):
    myfriend = itchat.get_friends(update=True)
    print(myfriend)
    friend = itchat.search_friends(name=gname)
    for friend in myfriend:
        if friend['NickName'] == gname:
            print('1')
            # time.sleep(random.randint(0,3))
            while True:
                print('1')
                username = friend['UserName']
                itchat.send_msg(context,username)
                time.sleep(random.randint(0, 2))

def SendChatRoomsMsg(gname, context):
    # 获取所有群的相关信息，update=True表示信息更新
    myroom = itchat.get_chatrooms(update=True)

    global username

    # 搜索群名
    myroom = itchat.search_chatrooms(name=gname)
    # print(myroom.key())
    for room in myroom:
        print(room)
        if room['NickName'] == gname:
            username = room['UserName']
            itchat.send_msg(context, username)
        else:
            print('No groups found')


# 监听是谁给我发消息
@itchat.msg_register(INCOME_MSG)
def text_reply(msg):
    # 打印获取到的信息
    # print(msg)
    itchat.send("您发送了：\'%s\'\n微信目前处于python托管，你的消息我会转发到手机，谢谢" %
                (msg['Text']), toUserName=msg['FromUserName'])


itchat.auto_login(hotReload=True)

# SendChatRoomsMsg(gname, context)
Sendfriend(gname,context)
itchat.run()
