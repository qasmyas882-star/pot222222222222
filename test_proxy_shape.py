#!/usr/bin/env python3
import requests, json, time, random

def send_af(pkg, dev_key, gaid, af_uid, event_name, revenue=None, proxy=None, platform="android", idfa=None, idfv=None):
    url = f"https://api2.appsflyer.com/inappevent/{pkg}"
    current_ts = int(time.time() * 1000)
    APP_VERSION="2.3.0"; DEVICE_MODEL="SM-S911B"; OS_VERSION="Android 14"; SDK_VERSION="6.15.0"
    payload = {"appsflyer_id":af_uid,"advertising_id":gaid,"eventName":event_name,"eventTime":current_ts,"eventValue":{},"device_model":DEVICE_MODEL,"os_version":OS_VERSION,"sdk_version":SDK_VERSION,"app_version_name":APP_VERSION,"network":"WiFi","language":"en-US","timezone":"Asia/Riyadh"}
    level_num=''.join(filter(str.isdigit,event_name))
    if level_num: payload["eventValue"]={"af_level":level_num,"af_score":str(random.randint(1000,50000)),"af_duration":str(random.randint(30,300))}
    headers={"Authentication":dev_key,"User-Agent":f"AppsFlyer-Android-SDK/{SDK_VERSION} (Linux; Android 14; {DEVICE_MODEL})","Content-Type":"application/json","Accept":"*/*","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Connection":"keep-alive"}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30, proxies=proxy)
        return r.status_code, r.text[:100]
    except Exception as e:
        return 500, f"EXC: {e}"

# Reference-style SOCKS5 proxy dict (only socks5 key) - requests ignores it, goes direct
ref_socks5 = {"socks5": "socks5://fake:fake@1.2.3.4:9999"}
# My old-style SOCKS5 proxy dict (http/https keys) - requests tries to use it, throws
old_socks5 = {"http": "socks5://fake:fake@1.2.3.4:9999", "https": "socks5://fake:fake@1.2.3.4:9999"}

print("=== REFERENCE style socks5 dict (only socks5 key) ===")
print("Proxy dict:", ref_socks5)
s,r = send_af("com.superplaystudios.dicedreams","Hn5qYjVAaRNJYDcwF4LaWF",None,"1777078015955-4325801374339884483","af_kingdom_3_restored",None,ref_socks5,"ios")
print(f"Result: {s} - {r}")
print()
print("=== OLD style socks5 dict (http/https keys) ===")
print("Proxy dict:", old_socks5)
s,r = send_af("com.superplaystudios.dicedreams","Hn5qYjVAaRNJYDcwF4LaWF",None,"1777078015955-4325801374339884483","af_kingdom_3_restored",None,old_socks5,"ios")
print(f"Result: {s} - {r}")
