#!/usr/bin/env python
# encoding: utf-8


import datetime
import requests
import hashlib
import hmac


def encrypthmacsha256(key,value):
    result = ''
    for b in hmac.new(bytes(key, 'utf-8'), bytes(value, 'utf-8'), hashlib.sha256).digest():
        result += format(b, 'x')
    return result


access_key = '5acdc05032ef2c2bc463e711'
private_key = '5acdc05032ef2c2bc463e712'
user_id = '5a0a946089b8fa1b4060c295'
timestamp = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
currency_id = 'mbtc'
msg = 'currencyId={id}&timestamp={ts}'.format(id=currency_id, ts=timestamp)
print('msg is', msg)

data = 'accesskey={key}&userid={uid}&'.format(key=access_key, uid=user_id)

sign = encrypthmacsha256(private_key,msg)

param = 'sign={sign}&timestamp={ts}'.format(sign=sign, ts=timestamp)
data = data + param
print(data)


url = 'https://api.xbrick.io/api/v1/user/getaccount?currencyId={id}'.format(id=currency_id)

headers = {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'}
r = requests.post(url, data=data, headers=headers)
print('resp is ', r.status_code, r.text)
