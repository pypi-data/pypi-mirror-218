# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['actionai']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.8,<0.28.0', 'pydantic>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'actionai',
    'version': '0.0.1',
    'description': 'A small library to call local functions using openai function calling',
    'long_description': '',
    'author': 'Amal Shaji',
    'author_email': 'amalshajid@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
