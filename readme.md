1. Get Parameters 
![image](https://raw.githubusercontent.com/bombehappy/APIExample/master/api.png)

2. Code Example

C# Code
```
using System;
using System.IO;
using System.Net;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace Example
{
    class Program
    {        
        private static string _userId = "5a0a946089b8fa1b4060c295";
        private static string _publicKey = "5acdc05032ef2c2bc463e711";
        private static string _privateKey = "5acdc05032ef2c2bc463e712";
        private static string currencyId = "ae";
        private static string _baseUrl = "https://api.xbrick.io/api/v1";
        static void Main(string[] args)
        {
            var timestamp = GetTotalMilliseconds();
            string apiUrl = _baseUrl + "/user/getaccount";
            string signStr = $"currencyId={currencyId}&timestamp={timestamp}";
            String sign = EncryptHMACSHA256(_privateKey, signStr);
            string requestUrl = apiUrl + $"?currencyId={currencyId}";
            var data = DoRequestAsync<DemoObject>(requestUrl, sign, timestamp).Result;//Get Dada
            Console.Read();
        }

        public static long GetTotalMilliseconds()
        {
            DateTime timeStamp = new DateTime(1970, 1, 1);
            long stamp = (DateTime.UtcNow.Ticks - timeStamp.Ticks) / 10000;
            return stamp;
        }
        public static string EncryptHMACSHA256(string key, string value)
        {
            HMACSHA256 sha = new HMACSHA256(Encoding.UTF8.GetBytes(key));
            var bytes = sha.ComputeHash(Encoding.UTF8.GetBytes(value));
            string result = string.Empty;
            foreach (var item in bytes)
            {
                result += item.ToString("x");
            }
            return result;
        }
        protected static async Task<T> DoRequestAsync<T>(string requestUrl, string sign, long timestamp)
        {
            HttpWebRequest httpRequest = null;
            HttpWebResponse httpResponse = null;
            if (requestUrl.Contains("https://"))
            {
                httpRequest = (HttpWebRequest)WebRequest.CreateDefault(new Uri(requestUrl));
            }
            else
            {
                httpRequest = (HttpWebRequest)WebRequest.Create(requestUrl);
            }
            httpRequest.Method = "POST";
            httpRequest.ContentType = "application/x-www-form-urlencoded;charset=utf-8";
            var param = $"accesskey={_publicKey}&userid={_userId}";
            if (!string.IsNullOrEmpty(sign))
            {
                param += $"&sign={sign}";
            }
            if (timestamp > 0)
            {
                param += $"&timestamp={timestamp}";
            }
            byte[] btBodys = Encoding.UTF8.GetBytes(param);
            Stream newStream = httpRequest.GetRequestStream();
            newStream.Write(btBodys, 0, btBodys.Length);
            newStream.Close();
            try
            {
                httpResponse = (HttpWebResponse)await httpRequest.GetResponseAsync();
            }
            catch (WebException ex)
            {
                httpResponse = (HttpWebResponse)ex.Response;
            }

            if (httpResponse.StatusCode == HttpStatusCode.OK)
            {
                Stream st = httpResponse.GetResponseStream();
                StreamReader reader = new StreamReader(st, Encoding.GetEncoding("utf-8"));
                var result = reader.ReadToEnd();
                st.Close();
                httpResponse.Close();
                var data = Newtonsoft.Json.JsonConvert.DeserializeObject<T>(result);
                return data;
            }
            return default(T);
        }
    }
    public class DemoObject
    {
        public bool IsSuccess { get; set; }
        public int Code { get; set; }
        public object ErrorMsg { get; set; }
        public Data Data { get; set; }
    }

    public class Data
    {
        public decimal Balance { get; set; }
        public decimal Locked { get; set; }
        public decimal Mortgaged { get; set; }
    }
}

```
Python Code

```
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

```