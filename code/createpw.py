# うまくいかなかった。
# {"statusCode":100,"body":{"commandId":"CMD170323314669208"},"message":"success"}
# のようにレスポンスがあるが、実際にはパスワードが設定されない

import os
import json
import requests
from dotenv import load_dotenv

import utils

base_url = 'https://api.switch-bot.com'
load_dotenv()
# tokenとsecretを貼り付ける
token = os.getenv("TOKEN") 
secret = os.getenv("secret") 
headers = utils.make_request_header(token,secret)

def read_keypad_from_json(deviceListJson='../deviceList.json') -> dict:
    createpw = {}
    f = open(deviceListJson,"r",encoding="utf-8")
    jsonfile = json.load(f)
    devices = jsonfile["body"]["deviceList"]

    for device in devices:
        if device["deviceType"] == "Keypad":
            device_pad = device
    return device_pad

def createpw(deviceId, passcode_name_str, passcode_type_str, passcode_str, valid_from_long, valid_to_long):
    devices_url = base_url + "/v1.1/devices/" + deviceId + "/commands"
    data = {
        "commandType": "command",
        "command": "createKey",
        "parameter": { "name": passcode_name_str, "type": passcode_type_str, "password": passcode_str, "startTime": valid_from_long, "endTime": valid_to_long },
    }
    try:
        # 作成
        res = requests.post(devices_url, headers=headers, json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:', e)

if __name__ == "__main__":
    # デバイス一覧を取得/更新
    utils.get_device_list()
    
    device = read_keypad_from_json()
    deviceId = device["deviceId"]
    
    passcode_name_str = "your_passcode_name"
    passcode_type_str = "your_passcode_type"
    passcode_str = "2213579"
    valid_from_long = ""
    valid_to_long = ""

    createpw(deviceId, passcode_name_str, passcode_type_str, passcode_str, valid_from_long, valid_to_long)
        
