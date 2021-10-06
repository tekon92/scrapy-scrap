#merge everything

import pprint
import json
import requests
from scrapy import Selector
pp = pprint.PrettyPrinter(indent=2)
# main_url = ''


def get_content(url):
  """request to get source code"""
  # main_url = url
  return Selector(text=requests.get(url).content)

def generate_url(url):
  """get list of URL"""
  get_title(url)
  return get_content(url).css('div.zox-art-title a::attr(href)').extract()

def get_news_detail(url):
  """parse news detail"""
  news = {}
  nc = get_content(url)

  news['url'] = url
  news['title'] = nc.css('h1::text').extract_first()
  news['author'] = nc.css('div.zox-author-name-wrap > span > a::text').extract_first()
  news['published'] = nc.css('div.zox-post-date-wrap > span > time::attr(datetime)').extract_first()
  news['content'] = nc.css('div.zox-post-body p::text').extract()

  return news

def get_title(url):
  """get dynamic title"""
  return 'news2scrape'+'_'+url.split('/')[-2] if (url.split('/')[-2].isnumeric()) else 'news2scrape'

def write_to_json(data):
  """write into json file"""
  # title = 'news2scrape'+'_'+url.split('/')[-2] if (url.split('/')[-2].isnumeric()) else 'news2scrape'
  with open("news2scrape.json", "w") as file:
    file.write(json.dumps(data))


def get_scrape(url):
  """call all functions"""
  url = generate_url(url)
  data = []

  for i in url:
    data.append(get_news_detail(i))

  for q in data[0:10]:
    pp.pprint(q)

  write_to_json(data[0:10])
