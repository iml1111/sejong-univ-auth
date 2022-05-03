import unittest, os
from sejong_univ_auth import *
from sejong_univ_auth.authenticator import Authenticator
from tests.decorator import timer


class AuthenticatorTestCase(unittest.TestCase):

    def setUp(self):
        self.id = os.getenv('STUDENT_ID')
        self.pw = os.getenv('PASSWORD')

    @timer
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

    @timer
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

    @timer
    def test_moodler_session(self):
        """MoodlerSession Authenticator 테스트"""
        module: Authenticator = MoodlerSession()
        # correct case
        res = module.authenticate(id=self.id, password=self.pw)
        self.assertTrue(res.is_auth)
        # incorrect case
        res = module.authenticate(id='wrong', password='wrong')
        self.assertFalse(res.is_auth)
        self.assertEqual(res.code, 'auth_failed')

    @timer
    def test_classic_session(self):
        """MoodlerSession Authenticator 테스트"""
        module: Authenticator = ClassicSession()
        # correct case
        res = module.authenticate(id=self.id, password=self.pw)
        self.assertTrue(res.is_auth)
        # incorrect case
        res = module.authenticate(id='wrong', password='wrong')
        self.assertFalse(res.is_auth)
        self.assertEqual(res.code, 'auth_failed')


if __name__ == '__main__':
    unittest.main()
