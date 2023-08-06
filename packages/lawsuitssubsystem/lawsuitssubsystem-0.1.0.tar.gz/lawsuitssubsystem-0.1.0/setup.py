# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parsing_lawsuits']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.24.1,<0.25.0',
 'pandas>=2.0.3,<3.0.0',
 'pypdf>=3.12.0,<4.0.0',
 'selenium>=4.10.0,<5.0.0',
 'tqdm>=4.65.0,<5.0.0',
 'undetected-chromedriver>=3.5.0,<4.0.0']

setup_kwargs = {
    'name': 'lawsuitssubsystem',
    'version': '0.1.0',
    'description': '',
    'long_description': '# scraping lawsuits\nSubsystem for parsing lawsuits\n## Project structure\n\n## How to dev\n```\npoetry shell\npoetry install\n```\n\n***\n```\n├── debug.py\n├── parsing_lawsuits\n│   └── python_callables.py - core functions for Airflow\n├── poetry.lock\n├── pyproject.toml\n└── README.md\n\n```\n\n## How to public to Pypi\nFirst you need create api on pypi\n\n```bash\npoetry config pypi-token.pypi $(cat .token)\npoetry publish --build\n```\n',
    'author': 'DieNice',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
