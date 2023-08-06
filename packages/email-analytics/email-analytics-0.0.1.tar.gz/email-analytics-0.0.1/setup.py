from setuptools import setup, find_packages
from os import path
from io import open

import email_analytics

here = path.abspath(path.dirname(__file__))
reqs = []

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    read_lines = f.readlines()
    reqs = [each.strip() for each in read_lines]

setup(
    name = email_analytics.__name__,
    version = email_analytics.__version__,
    description = email_analytics.__description__,
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/get-dataxy/email-analytics.git',
    author = 'Kiran Kumar Kotari',
    author_email = 'kirankotari@live.com',
    # entry_points={
    #     'console_scripts': [
    #         'pyang_patch=pyang_patch.scripts.pyang_patch:run',
    #     ],
    # },
    install_requires=reqs,
    classifiers = [
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11'
        ],
    keywords = 'email-analytics',
    packages = find_packages(where='.', exclude=['tests']),
    include_package_data=True,
)

