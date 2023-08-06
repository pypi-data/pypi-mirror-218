from distutils.core import setup


setup(
    name='pyappi',
    version='1.0.2',
    packages=['pyappi', 'tests'],
    license='Copyright (c) All Rights Reserved',
    description="Native Python Appi implementation. Single threaded, single node, no plug-ins.",
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
