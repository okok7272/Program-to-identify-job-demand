import urllib
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
#회사 수에 따라 페이지 수 설정 때문에 필요
#first_url = 'https://www.jobkorea.co.kr/Search/?stext=AI&tabType=recruit&Page_No=1'

page_order = 1

#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.list-filter-wrap > p > strong



base_url = 'http://www.jobkorea.co.kr/Search/?stext={}&tabType=recruit&Page_No={}'

def page_number(keyword, page_num):
    keyword = urllib.parse.quote(keyword)
    url = base_url.format(keyword,page_num)
    response = urllib.request.urlopen(url)
    soup = bs(response,'html.parser')
    text_num = soup.select_one("div.recruit-info > div.list-filter-wrap > p > strong").text
    trans_num = re.sub(r'[^0-9]', '', text_num)
    real_num = int(trans_num)
    return real_num

print(page_number('AI', 1))

def crawl(keyword, page_num):
    keyword = urllib.parse.quote(keyword)
    url = base_url.format(keyword,page_num)
    response = urllib.request.urlopen(url)
    soup = bs(response,'html.parser')
    name = [element.text for element in soup.select("a.name")][:19]
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span.exp
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span.edu
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span:nth-child(3)
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span.loc.short
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span.loc.long
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > p.option > span.date
    #content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li.list-post.active > div > div.post-list-info > a > strong
    personal_history = [element.text for element in soup.select("div.post-list-info > p.option > span.exp")][:19]
    edu= [element.text for element in soup.select("div.post-list-info > p.option > span.edu")][:19]
    employment_type = [element.text for element in soup.select("div.post-list-info > p.option > span:nth-child(3)")][:19]
    location = [element.text for element in soup.select("div.post-list-info > p.option > span.loc.long")][:19]
    datetime = [element.text for element in soup.select("div.post-list-info > p.option > span.date")][:19]
    detail = [element.text for element in soup.select("div.post-list-info > a.title")][:19]
    detail = [element.replace("\n","").replace("\r","") for element in detail]
    df = pd.DataFrame({'기업 이름' : name, '경력' : personal_history ,'자세 내용' : detail})
    return df

