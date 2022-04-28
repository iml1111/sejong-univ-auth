# sejong-univ-auth ![Python versions](https://img.shields.io/badge/Python-3.7-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.1.1-red)
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

- **PortalSSOToken**

​		세종대학교 포탈 사이트의 ssotoken 유무를 통해 인증 결과를 확인합니다.

- **DosejongSession**

  dosejong 사이트의 세션 정보를 유지하여, 사용자의 이름/학번 등의 scraping을 시도하여 인증 유무를 확인합니다. 따라서 해당 메소드의 경우, 인증에 성공할 경우 해당 아이디의 이름 및 학번을 함께 조회할 수 있습니다.

- **Manual**

​		현재 구현된 모든 메소드를 순서대로 수행합니다.

메소드를 직접 지정하는 경우, 아래와 같이 사용할 수 있습니다.

```python
>>> from sejong_univ_auth import PortalSSOToken, DosejongSession, auth
>>> auth(id='<your-id>', password='<your-pw>', methods=PortalSSOToken)
>>> auth(id='<your-id>', password='<your-pw>', methods=DosejongSession)
...
# same to default
>>> auth(id='<your-id>', password='<your-pw>', methods=[PortalSSOToken, DosejongSession])
```

복수의 Authenticator를 list(혹은 tuple) 형태로 주게 될 경우, 순차적으로 메소드를 수행합니다. 만약 현재의 메소드에서 현재 인증이 불가능한(Internel Sever Error 등의) 상황일 경우, 바로 다음 메소드로 시프트하여 인증을 진행합니다.

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
	authenticator=<class'DosejongSession'>
)
```

- **success: 인증 서버 정상 동작 여부 **
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
  - 인증 실패시의 보다 정확한 실패 사유, 메소드에 따라 
    이름/학번 등의 추가 정보 수집이 가능할 경우, 해당 필드에 함께 반환됩니다.
  - Value: dict
- **authenticator: 해당 인증에 사용된 Authenticator 클래스**

