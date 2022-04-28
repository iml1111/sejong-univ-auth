import unittest, os
from sejong_univ_auth import PortalSSOToken, DosejongSession
from sejong_univ_auth.authenticator import Authenticator


class AuthenticatorTestCase(unittest.TestCase):

    def setUp(self):
        self.id = os.getenv('STUDENT_ID')
        self.pw = os.getenv('PASSWORD')

    def test_portal_ssotoken(self):
        """PortalSSOToken Authenticator 테스트"""
        module: Authenticator = PortalSSOToken()
        # correct case
        res = module.authenticate(id=self.id, password=self.pw)
        self.assertTrue(res.is_auth)
        # incorrect case
        res = module.authenticate(id='wrong', password='wrong')
        self.assertFalse(res.is_auth)
        self.assertIn(
            res.code,
            ('erridpwd_auth_failed', 'Error_auth_failed')
        )

    def test_dosejong_session(self):
        """DosejongSession Authenticator 테스트"""
        module: Authenticator = DosejongSession()
        # correct case
        res = module.authenticate(id=self.id, password=self.pw)
        self.assertTrue(res.is_auth)
        # incorrect case
        res = module.authenticate(id='wrong', password='wrong')
        self.assertFalse(res.is_auth)
        self.assertEqual(res.code, 'auth_failed')


if __name__ == '__main__':
    unittest.main()
