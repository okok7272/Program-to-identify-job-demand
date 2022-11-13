import urllib
import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
#회사 수에 따라 페이지 수 설정 때문에 필요
#first_url = 'https://www.jobkorea.co.kr/Search/?stext=AI&tabType=recruit&Page_No=1'
import time
page_order = 1

#content > div > div > div.cnt-list-wrap > div > div.recruit-info > div.list-filter-wrap > p > strong

#https://www.jobkorea.co.kr/Search/?stext=%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%94%EB%93%9C

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
    df = pd.DataFrame({'회사명' : name, '채용제목' : detail, '근무지역' : location, '최소학력' : edu, '근무형태' : employment_type ,'경력' : personal_history , '모집기간' : datetime})
    return df

#해당 함수 구조
            # "회사명":COMPANY,
            # "체용제목":TITLE,
            # "임금형태":SAL_TMNM,
            # "급여":SAL,
            # "근무지역":REGION,
            # "근무형태":HOLIDAY_TPNM,
            # "최소학력":MIN_DEUBG,
            # "경력":CAREER,
#해당 구조와 비슷하게 데이터 받기 

AI_df = pd.DataFrame(columns=['회사명', '채용제목', '근무지역', '최소학력', '근무형태', '경력', '모집기간'])

def auto_crawling(keyword):
    page_num = page_number(keyword, 1)
    for i in range(page_num):
        temp_df = crawl(keyword, i)
        #페이지 켜지는 시간 넣기 sleep으로
        time.sleep(4)
        AI_df.append(temp_df,sort=False, ignore_index = True)
#https://www.jobkorea.co.kr/Search/?stext=%EA%B7%B8%EB%A1%9C%EC%8A%A4%20%EB%A7%88%EC%BC%80%ED%8C%85
auto_crawling('%EA%B7%B8%EB%A1%9C%EC%8A%A4%20%EB%A7%88%EC%BC%80%ED%8C%85')