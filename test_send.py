#!/usr/bin/env python3
import requests
import json
import time

def send_singular(event_name, aifa, uid, package, app_key, level=None, proxy=None, platform="android", idfa=None, idfv=None):
    base_url = "https://s2s.singular.net/api/v1/evt"
    params = {
        "a": app_key,
        "p": "Android",
        "i": package,
        "aifa": aifa,
        "u": uid if uid else "",
        "utime": int(time.time()),
        "n": event_name
    }
    if level:
        params["level"] = level
    params = {k: v for k, v in params.items() if v}
    print(f"[DEBUG] URL: {base_url}")
    print(f"[DEBUG] Params: {json.dumps(params, indent=2)}")
    headers = {
        "User-Agent": "SingularS2S/1.0",
        "Accept": "application/json"
    }
    try:
        r = requests.get(base_url, params=params, headers=headers, timeout=30)
        print(f"[DEBUG] Final URL: {r.url}")
        print(f"[DEBUG] Response: {r.status_code} - {r.text[:300]}")
        return r.status_code, r.text
    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        return 500, str(e)

# Test with Animals & Coins game data from the reference
print("=" * 60)
print("TEST 1: Singular - Animals & Coins (Android)")
print("=" * 60)
status, resp = send_singular(
    event_name="Reach Level 3",
    aifa="8de8604d-1318-4fd0-907c-402ea9de2529",
    uid="test_user_123",
    package="com.innplaylabs.animalkingdomraid",
    app_key="innplay_labs_33d87c9b",
    level=None,
    platform="android"
)
print(f"\nResult: {status}")

print("\n" + "=" * 60)
print("TEST 2: Singular - iOS (aifa=None)")
print("=" * 60)
status, resp = send_singular(
    event_name="Reach Level 3",
    aifa=None,
    uid="test_user_ios",
    package="com.innplaylabs.animalkingdomraid",
    app_key="innplay_labs_33d87c9b",
    level=None,
    platform="ios",
    idfa="12345678-1234-1234-1234-123456789012",
    idfv="12345678-1234-1234-1234-123456789012"
)
print(f"\nResult: {status}")

print("\n" + "=" * 60)
print("TEST 3: AppsFlyer - Dice Dreams (Android)")
print("=" * 60)
import random, uuid
def send_af(pkg, dev_key, gaid, af_uid, event_name, revenue=None, proxy=None, platform="android", idfa=None, idfv=None):
    url = f"https://api2.appsflyer.com/inappevent/{pkg}"
    current_ts = int(time.time() * 1000)
    DEVICE_MODEL = "SM-S911B"
    OS_VERSION = "Android 14"
    SDK_VERSION = "6.15.0"
    APP_VERSION = "2.3.0"
    payload = {
        "appsflyer_id": af_uid,
        "advertising_id": gaid,
        "eventName": event_name,
        "eventTime": current_ts,
        "eventValue": {},
        "device_model": DEVICE_MODEL,
        "os_version": OS_VERSION,
        "sdk_version": SDK_VERSION,
        "app_version_name": APP_VERSION,
        "network": "WiFi",
        "language": "en-US",
        "timezone": "Asia/Riyadh"
    }
    if revenue:
        payload["eventRevenue"] = str(revenue)
        payload["eventCurrency"] = "USD"
    else:
        level_num = ''.join(filter(str.isdigit, event_name))
        if level_num:
            payload["eventValue"] = {
                "af_level": level_num,
                "af_score": str(random.randint(1000, 50000)),
                "af_duration": str(random.randint(30, 300))
            }
    headers = {
        "Authentication": dev_key,
        "User-Agent": f"AppsFlyer-Android-SDK/{SDK_VERSION} (Linux; Android 14; {DEVICE_MODEL})",
        "Content-Type": "application/json",
        "Accept": "*/*",
    }
    print(f"[DEBUG] URL: {url}")
    print(f"[DEBUG] Payload: {json.dumps(payload, indent=2)}")
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        print(f"[DEBUG] Response: {r.status_code} - {r.text[:300]}")
        return r.status_code, r.text
    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        return 500, str(e)

status, resp = send_af(
    pkg="com.superplaystudios.dicedreams",
    dev_key="Hn5qYjVAaRNJYDcwF4LaWF",
    gaid="8de8604d-1318-4fd0-907c-402ea9de2529",
    af_uid="1777078015955-4325801374339884483",
    event_name="af_kingdom_3_restored",
    platform="android"
)
print(f"\nResult: {status}")

print("\n" + "=" * 60)
print("TEST 4: Adjust - Get Color (Android)")
print("=" * 60)
def send_adj(app_token, event_token, gps_adid, proxy=None):
    url = "https://s2s.adjust.com/event"
    params = {
        "app_token": app_token,
        "event_token": event_token,
        "gps_adid": gps_adid,
        "s2s": "1",
        "created_at": int(time.time())
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    print(f"[DEBUG] URL: {url}")
    print(f"[DEBUG] Params: {json.dumps(params, indent=2)}")
    try:
        r = requests.get(url, params=params, headers=headers, timeout=30)
        print(f"[DEBUG] Final URL: {r.url}")
        print(f"[DEBUG] Response: {r.status_code} - {r.text[:300]}")
        return r.status_code, r.text
    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        return 500, str(e)

status, resp = send_adj(
    app_token="367kicwptj5s",
    event_token="8t8nb3",
    gps_adid="8de8604d-1318-4fd0-907c-402ea9de2529"
)
print(f"\nResult: {status}")
