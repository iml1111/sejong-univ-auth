"""
sejong-univ-auth
-------------
Sejong University Member Account Authentication.
"""

from setuptools import setup
from sejong_univ_auth import __VERSION__

with open("README.md", "r", encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sejong-univ-auth',
    version=__VERSION__,
    description='Sejong University Member Account Authentication.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iml1111/sejong-univ-auth',
    author='IML',
    author_email='shin10256@gmail.com',
    license='MIT',
    keywords='sejong univ auth',
    packages=['sejong_univ_auth', 'sejong_univ_auth.authenticator'],
    install_requires=['requests', 'bs4'],
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)