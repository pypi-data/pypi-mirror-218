"""
@Project: https://github.com/KouShoken/pynihongo
@Time: 西暦2023年6月16日 15:30
@Author: KouShoken

This is an open source project that uses the MIT protocol. 
While I don't make any demands, But　I think respecting copyright 
maybe is a basic morality.
"""
import functools
from datetime import datetime

from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='PyNihongo',
    version='0.0.1dev3',
    author='Koushoken',
    author_email='kskjcx-dev@yahoo.co.jp',
    description='A Python package about japanese.',
    packages=['pynihongo'],
    install_requires=[
    ],
)
