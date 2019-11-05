# coding: utf-8
from __future__ import unicode_literals

from os.path import dirname
from os.path import join

import six
from setuptools import find_packages
from setuptools import setup


if six.PY2:
    from io import open


with open(join(dirname(__file__), 'README.md'),
          mode='r', encoding='utf-8') as readme:
    long_description = readme.read()


def main():
    setup(
        name='project',
        author='author',
        version='0.1.0',
        description=(
            ''
        ),
        long_description=long_description,
        long_description_content_type='text/markdown',
        classifiers=[],
        packages=find_packages('src'),
        package_dir={'': 'src'},
        install_requires=(),
    )


if __name__ == '__main__':
    main()
