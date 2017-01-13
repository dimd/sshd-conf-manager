from os import path
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), 'r') as f:
    long_description = f.read()

setup(
    name='sshd_conf_manager',
    version='0.2.4',
    description='Read configuration from Redis and apply it to sshd',
    long_description=long_description,
    packages=find_packages(include=['sshd_conf_manager']),
    author='Dimitris Dalianis',
    author_email='dalianis.dimitris@nokia.com',
    install_requires=[
        'docopt==0.6.2',
        'gevent==1.1.2',
        'PyYAML==3.11',
        'redis==2.10.5',
        'supervisor>=3.2.3'],
    entry_points={
        'console_scripts': [
            'sshd-conf-manager = sshd_conf_manager.sshd_conf:main',
        ]
    },
    keywords=['configuration', 'redis', 'sshd', 'supervisord'],
    url='https://gitlabe1.ext.net.nokia.com/utas-security/conf-manager.git',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ],
    data_files=[
        ('conf', ['conf/logging_config.yaml'])
    ]
)
