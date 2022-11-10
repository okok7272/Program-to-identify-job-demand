#https://www.jobkorea.co.kr/Search/?stext=PM&careerType=1&edu=0&Page_No=1

import urllib

from bs4 import BeautifulSoup as bs

import pandas as pd

#https://www.jobkorea.co.kr/Search/?stext=PM&careerType=1&edu=0&Page_No=1&tabType=recruit

base_url = 'http://www.jobkorea.co.kr/Search/?stext={}&tabType=recruit&Page_No={}'

#num
#content > div > div > div.cnt-list-wrap.topLine > div > div.recruit-info > div.list-filter-wrap > p > strong
#name
##content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li:nth-child(1) > div > div.post-list-corp > a
#채용형태
#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li:nth-child(1) > div > div.post-list-info > p.option > span:nth-child(3)
#모집기간
#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.lists > div > div.list-default > ul > li:nth-child(1) > div > div.post-list-info > p.option > span.date
def crawl(keyword, page_num):
    keyword = urllib.parse.quote(keyword)
    url = base_url.format(keyword,page_num)
    response = urllib.request.urlopen(url)
    soup = bs(response,'html.parser')
    name = [element.text for element in soup.select("a.name")][:19]
    detail = [element.text for element in soup.select("div.post-list-info > a.title")][:19]
    detail = [element.replace("\n","").replace("\r","") for element in detail]
    df = pd.DataFrame({'기업 이름' : name, '자세 내용' : detail})
    return df