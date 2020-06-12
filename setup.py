import json
from setuptools import setup, find_namespace_packages

with open('osvimdriver/pkg_info.json') as fp:
    _pkg_info = json.load(fp)

with open("DESCRIPTION.md", "r") as description_file:
    long_description = description_file.read()

setup(
    name='os-vim-driver',
    version=_pkg_info['version'],
    author='Accanto Systems',
    description='Openstack implementation of a VIM driver',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/accanto-systems/openstack-vim-driver",
    packages=find_namespace_packages(include=['osvimdriver*']),
    include_package_data=True,
    install_requires=[
        'ignition-framework{0}'.format(_pkg_info['ignition-version']),
        'python-heatclient>=1.17.0,<2.0',
        'python-keystoneclient>=3.19.0,<4.0',
        'python-neutronclient>=6.5.1,<7.0',
        'python-novaclient>=13.0.0,<14.0.0',
        'tosca-parser @ git+https://github.com/accanto-systems/tosca-parser.git@accanto',
        'heat-translator @ git+https://github.com/accanto-systems/heat-translator.git@accanto-nfv',
        'uwsgi>=2.0.18,<3.0',
        'gunicorn>=19.9.0,<20.0'
    ],
    entry_points='''
        [console_scripts]
        ovd-dev=osvimdriver.__main__:main
    ''',
    scripts=['osvimdriver/bin/ovd-uwsgi', 'osvimdriver/bin/ovd-gunicorn', 'osvimdriver/bin/ovd']
)
