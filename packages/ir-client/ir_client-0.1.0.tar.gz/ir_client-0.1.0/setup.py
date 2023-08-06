# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ir_client',
 'ir_client.laps',
 'ir_client.series_race_results',
 'ir_client.subsession_results',
 'ir_client.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ir-client',
    'version': '0.1.0',
    'description': 'Library to access the iRacing web API',
    'long_description': 'None',
    'author': 'Sascha Lamp',
    'author_email': 'sascha@lamp-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
