

from os.path import dirname
from os.path import join

from setuptools import find_packages
from setuptools import setup


with open(join(dirname(__file__), 'README.md'),
          mode='r', encoding='utf-8') as readme:
    long_description = readme.read()


def main():
    setup(
        name='blank-project',
        author='zkksch',
        version='0.1.0',
        description=(
            ''
        ),
        long_description=long_description,
        long_description_content_type='text/markdown',
        classifiers=[],
        packages=find_packages('src'),
        package_dir={'blank_project': 'src/blank_project'},
        package_data={'blank_project': [
            'template/*.*',
            'template/.*',
            'template/docs/*.*',
            'template/docs/*',
            'template/docs/source/*.*',
            'template/requirements/*.*',
        ]},
        install_requires=(
            'jinja2==2.10.3',
        ),
        scripts=(
            'scripts/blank-project.py',
        ),
    )


if __name__ == '__main__':
    main()
