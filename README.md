# sejong-univ-auth ![Python versions](https://img.shields.io/badge/Python-3.6<=@-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.1.1-red)
**Sejong University Member Account Authentication**

세종대학교 구성원인지 확인하기 위한 간편한 인증 라이브러리



## Easy to install

**Pip**: `pip install sejong-univ-auth`

**Direct:**

- `git clone https://github.com/iml1111/sejong-univ-auth`
- `python setup.py install`



## Easy to use

```python
>>> from sejong_univ_auth import auth
>>> result = auth(id='16011089', password='<your-password>')
>>> result.is_auth
True
```

