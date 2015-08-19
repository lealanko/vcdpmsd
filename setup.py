#!/usr/bin/env python

from setuptools import setup
from os.path import join, dirname

setup(
    name='vcdpmsd',
    version='0.9.0',
    description="A daemon to let DPMS manage VideoCore's HDMI output",
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    url='https://github.com/lealanko/vcdpmsd',
    author='Lauri Alanko',
    author_email='la@iki.fi',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Desktop Environment :: Screen Savers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    keywords=['DPMS', 'VideoCore', 'Raspberry Pi'],
    py_modules=['vcdpmsd'],
    install_requires=['sh'], # also xpyb, but it doesn't support setuptools
    entry_points={
        'console_scripts': ['vcdpmsd=vcdpmsd:main'],
    }
)
