# sejong-univ-auth
Sejong University Member Account Authentication

# How to Use
## Local
```{.python}
$ python sj_auth.py
$ 학교 아이디: <학번 입력>
$ 비밀번호: <비밀번호 입력>

//do.sejong.ac.kr Crawling
{'result': True, 'name': '김희재', 'id': '16011229', 'major': '컴퓨터공학과'}

//sjulms.moodler.kr Crawling
{'result': True, 'name': '김희재', 'id': '16011229', 'major': '컴퓨터공학과'}
...
```
## Python Import
```{.python}
>>> from sj_auth import dosejong_api, sjlms_api
>>> dosejong_api(id,pw)
{'result': True, 'name': '김희재', 'id': '16011229', 'major': '컴퓨터공학과'}
>>> sjlms_api(id,pw)
{'result': True, 'name': '김희재', 'id': '16011229', 'major': '컴퓨터공학과'}
>>> uis_api(id,pw)
{'result': True, 'name': '김희재', 'id': '16011229', 'major': 'none'}
```
