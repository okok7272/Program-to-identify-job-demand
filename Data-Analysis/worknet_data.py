import requests
from bs4 import BeautifulSoup
import pandas as pd


#url 잘게 자르기
url = "http://openapi.work.go.kr/opi/opi/opia/wantedApi.do"
#url ="http://openapi.work.go.kr/opi/opi/opia/wantedApi.do?authKey=WNKXZRZNR5AUCD0GJSCZJ2VR1HK&callTp=L&returnType=XML&startPage=1&display=100&occupation=023|024|025&&region=11000|41130"
serviceKey = "?authKey=WNKXZRZNR5AUCD0GJSCZJ2VR1HK"
Calltp = "&callTp=L"
Return = "&returnType=XML"
StartPage="&startPage=6"
Display = "&display=100"
OCCUPATION = "&occupation=023|024|025"
Region = "&region=11000|41130"

#항목 parsing 함수작성하기
def parse():
    try:
        COMPANY = wanted.find("company").get_text()
        TITLE = wanted.find("title").get_text()
        SAL_TMNM = wanted.find("salTpNm").get_text()
        SAL = wanted.find("sal").get_text()
        REGION = wanted.find("region").get_text()
        HOLIDAY_TPNM = wanted.find("holidayTpNm").get_text()
        MIN_DEUBG = wanted.find("minEdubg").get_text()
        CAREER = wanted.find("career").get_text()
        return {
            "회사명":COMPANY,
            "체용제목":TITLE,
            "임금형태":SAL_TMNM,
            "급여":SAL,
            "근무지역":REGION,
            "근무형태":HOLIDAY_TPNM,
            "최소학력":MIN_DEUBG,
            "경력":CAREER,
        }
    except AttributeError as e:
        return {
            "회사명":None,
            "체용제목":None,
            "임금형태":None,
            "급여":None,
            "근무지역":None,
            "근무형태":None,
            "최소학력":None,
            "경력":None,
        }
 
#parsing 하기
result = requests.get(url+serviceKey+Calltp+Return+StartPage+Display+OCCUPATION+Region)
soup = BeautifulSoup(result.text,'lxml-xml')
wanteds = soup.find_all("wanted")
 
row = []
for wanted in wanteds:
    row.append(parse()) 
 
#pandas 데이터프레임에 넣기
df = pd.DataFrame(row)

df.to_csv("서울_성남_개발자_채용정보_6.csv",mode='w',encoding='utf-8')