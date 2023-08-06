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

install_requires = \
['more-itertools>=9.1.0,<10.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'ir-client',
    'version': '0.1.3',
    'description': 'Library to access the iRacing web API',
    'long_description': 'None',
    'author': 'Sascha Lamp',
    'author_email': 'sascha@lamp-online.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
