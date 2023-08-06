# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skinny_orm']

package_data = \
{'': ['*']}

install_requires = \
['dateparser>=1.1.8,<2.0.0']

setup_kwargs = {
    'name': 'skinny-orm',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'MayasMess',
    'author_email': 'amayas.messara@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
