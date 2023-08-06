# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cherre_singer_ingest',
 'cherre_singer_ingest.factories',
 'cherre_singer_ingest.repositories',
 'cherre_singer_ingest.services',
 'cherre_singer_ingest.services.stream_writers',
 'cherre_singer_ingest.services.streams',
 'cherre_singer_ingest.services.taps',
 'cherre_singer_ingest.services.targets',
 'cherre_singer_ingest.value_items',
 'cherre_singer_ingest.value_items.ingest_bookmarks',
 'cherre_singer_ingest.value_items.specifications']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.6.2,<4.0.0',
 'cherre-domain>=9.0.1',
 'cherre-google-clients>=7.12.0',
 'cherre-types>=0.5.0',
 'cherre_domain>=8.12.0',
 'click>=7.1.2,<8.0.0',
 'fastavro>=1.3.2,<2.0.0',
 'ijson>=3.1.1,<4.0.0',
 'openpyxl==3.0.7',
 'paramiko>=2.7.2,<3.0.0',
 'pyfarmhash>=0.2.2,<0.3.0',
 'python-snappy>=0.6.0,<0.7.0',
 'singer-sdk==0.1.6',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'cherre-singer-ingest',
    'version': '16.6.6',
    'description': 'Library holding the taps and targets for Cherre ingestion',
    'long_description': 'None',
    'author': 'Mathieson',
    'author_email': 'mathieson@cherre.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.9',
}


setup(**setup_kwargs)
