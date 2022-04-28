import unittest, os
from dotenv import load_dotenv

REQUIRED_ENVS = (
    'STUDENT_ID',
    'PASSWORD'
)

def env_check():
    try:
        return [os.environ[i] for i in REQUIRED_ENVS]
    except KeyError as e:
        print(
            f'"{e.args[0]}" 환경변수가 등록되지 않았습니다.\n'
            f'테스트를 실행시키기 위해서는 실제 인증된 학번/비밀번호로 아래와 같은 환경변수들이 등록해야 합니다.\n'
            f'{REQUIRED_ENVS}'
        )
        return False

def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    load_dotenv(verbose=True)
    if env_check():
        test()