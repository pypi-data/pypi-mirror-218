from distutils.core import setup


setup(
    name='pyappi',
    version='1.0.3',
    packages=['pyappi', 'tests'],
    license='Copyright (c) All Rights Reserved',
    description="Native Python Appi implementation. Single threaded, single node, no plug-ins.",
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['pyappi=pyappi.main:cli',
                            'pyappi-client=pyappi.client:cli'
                            ],
    },
    install_requires=[
        "wheel",
        "uvicorn"
    ],
)
