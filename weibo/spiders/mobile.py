# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import WeiboItem
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Join


class MobileSpider(scrapy.Spider):
    name = 'mobile'
    allowed_domains = ['weibo.cn']
    cookie = ''  # login and then populate cookie here
    cookies = {}
    for i in cookie.strip().split(';'):
        element = i.split('=')
        cookies[element[0].strip()] = element[1]
    headers = {
        'Host': 'm.weibo.cn',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Accept-Language': 'zh - CN, zh;q = 0.9, en;q = 0.8',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    def start_requests(self):
        url = 'https://m.weibo.cn/feed/friends?version=v4'
        return [scrapy.Request(url, cookies=self.cookies, headers=self.headers, callback=self.parse)]

    def parse(self, response):
        json_data = json.loads(response.text)
        twitters = json_data[0]['card_group']
        for twitter in twitters:
            if twitter.get('mblog'):
                loader = ItemLoader(item=WeiboItem())
                loader.default_output_processor = Join()
                try:
                    loader.add_value('user_name', twitter['mblog']['user']['screen_name'])
                    loader.add_value('time', twitter['mblog']['created_at'])
                    loader.add_value('comments', str(twitter['mblog']['comments_count']))
                    loader.add_value('likes', str(twitter['mblog']['attitudes_count']))
                    loader.add_value('text', twitter['mblog']['text'])
                    if twitter['mblog'].get('retweeted_status'):
                        loader.add_value('type', '转发')
                    elif twitter['mblog'].get('page_info'):
                        if twitter['mblog']['page_info'].get('video_details'):
                            loader.add_value('type', '视频')
                        else:
                            loader.add_value('type', '原创')
                    else:
                        loader.add_value('type', '原创')
                    yield loader.load_item()
                except KeyError:
                    self.logger.error('KeyError')
            else:
                self.logger.info('No mblog key')
        # go to next link
        next_link = json_data[0]['next_cursor']
        yield scrapy.Request('https://m.weibo.cn/feed/friends?version=v4&next_cursor={}&page=1'.format(str(next_link)), callback=self.parse)
