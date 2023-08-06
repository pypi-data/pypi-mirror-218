#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# tr!bf tribf@tribf.com

import requests
from requests.adapters import HTTPAdapter

s = requests.Session()
s.mount("https://", HTTPAdapter(pool_connections=1, pool_maxsize=50))
s.mount("http://", HTTPAdapter(pool_connections=1, pool_maxsize=50))


def req_post_json(url, data):
    min_time = 0.9
    try:
        r = s.post(url, headers={"Content-type": "application/json"}, json=data)
        r.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    except requests.RequestException as e:
        print(e)
        return
    else:
        time_out = r.elapsed.total_seconds()
        if time_out > min_time:
            print(time_out)

    content = r.content.decode(encoding="UTF-8")
    return content


def main():
    print(req_post_json("http://172.16.10.96:54000/getTrainingTaskStatus", {}))


if __name__ == "__main__":
    main()
