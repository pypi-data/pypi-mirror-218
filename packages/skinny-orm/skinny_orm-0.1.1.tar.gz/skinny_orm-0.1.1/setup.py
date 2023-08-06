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
    'version': '0.1.1',
    'description': '',
    'long_description': '# Skinny ORM\n\n"Skinny ORM" - a lightweight Python package that simplifies data storage, manipulation, and retrieval from a SQLite (maybe others later) database using Python dataclasses.\n\n\nIt\'s not really a "Relational Mapper". It\'s just a simple way to persist data.\n\nInstallation:\n- \n```shell script\n  pip install skinny_orm\n```\nor\n```shell script\n  poetry add skinny_orm\n```\n\nExample:\n-\n- Create your model:\n```python\nfrom dataclasses import dataclass\nfrom datetime import datetime\n\n@dataclass\nclass User:\n    id: int\n    name: str\n    age: int\n    birth: datetime\n    percentage: float\n\n```\n\n- Create a connection et an "orm" object\n\n```python\nimport sqlite3\nfrom skinny_orm.orm import Orm\n\nconnection = sqlite3.connect(\'database.db\')\norm = Orm(connection)\n```\n\n- And Voila (no need to create tables. if they don\'t exist, it will create them automatically)\n\n```python\nusers = [\n    User(id=1, name=\'Naruto\', age=15, birth=datetime.now(), percentage=9.99),\n    User(id=2, name=\'Sasuke\', age=15, birth=datetime.now(), percentage=9.89),\n    User(id=3, name=\'Sakura\', age=15, birth=datetime.now(), percentage=9.79),\n]\n# Bulk insertions (if the table "User" does not exist, it will create it)\norm.bulk_insert(users)\n# Selections (always end with .first() or .all() )\nnaruto: User = orm.select(User).where(User.name == \'Naruto\').first()\nthe_boys: list[User] = orm.select(User).where((User.name == \'Naruto\') | (User.name == \'Sasuke\')).all()\n\n# Update data by setting specific fields\norm.update(User).set(User.age == 30).where(User.id == 1)\n# Or you can simply update the object with all the fields\nnaruto.age = 30\norm.update(naruto).using(User.id)\n\n# Bulk update objects\nusers_20_year_later = [\n    User(id=1, name=\'Naruto\', age=35, birth=datetime.now(), percentage=9.99),\n    User(id=2, name=\'Sasuke\', age=35, birth=datetime.now(), percentage=9.89),\n    User(id=3, name=\'Sakura\', age=35, birth=datetime.now(), percentage=9.79),\n]\norm.bulk_update(users_20_year_later).using(User.id)\n```\n',
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
