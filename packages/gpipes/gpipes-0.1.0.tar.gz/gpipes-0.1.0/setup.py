# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gpipes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gpipes',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Przemysław Krzysztof Rekucki',
    'author_email': 'przemyslaw.rekucki@golem.network',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
