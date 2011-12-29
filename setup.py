from setuptools import setup, find_packages

setup(
    name = 'platypus-router',
    version = '0.1.0',
    description = 'Django like WSGI router',
    author = 'Vincent Jauneau',
    author_email = 'vincent.jauneau@platypus-creation.com',
    url = 'https://github.com/platypus-creation/platypus-router/',
    packages = find_packages(),
    install_requires = ['WebOb',],
)
