from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='readlike',
    version='0.1.1',
    description='GNU Readline-like line editing module',
    long_description=long_description,
    url='http://jangler.info/code/readlike',
    author='Brandon Mulcahy',
    author_email='brandon@jangler.info',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
    ],
    keywords=['line editing', 'readlike', 'readline', 'urwid'],
    py_modules=['readlike'],
)
