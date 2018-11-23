from urllib import request
from TwitterProject.settings import rupath,FILES_STORE
from lxml import etree
from TwitterProject.items import TwitterprojectItem

def parse_li(li_list):
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
                "original_file_name": '',
                "generate_file_name": request.urljoin('https://pbs.twimg.com/', img),
                "relative_url_path": rupath,
                "relative_physical_path": FILES_STORE,
            } for img in img_list if img]
        }
        yield item


def parse(html):
    Html = etree.HTML(html)
    li_list = Html.xpath('//li[contains(@class, "js-stream-item")]')
    parse_li(li_list)
    id_list = [li.xpath('./@data-item-id')[0] for li in li_list if li]
    pos = "TWEET-{}-{}".format(id_list[-1], id_list[0])
    return pos

