# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ario3s_aiva', 'ario3s_aiva.commands', 'ario3s_aiva.utils']

package_data = \
{'': ['*']}

install_requires = \
['toml>=0.10.2,<0.11.0', 'tomli>=2.0.1,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['aiva = ario3s_aiva.main:app']}

setup_kwargs = {
    'name': 'ario3s-aiva',
    'version': '1.0.6',
    'description': 'Manage dynamic ssh tunnel on localhost',
    'long_description': '# aiva cli tool\n\n<p>A tool to create SOCKS5 proxy on localhost</p>\n\n\n## Configuration\n<p>Default config file path is /home/USERNAME/.aiva.toml\n\n<b>Config file Format</b>\n```\n[default]\nusername = "<DEFAULT USERNAME>"\nlocal_port = <DEFAULT BIND PORT>\nserver_label = "<DEFAULT LABEL>"\n\n[server_<label>]\nip = <server-ip>\nport = <server-port>\n\n[server_<label>]\n...\n\n```\n</p>\n\n## Usage\n\nConnects to server using ssh\n```\naiva connect  \n```\n\nDisconnects from server\n```\naiva disconnect  \n```\n\nGet connection status\n```\naiva status [-d] \n```\n\nList available servers\n```\naiva list_servers\n```\n\nChange default server\n```\naiva change-server\n```',
    'author': 'ario',
    'author_email': 'cybera.3s@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
