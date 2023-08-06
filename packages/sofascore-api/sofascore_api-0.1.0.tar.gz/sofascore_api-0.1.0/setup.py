# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sofascore_api']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'sofascore-api',
    'version': '0.1.0',
    'description': 'API wrapper for Sofascore',
    'long_description': '# sofascore-api',
    'author': 'Felipe Allegretti',
    'author_email': 'felipe@allegretti.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
