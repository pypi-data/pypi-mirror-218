# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['message_system']

package_data = \
{'': ['*']}

install_requires = \
['netifaces>=0.11.0,<0.12.0']

setup_kwargs = {
    'name': 'message-system',
    'version': '0.1.2',
    'description': '',
    'long_description': '',
    'author': 'JavierOramas',
    'author_email': 'javiale2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
