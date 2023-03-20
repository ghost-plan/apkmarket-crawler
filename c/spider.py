from items import PriceItem
from log import log, handle_parse_exception
import scrapy
from scrapy import Spider
import json


def get_headers():
    headers = {
        'Host': "web-drcn.hispace.dbankcloud.cn",
        "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Accept': "application/json, text/plain, */*",
        "sec-ch-ua-mobile": "?0",
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": '"macOS"',
        "Origin": "https://appgallery.huawei.com",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': "https://appgallery.huawei.com/",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    return headers


class TrackerSpider(Spider):
    """
    https://appgallery.huawei.com/tab/automore%7Cdoublecolumncardwithstar%7C903192%7CPC1000
    """
    name = 'tracker'
    custom_settings = {
        'ITEM_PIPELINES': {
            'a.pipelines.SavePriceItem': 300,
        }
    }

    def start_requests(self):
        log.info("start requests")
        yield scrapy.Request(
            "https://web-drcn.hispace.dbankcloud.cn/uowap/index?method=internal.getTabDetail&serviceType=20&reqPageNum=1&uri=automore%7Cdoublecolumncardwithstar%7C903192%7CPC1000&maxResults=25&zone=&locale=zh",
            headers=get_headers())

    # @handle_parse_exception
    def parse(self, response):
        log.info(f"end response {response.text}")
        t = json.loads(response.text)
        for l in t['layoutData']:
            for d in l['dataList']:
                log.info(d['name'])
        # log.warn(response)
        log.success(f'apk size :{len(t["layoutData"])}')
        yield PriceItem(id=1)
