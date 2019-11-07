from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


with open(join(dirname(__file__), 'README.md'),
          mode='r', encoding='utf-8') as readme:
    long_description = readme.read()


def main():
    setup(
        name='project',
        author='author1',
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
