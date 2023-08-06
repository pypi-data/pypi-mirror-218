import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='ipwho',
    version='0.1.2',
    packages = find_packages(),
    include_package_data=True,
    description='ip information gathering. originally created by kamabay modified the code to get only some specific data.',
    long_description = README,
    author='Jay',
    url='https://github.com/techdjay/ipwho',
    license='Apache License 2.0',
    install_requires=['requests'],
    keywords = ['jay', 'ipwho', 'techdjay', 'ip', 'whois', 'information', 'gathering'],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    entry_points={
        "console_scripts":[
            "ipwho = ipwhois.IPwhois:main"
        ]
    }
)
