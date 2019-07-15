# -*- coding: utf-8 -*-
import requests, re, json

from utils.common_utils import *
from bs4 import BeautifulSoup
from datetime import datetime

class EventUs:
    def __init__(self):
        self.search_url = "https://event-us.kr/UserHelpers/SearchProjectList"
        self.base_url = "https://onoffmix.com/"

    def crawling(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 NetHelper70"
        }

        params = {
            "search": "해커톤",
            "category": "Non",
            "area": "All",
            "cost": "All",
            "size": "0",
            "endSize": "0",
            "work": "new",
            "num": 12,
        }

        with requests.session() as session:
            response = session.post(self.search_url, headers=headers, data=params)
            result = []

            if response.status_code == 200:
                data = json.loads(response.text)["data"]

                for item in data:
                    # FIXME timestamp to utc
                    # date = re.sub(r"[^\d]", "", item["StartDate"])
                    # print(date)
                    # print(datetime.fromtimestamp(float(date)))

                    event = {
                        "link": "https://event-us.kr/pathfinder/event/" + item["ProjectId"],
                        "thumbnail": "https://eventusstorage.blob.core.windows.net/evs" + item["CoverImageUrl"],
                        "title": item["Title"],
                        "payment_type": item["IsCost"],
                        "category_type": item["Category"],
                        "start_date": item["StartDate"],
                        "end_date": "",
                        "start_time": "",
                        "end_time": "",
                        "place": item["Area_Detail"],
                        "is_close":item["IsClose"]
                    }
                    result.append(event)
                    print(event)
EventUs().crawling()