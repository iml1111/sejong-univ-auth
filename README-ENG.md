# sejong-univ-auth
![Python versions](https://img.shields.io/badge/Python-3.7-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Release](https://img.shields.io/badge/release-0.3.4-red)

<p align="center">
  <img width="25%" alt="sejong-univ-auth image" src="https://user-images.githubusercontent.com/47492535/177720510-4f7d28aa-8c3d-46a1-b28e-12e24a2e5893.png" >
	<br /> 
	<b>Sejong University Member Account Authentication</b>
	<br /> 
</p>

A simple authentication library to verify Sejong University members.

If you're using **Python**, you can easily implement it as shown below!

Using **another programming language**? Try our [custom-developed REST API](https://github.com/iml1111/sejong-univ-auth#sejong-auth-api)!

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


### Sejong University provides various web services, all authenticated via a single portal member account.

This library replicates the authentication structure of multiple web services, allowing programmatic use of the results after performing the login.

The endpoint function for using sejong_univ_auth is as follows:

```python
def auth(id: str, password: str, methods: Authenticator)
# id, password: Account information for logging into the Sejong University portal.
# methods: Determines which authentication method to attempt (default=Manual).
```

### Methods
The currently supported authentication methods are:

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

  - Authentication method for the Sejong University portal site.

- **DosejongSession**

  - Session authentication method for the dosejong site.
  - Additionally retrieves name and major.

- **ClassicSession**

  - Session authentication method for the Daeyang Humanities College site.
  - Additional information retrieved:
    - Name
    - Major
    - Year
    - Enrollment status (enrolled/leave of absence/completed)
    - Status of classic reading certification

- **MoodlerSession**

  - Session authentication method for the SJULMS site.
  - Additionally retrieves name and major.

- **Manual (default)**
  - Executes all implemented methods sequentially in the order of average execution speed.
  - Stops when authentication succeeds or fails due to incorrect ID/password.

To specify a method directly, use the following:

```python
>>> from sejong_univ_auth import PortalSSOToken, DosejongSession, auth
>>> auth(id='<your-id>', password='<your-pw>', methods=PortalSSOToken)
>>> auth(id='<your-id>', password='<your-pw>', methods=DosejongSession)
...
# To execute multiple Authenticators sequentially:
>>> auth(id='<your-id>', password='<your-pw>', methods=[PortalSSOToken, DosejongSession])
```

If multiple Authenticators are provided as a list (or tuple), they are executed sequentially

If the current method cannot authenticate (e.g., Internal Server Error), it shifts to the next method.

### AuthResponse

The result of authentication is returned as a Nametuple:

```python
AuthResponse(
	success=True,
	is_auth=True,
	status_code=200,
	code='success',
	body={
		'name': 'Shin Hee-jae',
		'major': 'Computer Science'
	},
	authenticator='DosejongSession'
)
```

- **success: Whether the authentication server operated normally**

  - Indicates if the server returned valid results for the authentication process.
  - Value: True / False

- **is_auth: Whether authentication succeeded**

  - Even with correct ID/password, server errors or updated authentication formats may cause authentication failures.
  - Returns None if the result cannot be determined.
  - Value: True / False / None

- **status_code: HTTP status code of the authentication server**
  - Value: int
- **code: Authenticator return code**
  - Returns 'success' for successful authentication.
  - Returns specific codes for failures or unknown results.
  - Value: string
- **body: Metadata**
  - Contains metadata related to the authentication result, such as:
    - Detailed reasons for authentication failure
    - Additional information like name, student ID, year, enrollment status, etc.
  - Value: dict
- **authenticator: The Authenticator class used for this authentication**

<br />

# Sejong Auth API

For users of other programming languages like Java or Node.js, we provide a custom-developed REST API.

- **Continuous support for this API is not guaranteed.**

### Request

**method**For method, input the existing methods as is, such as "Manual" or "DosejongSession". Sequential invocation of multiple methods is not supported.

```javascript
POST https://auth.imsejong.com/auth?method=<desired-method> HTTP/1.1
        Host: auth.imsejong.com
{
  "id": "<student-id>",
        "pw": "<password>"
}

```

### Response

```javascript
{
  "msg": "success",
          "result": {
    "authenticator": "DosejongSession",
            "body": {
      "major": "Computer Science",
              "name": "Shin Hee-jae"
    },
    "code": "success",
            "is_auth": true,
            "status_code": 200,
            "success": true
  },
  "version": "0.3.4"
}

```

<br />

# Contributors

If you'd like to contribute, please refer to our guidelines. Thank you! 😀

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

