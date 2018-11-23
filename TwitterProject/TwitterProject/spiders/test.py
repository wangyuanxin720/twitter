import random
import urllib

from lxml import etree
import requests
# pos = "TWEET-1262827186-1266874329"

url1 = 'https://twitter.com/search?f=tweets&vertical=default&q=from%3Agreta%20since%3A2008-08-28%20until%3A2009-03-02&l=en'

HEADERS_LIST = [
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; x64; fr; rv:1.9.2.13) Gecko/20101203 Firebird/3.6.13',
    'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Mozilla/5.0 (Windows NT 5.2; RW; rv:7.0a1) Gecko/20091211 SeaMonkey/9.23a1pre'
]

HEADER = {'User-Agent': random.choice(HEADERS_LIST)}
pos = 'cm%2B55m-aEsIsDbvDv-aEFFIbvXEJ'
url = 'https://twitter.com/i/search/timeline?f=tweets&vertical=default&include_available_features=1&include_entities=1&reset_error_state=false&src=typd&max_position={pos}&q={q}&l={lang}'.format(pos=pos, q='from%3Agreta%20since%3A2008-08-28%20until%3A2009-03-02', lang='en')
# print(url)
response = requests.get(
    url1,
    proxies={'http': '127.0.0.1:1087', 'https': '127.0.0.1:1087'},
    headers=HEADER,
)
# print(response.text)
a = urllib.parse.quote('cm+55m-aEsIsDbvDv-aEFFIbvXEJ')
html = etree.HTML(response.text)
content_list = html.xpath('//ol[@id="stream-items-id"]//li')
id_list = []
for li in content_list:
    id = li.xpath('./@data-item-id')
    if id:
        id_list.append(id[0])

# print(id_list)