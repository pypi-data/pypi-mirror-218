#!/usr/bin/python

import setuptools
  
with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()
    
KEYWORDS = ('powerdns pdns database exporter mysql zone bind')

setuptools.setup(
    name="pdns_exporter",
    version="0.3.0",
    author="Denis MACHARD",
    author_email="d.machard@gmail.com",
    description="PowerDNS records exporter",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/dmachard/python-pdns-exporter",
    packages=['pdns_exporter'],
    include_package_data=True,
    platforms='any',
    keywords=KEYWORDS,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={'console_scripts': ['pdns_exporter = pdns_exporter.exporter:start_exporter']},
    install_requires=[
        "SQLAlchemy",
        "aiohttp",
        "aiomysql",
        "requests",
    ]
)