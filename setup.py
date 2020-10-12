

from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = "2.4.1"

setup(
    version=VERSION,
    name="wthings-gateway",
    author="WaveletThings",
    author_email="info@wthings.io",
    license="Apache Software License (Apache Software License 2.0)",
    description="Waveletthings Gateway for IoT devices.",
    url="https://github.com/wthings/wthings-gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.5",
    packages=['wthings_gateway', 'wthings_gateway.gateway', 'wthings_gateway.storage',
              'wthings_gateway.wt_client', 'wthings_gateway.connectors', 'wthings_gateway.connectors.ble',
              'wthings_gateway.connectors.mqtt', 'wthings_gateway.connectors.opcua', 'wthings_gateway.connectors.request',
              'wthings_gateway.connectors.modbus', 'wthings_gateway.connectors.can', 'wthings_gateway.connectors.bacnet',
              'wthings_gateway.connectors.bacnet.bacnet_utilities', 'wthings_gateway.connectors.odbc',
              'wthings_gateway.connectors.rest', 'wthings_gateway.connectors.snmp',
              'wthings_gateway.wt_utility', 'wthings_gateway.extensions',
              'wthings_gateway.extensions.mqtt', 'wthings_gateway.extensions.modbus', 'wthings_gateway.extensions.opcua',
              'wthings_gateway.extensions.ble', 'wthings_gateway.extensions.serial', 'wthings_gateway.extensions.request',
              'wthings_gateway.extensions.can', 'wthings_gateway.extensions.bacnet', 'wthings_gateway.extensions.odbc',
              'wthings_gateway.extensions.rest',  'wthings_gateway.extensions.snmp', 'wthings_gateway.extensions.opcda',
              'wthings_gateway.extensions.plc'
              ],
    install_requires=[
        'jsonpath-rw',
        'regex',
        'pip',
        'paho-mqtt',
        'pyserial',
        'PyYAML',
        'simplejson',
        'requests'
    ],
    download_url='https://github.com/wthings/wthings-gateway/archive/%s.tar.gz' % VERSION,
    entry_points={
        'console_scripts': [
            'wthings-gateway = wthings_gateway.wt_gateway:daemon'
        ]},
    package_data={
        "*": ["config/*"]
    })



