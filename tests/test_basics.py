import unittest
import sejong_univ_auth

class BasicsTestCase(unittest.TestCase):

    def setUp(self):
        self.module = sejong_univ_auth.auth

    def tearDown(self):
        pass

    def test_module_exists(self):
        """Run Module Exists"""
        self.assertFalse(self.module is None)

    def test_auth_failed(self):
        """잘못된 id/pw 인증 테스트"""
        res = self.module(id='invalid_id', password='invalid_pw')
        self.assertTrue('auth_failed' in res.code)

if __name__ == '__main__':
    unittest.main()