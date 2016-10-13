from setuptools import find_packages, setup

setup(
    name='conf_manager',
    version='0.2',
    description='Read configuration from Redis and apply it to sshd',
    packages=find_packages(exclude=['tests']),
    author='Dimitris Dalianis',
    author_email='dalianis.dimitris@nokia.com',
    install_requires=[
        'docopt==0.6.2',
        'gevent==1.1.2',
        'redis==2.10.5',
        'supervisor>=3.2.3'],
    entry_points={
        'console_scripts': [
            'sshd-conf-manager = conf_manager.sshd_conf:main',
        ]
    },
    keywords=['configuration', 'redis', 'ssh'],
    url='https://gitlabe1.ext.net.nokia.com/utas-security/conf-manager.git',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2.7',
    ]
)
