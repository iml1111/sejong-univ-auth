# sejong-univ-auth ![Python versions](https://img.shields.io/badge/Python-3.7-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.3.4-red)

<p align="center">
  <img width="25%" alt="sejong-univ-auth image" src="https://user-images.githubusercontent.com/47492535/177720510-4f7d28aa-8c3d-46a1-b28e-12e24a2e5893.png" >
	<br /> 
	<b>Sejong University Member Account Authentication</b>
	<br /> 
</p>

세종대학교 구성원인지 확인하기 위한 간편한 인증 라이브러리입니다.

**Python**이라면 아래와 같은 방법으로 쉽게 구현해보세요!

If you have difficulty understanding Korean, please refer to [this document](https://github.com/iml1111/sejong-univ-auth/blob/main/README-ENG.md).

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

# Contributors

컨트리뷰트를 원하신다면 [가이드라인](https://github.com/iml1111/sejong-univ-auth/blob/main/CONTRIBUTING.md)을 참고해주세요! 감사합니다! 😀

# Disclaimer
본 오픈소스 라이브러리 sejong-univ-auth(이하 “본 소프트웨어”)와 관련하여 다음과 같은 사항을 명시합니다:
1. MIT 라이선스 배포: 본 소프트웨어는 MIT 라이선스로 배포됩니다.
2. 개인 정보 비저장: 사용자가 입력한 학번 및 비밀번호는 외부로 전송되거나 저장되지 않으며, 오직 인증 여부 확인에만 사용됩니다.
3. 비공식 구현: 본 소프트웨어는 세종대학교의 공식 인증 API나 사전 허가를 기반으로 하지 않고, 세종대학교 웹 인증 절차를 모방하여 구현되었습니다. 따라서 본 소프트웨어는 세종대학교와 공식적으로 아무런 관련이 없음을 밝힙니다.
4. 사용자 책임: 본 소프트웨어는 있는 그대로(AS IS) 제공되며, 이 소프트웨어의 사용으로 인한 위험은 전적으로 사용자에게 있습니다. 본 소프트웨어의 사용 또는 오작동으로 인해 발생하는 어떠한 직접적이거나 간접적인 손해에 대해서도 저자는 책임을 지지 않습니다.
5. 자유 이용 및 법규 준수: 개인, 기업, 조직 등 어떤 형태의 사용자도 본 소프트웨어를 자유롭게 사용할 수 있습니다. 단, 본 소프트웨어 사용 시 제3자의 약관이나 관련 법률을 준수할 책임은 사용자에게 있습니다. 만약 본 소프트웨어의 사용으로 인해 제3자의 권리 침해나 약관 위반 등의 문제가 발생할 경우, 그에 대한 모든 법적 책임은 사용자 본인에게 있습니다.

# References

- https://pypi.org/project/sejong-univ-auth/
- https://auth.imsejong.com/

