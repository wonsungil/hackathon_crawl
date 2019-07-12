# -*- coding: utf-8 -*-
import requests, re

from utils.common_utils import *
from bs4 import BeautifulSoup
from datetime import datetime

class OnOffMix:
    def __init__(self):
        self.search_url = "https://onoffmix.com/event/main?s=해커톤"
        self.base_url = "https://onoffmix.com/"

    def crawling(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36 NetHelper70"
        }

        with requests.session() as session:
            response = session.get(self.search_url, headers=headers)
            result = []

            if response.status_code == 200:
                bs = BeautifulSoup(response.text, "html.parser")

                event_list = bs.find("ul", {"class": "event_lists"})
                lis = event_list.findAll("li", {"class": ""})

                for each in lis:
                    a_link = each.find("a")
                    div_thumbnail = each.find("div", {"class": "event_thumbnail"})
                    div_event_info_area = each.find("div", {"class": "event_info_area"})
                    h5_title =  div_event_info_area.find("h5") if not is_none(div_event_info_area) else None
                    div_event_info = each.find("div", {"class": "event_info"})
                    span_payment_type = div_event_info.find("span", {"class": "payment_type"}) if not is_none(div_event_info) else None
                    span_category_type = div_event_info.find("span", {"class": "category_type"}) if not is_none(div_event_info) else None
                    list_date_place = each.find("div", {"class": "list_date_place"})
                    span_date = each.find("span",{"class": "date"}) if not is_none(list_date_place) else None
                    span_place = each.find("span", {"class": "place"}) if not is_none(list_date_place) else None

                    link = self.base_url + a_link["href"] if not is_none(a_link) else ""
                    thumbnail = div_thumbnail.find("img")["src"] if not is_none(div_thumbnail) else ""
                    title = h5_title.text if not is_none(h5_title) else ""
                    payment_type = span_payment_type.text if not is_none(span_payment_type) else ""
                    category_type = span_category_type.text if not is_none(span_category_type) else ""
                    date = span_date.text.split("~") if not is_none(span_date) else None
                    start_date = datetime.strptime(re.sub(r"[^\d]", "", date[0]), "%Y%m%d%H%M") if not is_none(date) else ""

                    if is_none(date[1]):
                        end_date = ""
                    elif len(date[1]) < 10:
                        end_date = datetime.strptime(start_date.strftime("%Y%m%d")+str(date[1].strip()), "%Y%m%d%H:%M")
                    else:
                        end_date = datetime.strptime(re.sub(r"[^\d]", "", date[1]), "%Y%m%d%H%M")

                    place = span_place.text if not is_none(span_place) else ""

                    event = {
                        "link": link.strip(),
                        "thumbnail": thumbnail.strip(),
                        "title": title.strip(),
                        "payment_type": payment_type.strip(),
                        "category_type" : category_type.strip(),
                        "start_date": start_date.strftime("%Y-%m-%d") if start_date != "" else "",
                        "end_date": end_date.strftime("%Y-%m-%d") if end_date != "" else "",
                        "start_time": start_date.strftime("%H:%M") if start_date != "" else "",
                        "end_time": end_date.strftime("%H:%M") if end_date != "" else "",
                        "place": place.strip()
                    }

                    result.append(event)
                    print(event)
            else:
                print("http error")

OnOffMix().crawling()