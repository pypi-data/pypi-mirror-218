# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dotsCLI', 'dotsCLI.config', 'dotsCLI.docker']

package_data = \
{'': ['*'], 'dotsCLI': ['samples/*']}

install_requires = \
['PyYAML>=6.0,<7.0', 'click>=8.1.4,<9.0.0', 'paramiko>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['dts = dotsCLI.dts:cli']}

setup_kwargs = {
    'name': 'dotscli',
    'version': '0.1.0',
    'description': 'A command line interface for automating containerization',
    'long_description': "# dotsCLI\nA command-line tool to automate deployment and containerization of your applications.\n\n> Supported enviroments: Node\n\n<br>\n\n## Installation\n1. Install the package globally\n```\npip install dotsCLI\n```\n2. Run the entry command to show the full range of functions:\n```\ndts\n```\n3. Make a config file in a new folder named '.dts' in the root directory of your system, configuring the values respectively.\n\n> Note: `FRONTEND_DIR_PATH` and `FRONTEND_DIST_PATH` must not contain a trailing slash.\n\n```bash\n[aws]\nAWS_USER=ubuntu\n\n[main]\nFRONTEND_DIR_PATH=<path_to_dir>\nFRONTEND_DIST_PATH=<path_to_dir>\nSSH_KEY_PATH=<path_to_dir>/ssh-key.pem\n```\n\n## Functions\n1. Easily deploy your frontend SPAs to remote linux servers\n    - Hassle-free deployment\n    - Automatic configuration of nginx request routing\n\n2. Dockerize your NodeJS application\n    - Allows you to define the base image version\n    - Easily define all dockerfile configurations\n    - Automatically setup a new docker network with custom name\n    - Customize docker-compose configurations \n    - Attaches the newly created docker network to the container\n\n## Future Scope\n1. Add support for more environments (like python, java etc)\n2. More flexibility towards docker network configurations\n    - Allow users to define the type of network created\n",
    'author': 'Yathartha Goenka',
    'author_email': 'goenkayathartha2002@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
