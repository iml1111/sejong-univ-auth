"""
과거에는 동작했으나 현재는 동작하지 않는 모듈들...
"""

import requests
from bs4 import BeautifulSoup as bs
import getpass

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
            AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept":"text/html,application/xhtml+xml,application/xml;\
            q=0.9,imgwebp,*/*;q=0.8"}
TIMEOUT_SEC = 3


def dosejong_api(id, pw):
    data = {
            #POST
            "email":id,
            "password":pw
            }
    with requests.Session() as s:
        html = s.post("https://do.sejong.ac.kr/ko/process/member/login", headers = header, data = data, timeout=TIMEOUT_SEC).content
        html = s.get("https://do.sejong.ac.kr/", timeout=TIMEOUT_SEC).text
        soup = bs(html, "html.parser")
        soup = soup.select("div.info")
        if soup == []: return {"result": False}
        name = soup[0].find("b").get_text().strip()
        major = soup[0].find("small").get_text().strip().split(" ")[1]
        return {
            "result":True,
            "name":name,
            "id":id,
            "major":major
        }



def uis_api(id, pw):
    uis_header = {
    "Referer": "https://portal.sejong.ac.kr",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
    }
    LOGIN_INFO = {
        'id': id,
        'password': pw,
        'rtUrl': '',
    }
    with requests.Session() as s:
        s.post(
            'https://portal.sejong.ac.kr/jsp/login/login_action.jsp', 
            headers=uis_header,
            data=LOGIN_INFO,
            timeout=TIMEOUT_SEC
        )
        res = s.get('https://portal.sejong.ac.kr/main.jsp', timeout=TIMEOUT_SEC)
        soup = bs(res.content, 'html.parser')
        name = soup.select_one('div.info0 > div').get_text().split("(")[0]
        if name is None: 
            return {"result":False}
        return {
            "result":True,
            "name":name,
            "id":id,
            "major":"none"
        }


def sjlms_api(id, pw):
    # 현재 작동하지 않음
    data = {"username":id, "password":pw, "rememberusername":"1"}
    with requests.Session() as s:
        page = s.post("http://sjulms.moodler.kr/login/index.php", 
            headers = header, data = data, timeout=TIMEOUT_SEC)
        soup = bs(page.text, "html.parser")
        if soup.find("h4") is None:
            return {"result":False}
        else:
            name = soup.find("h4").get_text()
            major = soup.find("p",{"class":"department"}).get_text()
            return {
            "result":True,
            "name":name,
            "id":id,
            "major":major
            }



if __name__ == '__main__':
    id = input("학교 아이디: ")
    pw = getpass.getpass("비밀번호: ")
    print(dosejong_api(id,pw))
    print(sjlms_api(id,pw))
    print(uis_api(id, pw))