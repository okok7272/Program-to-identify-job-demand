import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import psycopg2
import os
import re
import time
import urllib
from urllib.request import Request, urlopen
# engine = sqlalchemy.create_engine("postgresql://user:password@host:port/database")

#url 잘게 자르기
url = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do"
#url ="http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKXZRZNR5AUCD0GJSCZJ2VR1HK&callTp=L&returnType=XML&startPage=1&display=100&occupation=023|024|025&&region=11000|41130"
serviceKey = "?authKey=WNKXZRZNR5AUCD0GJSCZJ2VR1HK"
Calltp = "&callTp=L"
Return = "&returnType=XML"
StartPage="&startPage=6"
Display = "&display=100"
OCCUPATION = "&occupation=023|024|025"
#Region = "&region=11000|41130"

def pg_connect(user, password, db, host, port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)
    return create_engine(url, client_encoding='utf8')
    return engine


def worknet_jobSearch():

    result = requests.get(url+serviceKey+Calltp+Return+StartPage+Display+OCCUPATION)
    soup = BeautifulSoup(result.text,'lxml-xml')
    wanteds = soup.find_all("wanted")
    worknet_dataframe =pd.DataFrame()
    for wanted in wanteds:
        COMPANY = wanted.find("company").get_text()
        TITLE = wanted.find("title").get_text()
        SAL_TMNM = wanted.find("salTpNm").get_text()
        SAL = wanted.find("sal").get_text()
        REGION = wanted.find("region").get_text()
        HOLIDAY_TPNM = wanted.find("holidayTpNm").get_text()
        MIN_DEUBG = wanted.find("minEdubg").get_text()
        CAREER = wanted.find("career").get_text()
        regDt = wanted.find("regDt").get_text()

        df = pd.DataFrame({
        "회사명":COMPANY,
        "체용제목":TITLE,
        "임금형태":SAL_TMNM,
        "급여":SAL,
        "근무지역":REGION,
        "근무형태":HOLIDAY_TPNM,
        "최소학력":MIN_DEUBG,
        "경력":CAREER,
        "등록일자":regDt,
        }, index = [0])

        worknet_dataframe = pd.concat([worknet_dataframe, df])
    
    # con = psycopg2.connect(host='localhost', dbname='worknet',user='postgres',password='1234',port=5432)
    engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/worknet")
    conn = engine.connect()
    # host = 'localhost'
    # user = 'postgres'
    # db_name = 'worknet'
    # passwrd = '1234'
    #pg_engine = pg_connect(user, passwrd, db_name, host)
    worknet_dataframe.to_sql('worknet', if_exists= 'append', con= engine)
    conn.close()

    return worknet_dataframe

worknet_jobSearch()
