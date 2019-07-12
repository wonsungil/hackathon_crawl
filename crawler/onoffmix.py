# -*- coding: utf-8 -*-
import requests

from utils.common_utils import *
from bs4 import BeautifulSoup

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
                    start_date = ""
                    end_date = ""
                    start_time = ""
                    end_time = ""
                    place = span_place.text if not is_none(span_place) else ""

                    print(span_date)
                    print(span_place)


                    event = {
                        "link": link.strip(),
                        "thumbnail": thumbnail.strip(),
                        "title": title.strip(),
                        "payment_type": payment_type.strip(),
                        "category_type" : category_type.strip(),
                        "start_date": start_date.strip(),
                        "end_date": end_date.strip(),
                        "start_time": start_time.strip(),
                        "end_time": end_time.strip(),
                        "place": place.strip()
                    }

                    result.append(event)
                    print(event)
            else:
                print("http error")

OnOffMix().crawling()