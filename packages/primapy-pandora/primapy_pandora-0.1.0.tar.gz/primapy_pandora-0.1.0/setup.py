# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['primapy_pandora']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-pandora',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Devops',
    'author_email': 'devops@prima.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
