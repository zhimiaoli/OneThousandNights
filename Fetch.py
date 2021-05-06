import sys
import requests
from jinja2 import Template
from datetime import datetime


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
<itunes:category>人文</itunes:category>
{% for episode in episodes %}
<item>
    <title>{{episode['title']}}</title>
    <itunes:summary>{{episode['episodeDetail']['share_desc']}}</itunes:summary>
    <description><![CDATA[ {{episode['episodeDetail']['share_desc']}} <br> 标签:{{episode['episodeDetail']['tag']}} <br>{{episode['episodeDetail']['content'] | safe}}]]> </description>
    <link>{{episode['share_url']}}</link>
    <enclosure url="{{episode['media_key_full_url']}}" type="audio/mpeg" length="{{episode['media_size']}}"></enclosure>
    <pubDate>{{episode['pubDate']}}</pubDate>
    <itunes:author>梁文道</itunes:author>
    <itunes:duration>{{episode['duration_str']}}</itunes:duration>
    <itunes:explicit>no</itunes:explicit>
    <guid>{{episode['article_id']}}</guid>
</item> 
{% endfor %}
</channel>
</rss>
"""


def fetchepisodes():
    req = requests.session()
    action = "https://api.vistopia.com.cn/api/v1/content/article_list?api_token=null&content_id=6&api_token=null&count=1001"
    resp = req.get(action)
    episodes = []
    if resp.status_code == 200:
        podcasts_data = resp.json()
        for episode in podcasts_data['data']['article_list']:
            episodeDetail = fetchepisodeDetail(episode['article_id'])
            print("fething episodes"+episode['title'])
            episode['pubDate'] = datetime.fromtimestamp(int(episode['media_key'][:-4])/1000).strftime("%a, %d %b %Y %H:%M:%S %z")
            # guess real update time from filename, media_key field.
            episode['episodeDetail'] = episodeDetail['data']['part'][0]
            # attach essential episode detail to episode params.
            episodes.append(episode)
        #print(episodes)
        return episodes
    else:
        sys.exit()
    pass

def fetchepisodeDetail(episodeID):
    # 抓取每篇文章描述
    resp = requests.get("https://api.vistopia.com.cn/api/v1/reader/section-detail?api_token=&article_id="+episodeID)
    if resp.status_code == 200:
        return resp.json()
    else:
        sys.exit()

def main():
    episodes = fetchepisodes()
    xml = Template(feed_template).render(episodes = episodes)
    with open("feed.xml",'w',encoding='utf-8') as xmlFile:
        xmlFile.write(xml)
    print("Done.")

if __name__ == '__main__':
    main()