# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kade_drive',
 'kade_drive.core',
 'kade_drive.message_system',
 'kade_drive.tests']

package_data = \
{'': ['*']}

install_requires = \
['netifaces==0.11.0', 'rpyc==5.3.1', 'typer==0.9.0']

setup_kwargs = {
    'name': 'kade-drive',
    'version': '0.5.1',
    'description': 'distributed file system based on kademlia dht',
    'long_description': 'Distributed file system based on <https://github.com/bmuller/kademlia> for the final project of distributed systems\n\n## Basic Usage\n\n- Clone the repo and run poetry install\n- Run server.py in one pc or several pc in a local network\n- Run cli.py in any pc of the network and start playing with the system\n\n## Installation\n\n```console\n- pip install kade-drive\n```\n\n## Server\n\n```Python\nfrom kade_drive.server import start_server\n\nstart_server()\n```\n\n## Client\n\n### Note: Make shure that there exist at least a server in the local network\n\n```Python\nfrom kade_drive.cli import ClientSession\n\nclient = ClientSession()\nclient.connect()\nclient.put(4, 5)\nvalue = client.get(4)\nassert value == 5\n```\n\n### Tests\n\nTo run tests make shure that there is at least one server in the network.\n',
    'author': 'DanielUH2019',
    'author_email': 'danielcardenascabrera2016@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
