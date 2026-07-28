#!/usr/bin/env python3
import requests, json, time, random, uuid

def send_af(pkg, dev_key, gaid, af_uid, event_name, revenue=None, proxy=None, platform="android", idfa=None, idfv=None):
    url = f"https://api2.appsflyer.com/inappevent/{pkg}"
    current_ts = int(time.time() * 1000)
    APP_VERSION = "2.3.0"; DEVICE_MODEL = "SM-S911B"; OS_VERSION = "Android 14"; SDK_VERSION = "6.15.0"
    payload = {
        "appsflyer_id": af_uid,
        "advertising_id": gaid,
        "eventName": event_name,
        "eventTime": current_ts,
        "eventValue": {},
        "device_model": DEVICE_MODEL, "os_version": OS_VERSION, "sdk_version": SDK_VERSION,
        "app_version_name": APP_VERSION, "network": "WiFi", "language": "en-US", "timezone": "Asia/Riyadh"
    }
    if revenue:
        payload["eventRevenue"]=str(revenue); payload["eventCurrency"]="USD"
    else:
        level_num=''.join(filter(str.isdigit,event_name))
        if level_num:
            payload["eventValue"]={"af_level":level_num,"af_score":str(random.randint(1000,50000)),"af_duration":str(random.randint(30,300))}
    headers = {"Authentication":dev_key,"User-Agent":f"AppsFlyer-Android-SDK/{SDK_VERSION} (Linux; Android 14; {DEVICE_MODEL})","Content-Type":"application/json","Accept":"*/*","Accept-Language":"en-US,en;q=0.9","Accept-Encoding":"gzip, deflate, br","Connection":"keep-alive"}
    print(f"[DEBUG] af_uid={af_uid!r} gaid={gaid!r}")
    print(f"[DEBUG] payload={json.dumps(payload)}")
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"[DEBUG] {r.status_code} - {r.text[:200]}")
        return r.status_code, r.text
    except Exception as e:
        print(f"[DEBUG] EXCEPTION: {e}")
        return 500, str(e)

print("=== TEST A: iOS path, af_uid=None, gaid=None ===")
send_af("com.superplaystudios.dicedreams","Hn5qYjVAaRNJYDcwF4LaWF",None,None,"af_kingdom_3_restored",None,None,"ios",None,None)
print()
print("=== TEST B: iOS path, real af_uid, gaid=None ===")
send_af("com.superplaystudios.dicedreams","Hn5qYjVAaRNJYDcwF4LaWF",None,"1777078015955-4325801374339884483","af_kingdom_3_restored",None,None,"ios",None,None)
print()
print("=== TEST C: iOS path, af_uid=None but idfa/idfv set ===")
send_af("com.superplaystudios.dicedreams","Hn5qYjVAaRNJYDcwF4LaWF",None,None,"af_kingdom_3_restored",None,None,"ios","11111111-1111-1111-1111-111111111111","22222222-2222-2222-2222-222222222222")
