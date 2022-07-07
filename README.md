# sejong-univ-auth ![Python versions](https://img.shields.io/badge/Python-3.7-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.3.4-red)

<p align="center">
  <img width="25%" alt="sejong-univ-auth image" src="https://user-images.githubusercontent.com/47492535/177720510-4f7d28aa-8c3d-46a1-b28e-12e24a2e5893.png" >
	<br /> 
	<b>Sejong University Member Account Authentication</b>
	<br /> 
</p>

세종대학교 구성원인지 확인하기 위한 간편한 인증 라이브러리입니다.

**Python**이라면 아래와 같은 방법으로 쉽게 구현해보세요!

혹시 **다른 언어**를 사용하시나요? 그렇다면 [저희들이 직접 개발한 REST API](https://github.com/iml1111/sejong-univ-auth#sejong-auth-api)를 사용해보세요!

<br />

## Easy to install

**Pip**: `pip install sejong-univ-auth`

**Direct:**

- `git clone https://github.com/iml1111/sejong-univ-auth`
- `python setup.py install`

## Easy to use

```python
>>> from sejong_univ_auth import auth
>>> result = auth(id='16011089', password='<my-password>')
>>> result.is_auth
True
```

## Usage

세종대학교에는 다양한 웹 서비스가 있고, 하나의 포탈 멤버 계정을 통해 인증을 수행합니다.

해당 라이브러리의 동작 방식은 **여러 웹 서비스의 인증 동작 구조를 직접 재현하여 대신해서 로그인을 수행해본 후, 해당 결과를 프로그래밍적으로 활용**할 수 있도록 돕습니다.

`sejong_univ_auth`를 사용하기 위한 endpoint 함수는 아래와 같습니다.

```python
def auth(id: str, password: str, methods: Authenticator)
# id, password: 세종대학교 포탈에 로그인하기 위한 계정 정보입니다.
# methods: 어떠한 인증 방식으로 인증을 시도할지 결정합니다. (default=Manual)
```

### Methods

현재 사용가능한 인증 방식(Method)은 아래와 같습니다.

```python
from sejong_univ_auth import (
    Manual,
    PortalSSOToken,
    DosejongSession,
    MoodlerSession,
    ClassicSession
)
```

- **PortalSSOToken**

  - 세종대학교 포탈 사이트의 인증 방식입니다.

- **DosejongSession**

  - dosejong 사이트의 세션 인증 방식입니다.
  - 이름, 학과를 추가로 조회할 수 있습니다.

- **ClassicSession**

  - 대양휴머니티칼리지 사이트의 세션 인증 방식입니다.
  - 함께 조회되는 추가 정보는 다음과 같습니다.
    - 이름
    - 학과
    - 학년
    - 재학/휴학/수료 상태
    - 고전 독서 인증 현황

- **MoodlerSession**

  - SJULMS 사이트의 세션 인증 방식입니다.
  - 이름, 학과를 추가로 조회할 수 있습니다.

- **Manual (default)**
  - 현재 구현된 모든 메소드를 평균 실행 속도가 빠른 순서대로 수행합니다.
  - 인증 성공 및 id/pw 불일치로 인한 인증 실패가 반환될 때까지 순차적으로 실행합니다.

메소드를 직접 지정하는 경우, 아래와 같이 사용할 수 있습니다.

```python
>>> from sejong_univ_auth import PortalSSOToken, DosejongSession, auth
>>> auth(id='<your-id>', password='<your-pw>', methods=PortalSSOToken)
>>> auth(id='<your-id>', password='<your-pw>', methods=DosejongSession)
...
# 복수의 Authenticator를 순차적으로 수행할 경우
>>> auth(id='<your-id>', password='<your-pw>', methods=[PortalSSOToken, DosejongSession])
```

복수의 Authenticator를 list(혹은 tuple) 형태로 주게 될 경우, 순차적으로 메소드를 수행합니다.

만약 현재의 메소드에서 현재 인증이 불가능한(Internel Sever Error 등의) 상황일 경우, 바로 다음 메소드로 시프트하여 인증을 진행합니다.

### AuthResponse

인증의 결과는 Nametuple의 형태로 반환됩니다.

```python
AuthResponse(
	success=True,
	is_auth=True,
	status_code=200,
	code='success',
	body={
		'name': '신희재',
		'major': '컴퓨터공학과'
	},
	authenticator='DosejongSession'
)
```

- **success: 인증 서버 정상 동작 여부**

  - 해당 인증 절차에 대하여 서버는 정상적인 결과를 반환하였습니다.
  - Value: True / False

- **is_auth: 인증 성공 여부**

  - id/pw가 정확하더라도 서버의 상태 이상 및 인증 포맷이 갱신되어 라이브러리의 방식과 상이할 경우 인증 성공을 반드시 보장할 수 없습니다.
  - 인증 결과를 알 수 없을 경우, None이 반환됩니다.
  - Value: True / False / None

- **status_code: 인증 서버의 HTTP status code**
  - Value: int
- **code: Authenticator 반환 코드**
  - 인증이 성공할 경우, 'success'로 통일합니다.
  - 인증이 실패 및 알 수 없을 경우, 각각의 분기에 맞는 코드 값을 반환합니다.
  - Value: string
- **body: 메타데이터**
  - 인증 결과에 관련된 메타데이터를 포함합니다.
    - 인증 실패시의 보다 정확한 실패 사유
    - 이름/학번/학년/재학 상태 등의 추가 정보
  - Value: dict
- **authenticator: 해당 인증에 사용된 Authenticator 클래스**

<br />

# Sejong Auth API

Java, Node 등 다른 언어를 사용중이신 학우분들을 위해 저희들이 개발한 REST API를 사용하실 수 있습니다.

- **단, 해당 API의 경우, 지속적인 지원을 보장할 수 없습니다.**

### Request

**method**의 경우, 기존에 사용가능한 메소드를 "Manual", "DosejongSession"과 같은 형식으로 그대로 입력해주시면 됩니다. 복수의 메소드에 대한 순차적인 호출은 현재 지원되지 않습니다.

```javascript
POST https://auth.imsejong.com/auth HTTP/1.1
Host: auth.imsejong.com
{
    "id": "<학번>",
    "pw": "<비밀번호>",
    "method": "<사용하고자 하는 메소드>"
}
```

### Response

```javascript
{
    "msg": "success",
    "result": {
        "authenticator": "DosejongSession",
        "body": {
            "major": "컴퓨터공학과",
            "name": "신희재"
        },
        "code": "success",
        "is_auth": true,
        "status_code": 200,
        "success": true
    },
    "version": "0.3.3"
}
```

<br />

# Contributors

컨트리뷰트를 원하신다면 [가이드라인](https://github.com/iml1111/sejong-univ-auth/blob/main/CONTRIBUTING.md)을 참고해주세요! 감사합니다! 😀

<p align="center">
  <a href="https://github.com/iml1111/sejong-univ-auth/graphs/contributors">
  	<img src="https://contrib.rocks/image?repo=altmshfkgudtjr/python-oauth-kakao" />
	</a>
	<br /> 
</p>
<br />

# References

- https://pypi.org/project/sejong-univ-auth/
- https://auth.imsejong.com/

