import os
from setuptools import setup, find_packages

CURRENT_DIR = os.path.dirname(__file__)
def read(fname):
    return open(os.path.join(CURRENT_DIR, fname)).read()

# Info for setup
PACKAGE = 'reddit_view'
NAME = 'reddit_view'
DESCRIPTION = 'a reddit image collector'
AUTHOR = 'Jorge Perez'
AUTHOR_EMAIL = 'japrogramer@gmail.com'
URL = 'https://github.com/japrogramer/reddit_view'
VERSION = __import__(PACKAGE).__version__

# setup call
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='BSD',
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
         'Environment :: Web Environment',
         'Intended Audience :: Developers',
         'License :: OSI Approved :: BSD License',
         'Operating System :: OS Independent',
         'Programming Language :: Python',
    ],
    keywords = 'reddit images imgur links list subreddits',
    install_requires=[
         'requests',
         'beautifulsoup4',
         'fake-useragent',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': ['reddit_view=reddit_view.__main__:main',],},
    )
