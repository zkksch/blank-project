import os
import tempfile
import unittest
from filecmp import cmp
from filecmp import cmpfiles
from os import makedirs

from freezegun import freeze_time

from blank_project import Builder
from blank_project import Config


SAMPLES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'test_projects_files'
)


class BuilderTest(unittest.TestCase):
    @staticmethod
    def raise_file_cmp_error(left, right):  # pragma: no cover
        with open(left, mode='r') as left_file:
            left_content = left_file.read()

        with open(right, mode='r') as right_file:
            right_content = right_file.read()

        raise AssertionError(
            f'''
{left}:
===============================================================================
{left_content}
===============================================================================
{right}:
===============================================================================
{right_content}
===============================================================================
'''
        )

    def test_project_build(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            with_project = os.path.join(tmpdir, 'with_project')
            with_project_src = os.path.join(tmpdir, 'with_project_src')
            without_project = os.path.join(tmpdir, 'without_project')

            makedirs(with_project)
            makedirs(os.path.join(with_project_src, 'src', 'project'))

            Builder(with_project,
                    Config(name='project', author='author')).build()

            self.assertTrue(os.path.exists(
                os.path.join(with_project, 'src', 'project', '__init__.py')
            ))

            Builder(with_project_src,
                    Config(name='project', author='author')).build()

            self.assertTrue(os.path.exists(
                os.path.join(with_project_src, 'src', 'project')
            ))

            self.assertFalse(os.path.exists(
                os.path.join(with_project_src, 'src', 'project', '__init__.py')
            ))

            Builder(without_project,
                    Config(name='project', author='author')).build()

            self.assertTrue(os.path.exists(
                os.path.join(without_project, 'src', 'project', '__init__.py')
            ))

    @freeze_time('1970-01-01')
    def test_full_project(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            sample_dir = os.path.join(SAMPLES_DIR, 'full', 'project')
            Builder(tmpdir, Config(name='project', author='author')).build()

            match, mismatch, errors = cmpfiles(
                tmpdir, sample_dir,
                [
                    'MANIFEST.in',
                    'setup.py',
                    '.flake8',
                    'tox.ini',
                    'README.md',
                    'requirements/base.txt',
                    'requirements/dev.txt',
                    '.coveragerc',
                    'mypy.ini',
                    '.isort.cfg',
                    'docs/source/conf.py',
                    'docs/source/index.rst',
                    'docs/build.py',
                    'docs/make.bat',
                    'docs/Makefile',
                    '.pylintrc',
                    'src/project/__init__.py'
                ]
            )

            if mismatch:  # pragma: no cover
                for f in mismatch:
                    left = os.path.join(tmpdir, f)
                    right = os.path.join(sample_dir, f)

                    self.raise_file_cmp_error(left, right)

    def _build_and_compare_file(self, config, build_file, sample_file):
        with tempfile.TemporaryDirectory() as tmpdir:
            Builder(tmpdir, Config(**config)).build()

            left = os.path.join(tmpdir, build_file)
            right = sample_file

            same = cmp(left, right)

            if not same:  # pragma: no cover
                self.raise_file_cmp_error(left, right)

            self.assertTrue(same)

    def _build_and_check_file(self, config, exists=(), not_exists=()):
        with tempfile.TemporaryDirectory() as tmpdir:
            Builder(tmpdir, Config(**config)).build()

            for f in exists:
                self.assertTrue(os.path.exists(os.path.join(tmpdir, f)))

            for f in not_exists:
                self.assertFalse(os.path.exists(os.path.join(tmpdir, f)))

    @freeze_time('1970-01-01')
    def test_params_docs_build(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'docs_build')
        build_file = os.path.join('docs', 'build.py')

        self._build_and_compare_file(
            dict(name='foo', author='author'),
            build_file,
            os.path.join(sample_dir, 'build_foo.py')
        )

        self._build_and_compare_file(
            dict(name='bar', author='author'),
            build_file,
            os.path.join(sample_dir, 'build_bar.py')
        )

    @freeze_time('1970-01-01')
    def test_params_docs_config(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'docs_config')
        build_file = os.path.join('docs', 'source', 'conf.py')

        self._build_and_compare_file(
            dict(name='foo', author='author'),
            build_file,
            os.path.join(sample_dir, 'conf_foo.py')
        )

        self._build_and_compare_file(
            dict(name='bar', author='author'),
            build_file,
            os.path.join(sample_dir, 'conf_bar.py')
        )

        self._build_and_compare_file(
            dict(name='project', author='author0'),
            build_file,
            os.path.join(sample_dir, 'conf_author0.py')
        )

        self._build_and_compare_file(
            dict(name='project', author='author1'),
            build_file,
            os.path.join(sample_dir, 'conf_author1.py')
        )

        with freeze_time("2000-01-01"):
            self._build_and_compare_file(
                dict(name='project', author='author'),
                build_file,
                os.path.join(sample_dir, 'conf_2000.py')
            )

        with freeze_time("1970-01-01"):
            self._build_and_compare_file(
                dict(name='project', author='author'),
                build_file,
                os.path.join(sample_dir, 'conf_1970.py')
            )

    @freeze_time('1970-01-01')
    def test_params_flake8(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'flake8')
        build_file = os.path.join('.flake8')

        self._build_and_compare_file(
            dict(name='project', author='author', line_length=79),
            build_file,
            os.path.join(sample_dir, '.flake8_79')
        )

        self._build_and_compare_file(
            dict(name='project', author='author', line_length=120),
            build_file,
            os.path.join(sample_dir, '.flake8_120')
        )

    @freeze_time('1970-01-01')
    def test_params_isort(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'isort')
        build_file = os.path.join('.isort.cfg')

        self._build_and_compare_file(
            dict(name='foo', author='author'),
            build_file,
            os.path.join(sample_dir, '.isort_foo.cfg')
        )

        self._build_and_compare_file(
            dict(name='bar', author='author'),
            build_file,
            os.path.join(sample_dir, '.isort_bar.cfg')
        )

        self._build_and_compare_file(
            dict(name='project', author='author', line_length=79),
            build_file,
            os.path.join(sample_dir, '.isort_79.cfg')
        )

        self._build_and_compare_file(
            dict(name='project', author='author', line_length=120),
            build_file,
            os.path.join(sample_dir, '.isort_120.cfg')
        )

    @freeze_time('1970-01-01')
    def test_params_readme(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'readme')
        build_file = os.path.join('README.md')

        self._build_and_compare_file(
            dict(name='foo', author='author'),
            build_file,
            os.path.join(sample_dir, 'README_foo.md')
        )

        self._build_and_compare_file(
            dict(name='bar', author='author'),
            build_file,
            os.path.join(sample_dir, 'README_bar.md')
        )

    @freeze_time('1970-01-01')
    def test_params_setup(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'with_params', 'setup')
        build_file = os.path.join('setup.py')

        self._build_and_compare_file(
            dict(name='project', author='author', python2=True),
            build_file,
            os.path.join(sample_dir, 'with_python2', 'setup.py')
        )

        self._build_and_compare_file(
            dict(name='foo', author='author'),
            build_file,
            os.path.join(sample_dir, 'without_python2', 'setup_foo.py')
        )

        self._build_and_compare_file(
            dict(name='bar', author='author'),
            build_file,
            os.path.join(sample_dir, 'without_python2', 'setup_bar.py')
        )

        self._build_and_compare_file(
            dict(name='project', author='author0'),
            build_file,
            os.path.join(sample_dir, 'without_python2', 'setup_author0.py')
        )

        self._build_and_compare_file(
            dict(name='project', author='author1'),
            build_file,
            os.path.join(sample_dir, 'without_python2', 'setup_author1.py')
        )

    @freeze_time('1970-01-01')
    def test_only_coverage(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'only', 'coverage')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 isort=False),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 isort=False),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 isort=False),
            exists=('.coveragerc',),
            not_exists=('.flake8',
                        '.isort.cfg',
                        'mypy.ini',
                        '.pylintrc',
                        'docs',)
        )

    @freeze_time('1970-01-01')
    def test_exclude_coverage(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'exclude', 'coverage')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 coverage=-1),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 coverage=-1),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 coverage=-1),
            not_exists=('.coveragerc',),
            exists=('.flake8',
                    '.isort.cfg',
                    'mypy.ini',
                    '.pylintrc',
                    'docs',)
        )

    @freeze_time('1970-01-01')
    def test_only_flake8(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'only', 'flake8')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 isort=False,
                 coverage=-1),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 isort=False,
                 coverage=-1),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 isort=False,
                 coverage=-1),
            exists=('.flake8',),
            not_exists=('.coveragerc',
                        '.isort.cfg',
                        'mypy.ini',
                        '.pylintrc',
                        'docs',)
        )

    @freeze_time('1970-01-01')
    def test_exclude_flake8(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'exclude', 'flake8')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 flake8=False),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 flake8=False),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 flake8=False),
            not_exists=('.flake8',),
            exists=('.coveragerc',
                    '.isort.cfg',
                    'mypy.ini',
                    '.pylintrc',
                    'docs',)
        )

    @freeze_time('1970-01-01')
    def test_only_isort(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'only', 'isort')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 mypy=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            exists=('.isort.cfg',),
            not_exists=('.coveragerc',
                        '.flake8',
                        'mypy.ini',
                        '.pylintrc',
                        'docs',)
        )

    @freeze_time('1970-01-01')
    def test_exclude_isort(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'exclude', 'isort')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 isort=False),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 isort=False),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 isort=False),
            not_exists=('.isort.cfg',),
            exists=('.coveragerc',
                    '.flake8',
                    'mypy.ini',
                    '.pylintrc',
                    'docs',)
        )

    @freeze_time('1970-01-01')
    def test_only_mypy(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'only', 'mypy')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 pylint=False,
                 flake8=False,
                 coverage=-1),
            exists=('mypy.ini',),
            not_exists=('.coveragerc',
                        '.flake8',
                        '.isort.cfg',
                        '.pylintrc',
                        'docs',)
        )

    @freeze_time('1970-01-01')
    def test_exclude_mypy(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'exclude', 'mypy')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 mypy=False),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 mypy=False),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 mypy=False),
            not_exists=('mypy.ini',),
            exists=('.coveragerc',
                    '.flake8',
                    '.isort.cfg',
                    '.pylintrc',
                    'docs',)
        )

    @freeze_time('1970-01-01')
    def test_only_pylint(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'only', 'pylint')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 mypy=False,
                 flake8=False,
                 coverage=-1),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 mypy=False,
                 flake8=False,
                 coverage=-1),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 docs=False,
                 isort=False,
                 mypy=False,
                 flake8=False,
                 coverage=-1),
            exists=('.pylintrc',),
            not_exists=('.coveragerc',
                        '.flake8',
                        '.isort.cfg',
                        'mypy.ini',
                        'docs',)
        )

    @freeze_time('1970-01-01')
    def test_exclude_pylint(self):
        sample_dir = os.path.join(SAMPLES_DIR, 'exclude', 'pylint')

        req_file = os.path.join('requirements/dev.txt')
        tox_file = os.path.join('tox.ini')

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 pylint=False),
            req_file,
            os.path.join(sample_dir, 'dev.txt')
        )

        self._build_and_compare_file(
            dict(name='project',
                 author='author',
                 pylint=False),
            tox_file,
            os.path.join(sample_dir, 'tox.ini')
        )

        self._build_and_check_file(
            dict(name='project',
                 author='author',
                 pylint=False),
            not_exists=('.pylintrc',),
            exists=('.coveragerc',
                    '.flake8',
                    '.isort.cfg',
                    'mypy.ini',
                    'docs',)
        )
