# -*- coding: utf-8 -*-
import urllib
import scrapy
import json
from TwitterProject.items import TwitterprojectItem
from lxml import etree
from TwitterProject.settings import rupath, IMAGES_STORE
from urllib import request

class TweetSpider(scrapy.Spider):
    name = 'tweet'
    min_pos = ''
    since = '2008-08-1'
    until = '2018-11-11'
    l = 'en'
    user = 'realDonaldTrump'
    first_url = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3A{user}%20since%3A{since}%20until%3A{until}&l={l}'.format(user=user, since=since, until=until, l=l)
    base_url = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&include_available_features=1&include_entities=1&reset_error_state=false&src=typd&max_position={pos}&q=from%3A{user}%20since%3A{since}%20until%3A{until}&l={l}'
    start_urls = [first_url]

    def parse(self, response):
        li_list = response.xpath('//ol[@id="stream-items-id"]/li')
        HTML = ''.join(response.xpath('//ol[@id="stream-items-id"]/li').extract())
        pos = self.parse_pos(li_list)
        url = self.base_url.format(pos=pos, user=self.user, since=self.since, until=self.until, l=self.l)
        yield scrapy.Request(url, callback=self.parse_json, meta={'html': HTML})

    def parse_json(self, response):
        json_data = json.loads(response.text)
        sign = json_data['has_more_items']

        try:
            html = response.meta['html']
        except KeyError:
            html = json_data['items_html']
        '''
        向html中提取信息
        '''
        html = etree.HTML(html)
        li_list = html.xpath('//li[contains(@class, "js-stream-item")]')
        for li in li_list:
            item = TwitterprojectItem()
            tweet_id = li.xpath('./@data-item-id')[0]
            author = ''.join(li.xpath('.//span[@class="FullNameGroup"]//text()')).strip() or ''
            username = ''.join(li.xpath('.//span[@class="username u-dir u-textTruncate"]//text()')).strip() or ''
            content = ''.join(li.xpath('.//div[@class="js-tweet-text-container"]//text()')).strip() or ''
            timestamp = li.xpath('.//span[contains(@class, "js-short-timestamp")]/@data-time-ms')[0] or ''
            img_list = li.xpath('.//div[@class="AdaptiveMediaOuterContainer"]//img/@src')

            user_list = []
            u_list = li.xpath('.//a[@class="twitter-atreply pretty-link js-nav"]')
            if u_list:
                for a in u_list:
                    name = ''.join(a.xpath('.//text()')).strip()
                    id = a.xpath('./@data-mentioned-user-id')[0]
                    user_list.append({name: id})

            topic_list = []
            t_list = li.xpath('.//a[@class="twitter-hashtag pretty-link js-nav"]')
            if t_list:
                for t in t_list:
                    topic = ''.join(t.xpath('.//text()')).strip()
                    topic_list.append(topic)

            item['_id'] = tweet_id
            item['author'] = author
            item['username'] = username
            item['tweet'] = {
                'content': content,
                'timestamp': timestamp,
                'at': user_list,
                'topic': topic_list,
                'img': [{
                    "original_file_name": request.urljoin('https://pbs.twimg.com/', img),
                    "generate_file_name": '',
                    "relative_url_path": rupath,
                    "relative_physical_path": IMAGES_STORE,
                } for img in img_list if img]
            }
            yield item

        self.min_pos = urllib.parse.quote(json_data['min_position'])
        if sign:
            url = self.base_url.format(pos=self.min_pos, user=self.user, since=self.since, until=self.until, l=self.l)
            item = TwitterprojectItem()
            item['_id'] = url
            yield scrapy.Request(url, callback=self.parse_json)

    def parse_pos(self, html):
        id_list = [li.xpath('./@data-item-id').extract_first() for li in html if html]
        pos = "TWEET-{}-{}".format(id_list[-1], id_list[0])
        return pos




