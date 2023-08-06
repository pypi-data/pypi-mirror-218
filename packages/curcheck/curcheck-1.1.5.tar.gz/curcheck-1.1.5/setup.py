# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curcheck']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.3', 'lxml>=4.9.2', 'pyppeteer>=1.0.2']

setup_kwargs = {
    'name': 'curcheck',
    'version': '1.1.5',
    'description': 'Library for parsing SPA and MPA sites',
    'long_description': '# Curcheck \n\n___',
    'author': 'BulatXam',
    'author_email': 'Khamdbulat@yandex.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
