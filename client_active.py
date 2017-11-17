from time import sleep

import win32api

import win32con

from client import Client

if __name__ == '__main__':
    client = Client(code='0201705003')
    # client = Client(code='0201606005')
    # client = Client(code='0200810001')
    while True:
        json_text = client.run()
        msg = []
        if isinstance(json_text, str):
            print(json_text)
            if not json_text == 'Null':
                msg.append(json_text)
        if isinstance(json_text, list):
            for one in json_text:
                print(one.get('subject'),one.get('receive_date'))
                msg.append(one.get('subject') + one.get('receive_date'))
                print(msg)
        if len(msg):
            win32api.MessageBox(0, "\n".join(msg), "共收到{num}新消息".format(num=len(msg)), win32con.MB_OK)
        sleep(60*2)