#!/usr/bin/env python3

from getToken import APIClient
from datetime import datetime, timezone
import csv
import os
import math
import requests
import random

org_id = os.getenv("org_id")
api_key = os.getenv("api_key")
camera_id = os.getenv("camera_id")
event_type_uid = os.getenv("event_type_uid")
auth_url = "https://api.verkada.com/token"
helix_url = f'https://api.verkada.com/cameras/v1/video_tagging/event?org_id={org_id}'

def get_time():
    dt = datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    now = math.trunc(utc_timestamp) * 1000
    return now

def fruit_scan():
    with open('priceList.csv', newline='') as priceList:
        fp = list(csv.DictReader(priceList))
        row = random.choice(fp)
        fruit = row['fruit']
        price = row['price']
    return fruit, price

def send_to_helix():
    client = APIClient(api_key, auth_url)
    token = client.get_api_token()
    now = get_time()
    fruit, price = fruit_scan()
    headers = { 
        "x-verkada-auth": token,
        "accept": "application/json"
    }
    json ={
        "attributes": {
            "item": fruit,
            "price": float(price)
        },
        "event_type_uid": event_type_uid,
        "camera_id": camera_id,
        "flagged": False,
        "time_ms": now
    }
    response = requests.post(url=helix_url, headers=headers, json=json)
    return response

scan = send_to_helix()