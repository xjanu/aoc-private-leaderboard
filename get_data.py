#!/usr/bin/env python3

import requests
from datetime import datetime, timedelta

URL = "https://adventofcode.com/2021/leaderboard/private/view/{}.json"

wait = timedelta(minutes=15)

def time_ok():
    try:
        with open("data/request.time", "r") as f:
            then = datetime.fromisoformat(f.read())
        now = datetime.now()
        return then + wait < now or then > now
    except:
        return True

def set_time():
    with open("data/request.time", "w") as f:
        f.write(datetime.now().isoformat())

def get_secrets():
    with open("data/secret.txt", "r") as f:
        number = f.readline().strip()
        session = f.readline().strip()
    return number, session

def get_json():
    if not time_ok():
        return
    number, session = get_secrets()
    jar = requests.cookies.cookiejar_from_dict({"session": session})
    response = requests.get(URL.format(number), cookies=jar)
    set_time()
    if response.ok:
        with open("data/scores.json", "w") as f:
            f.write(response.text)

if __name__ == "__main__":
    get_json()