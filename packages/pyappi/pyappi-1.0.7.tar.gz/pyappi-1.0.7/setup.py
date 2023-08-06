from distutils.core import setup


setup(
    name='pyappi',
    version='1.0.7',
    packages=['pyappi', 'tests','pyappi.block','pyappi.document','pyappi.encoding','pyappi.stats','pyappi.stats','pyappi.sync','pyappi.user','pyappi.util'],
    license='Copyright (c) All Rights Reserved',
    description="Native Python Appi implementation. Single threaded, single node, no plug-ins.",
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['pyappi=pyappi.main:main',
                            'pyappi-client=pyappi.client:main'
                            ],
    },
    install_requires=[
        "wheel",
        "uvicorn",
        "twine",
        "fastapi",
        "pathvalidate",
        "twine",
        "wheel",
        "colorama",
        "httpx",
        "click"
    ],
)
