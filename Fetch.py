import sys
import requests
from jinja2 import Template


# rss feed xml get from https://2021.jackbarber.co.uk/blog/2017-02-14-podcast-rss-feed-template
feed_template = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>一千零一夜 - 梁文道</title>
<link>https://shop.vistopia.com.cn/detail?id=2H2iF</link>
<language>zh-cn</language>
<itunes:subtitle>回到人间的读书节目</itunes:subtitle>
<itunes:author>梁文道</itunes:author>
<itunes:summary>只有晚上，只在街头；梁文道导读，回到人间的读书节目。</itunes:summary>
<description>只有晚上，只在街头；梁文道导读，回到人间的读书节目。</description>
<itunes:owner>
    <itunes:name>梁文道-看理想</itunes:name>
    <itunes:email>me@example.com</itunes:email>
</itunes:owner>
<itunes:explicit>no</itunes:explicit>
<itunes:image href="https://cdn.vistopia.com.cn/1535342540956.png" />
<itunes:category text="人文"/></itunes:category>
{% for eposide in eposides %}
<item>
    <title>{{eposide['title']}}</title>
    <itunes:summary>{{eposide['eposideDetail']['share_desc']}}</itunes:summary>
    <description><![CDATA[ {{eposide['eposideDetail']['share_desc']}} <br> 标签:{{eposide['eposideDetail']['tag']}} <br>{{eposide['eposideDetail']['content'] | safe}}]]> </description>
    <link>{{eposide['share_url']}}</link>
    <enclosure url="{{eposide['media_key_full_url']}}" type="audio/mpeg" length="{{eposide['media_size']}}"></enclosure>
    <pubDate>{{eposide['eposideDetail']['update_date'] | replace(".","/")}}</pubDate>
    <itunes:author>梁文道</itunes:author>
    <itunes:duration>{{eposide['duration_str']}}</itunes:duration>
    <itunes:explicit>no</itunes:explicit>
    <guid>{{eposide['article_id']}}</guid>
</item> 
{% endfor %}
</channel>
</rss>
"""


def fetchEposides():
    req = requests.session()
    action = "https://api.vistopia.com.cn/api/v1/content/article_list?api_token=null&content_id=6&api_token=null&count=1001"
    resp = req.get(action)
    eposides = []
    if resp.status_code == 200:
        podcasts_data = resp.json()
        for eposide in podcasts_data['data']['article_list']:
            eposideDetail = fetchEposideDetail(eposide['article_id'])
            print("fething eposides"+eposide['title'])
            eposide['eposideDetail'] = eposideDetail['data']['part'][0]
            eposides.append(eposide)
        #print(eposides)
        return eposides
    else:
        sys.exit()
    pass

def fetchEposideDetail(eposideID):
    # 抓取每篇文章描述
    resp = requests.get("https://api.vistopia.com.cn/api/v1/reader/section-detail?api_token=&article_id="+eposideID)
    if resp.status_code == 200:
        return resp.json()
    else:
        sys.exit()

def main():
    eposides = fetchEposides()
    xml = Template(feed_template).render(eposides = eposides)
    with open("feed.xml",'w',encoding='utf-8') as xmlFile:
        xmlFile.write(xml)
    print("Done.")

if __name__ == '__main__':
    main()