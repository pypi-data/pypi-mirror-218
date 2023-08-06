#!/usr/bin/env python

"""The setup script."""
import codecs
import os

from setuptools import setup, find_packages


def read_requirements(rel_path):
    with open(rel_path) as f:
        return f.read().splitlines()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()


setup(
    author="Eric Richard",
    author_email='ehutzle@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    description="A simple program to download documentation from docs.rs and convert it into a plaintext file.",
    entry_points={
        'console_scripts': [
            'docs2txt=docs2txt.cli:main',
        ],
    },
    install_requires=read_requirements("requirements.txt"),
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='docs2txt',
    name='docs2txt',
    packages=find_packages(include=['docs2txt', 'docs2txt.*']),
    test_suite='tests',
    tests_require=read_requirements("requirements_dev.txt"),
    url='https://github.com/ehutzle/docs2txt',
    version=get_version("docs2txt/__init__.py"),
    zip_safe=False,
)
