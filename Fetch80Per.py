import sys
import requests
from jinja2 import Template
from datetime import datetime, timedelta
import time

# rss feed xml get from https://2021.jackbarber.co.uk/blog/2017-02-14-podcast-rss-feed-template
feed_template = """<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
<channel>
<title>八分 - 梁文道</title>
<link>https://shop.vistopia.com.cn/detail?id=2H2iF</link>
<language>zh-cn</language>
<itunes:subtitle>梁文道-八分</itunes:subtitle>
<itunes:author>梁文道</itunes:author>
<itunes:summary>梁文道-八分</itunes:summary>
<description><![CDATA[ 梁文道-八分 ]]> </description>
<itunes:owner>
    <itunes:name>梁文道-看理想</itunes:name>
    <itunes:email>podcast@miao.li</itunes:email>
</itunes:owner>
<itunes:explicit>no</itunes:explicit>
<itunes:image href="https://cdn.vistopia.com.cn/1535342540956.png" />
<itunes:category>人文</itunes:category>
{% for episode in episodes %}
<item>
    <title>{{episode['title']}}</title>
    <itunes:summary>{{episode['episodeDetail']['share_desc']}}</itunes:summary>
    <description><![CDATA[ 标签:{{episode['episodeDetail']['tag']}} <br> 在看理想app中查看 <br> <a href="{{episode['share_url']}}">{{episode['share_url']}}</a><br>{{episode['episodeDetail']['content'] | safe}}]]> </description>
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
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
req = requests.session()
req.headers = headers

def fetchepisodes():

    action = "https://api.vistopia.com.cn/api/v1/content/article_list?api_token=null&content_id=11&catalog_id=1138&api_token=null&count=1001"
    resp = req.get(action)
    episodes = []
    if resp.status_code == 200:
        podcasts_data = resp.json()
        current_updateDate,pre_updateDate = datetime.now() - timedelta(days=6650), datetime.now() - timedelta(days=6650)
        dt = timedelta(days=1)
        # airingDate = podcasts_data['data']['article_list'][0]['']
        for episode in podcasts_data['data']['article_list']:
            episodeDetail = fetchepisodeDetail(episode['article_id'])
            print("fething episodes: "+episode['title'])
            pdatetime = episodeDetail['data']['part'][0]['update_date']
            current_updateDate= datetime.strptime(pdatetime,"%Y.%m.%d")
            episode['pubDate'] = current_updateDate.strftime("%a, %d %b %Y %H:%M:%S %z")
            # guess real update time from filename, media_key field.
            episode['episodeDetail'] = episodeDetail['data']['part'][0]
            # attach essential episode detail to episode params.
            episodes.append(episode)
            time.sleep(5);
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
    with open("feed-11.xml",'w',encoding='utf-8') as xmlFile:
        xmlFile.write(xml)
    print("Done.")

if __name__ == '__main__':
    main()
