# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import wechat
import json
import time
from wechat import WeChatManager, MessageType
from flask import request, Flask, jsonify

# 加载wechat库
wechat_manager = WeChatManager(libs_path='./libs')

# 连接回调
@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[CONNECT] client id: {0}'.format(client_id))

# 登录成功
class WxBot(wechat.CallbackHandler):
    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        # 判断登录成功后，就向文件助手发条消息
        if message_type == MessageType.MT_USER_LOGIN:
            time.sleep(2)
            wechat_manager.send_text(client_id, 'filehelper', '机器人已经上线')
# 
 # 初始化登录
wxbot = WxBot()
# 添加回调实例
wechat_manager.add_callback_handler(wxbot)
wechat_manager.manager_wechat(smart=True)
time.sleep(1)

# 启动flask服务

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/send', methods=['POST'])

def send():
    data = json.loads(request.get_data(as_text=True))
    client_id = data['client_id']
    to_wxid = data['to_wxid']
    content = data['content']
    time.sleep(1)
    wechat_manager.send_text(client_id, to_wxid, content)
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5050)