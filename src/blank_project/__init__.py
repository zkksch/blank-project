import re
from datetime import date
from os import listdir
from os import makedirs
from os import path
from shutil import copyfile
from typing import Iterable
from typing import Iterator

from jinja2 import Environment
from jinja2 import FileSystemLoader

from blank_project.constants import DEFAULT_COVERAGE
from blank_project.constants import DEFAULT_LINE_LENGTH


TEMPLATE_PROJECT_DIR = path.join(path.dirname(path.abspath(__file__)),
                                 'template')


env = Environment(
    loader=FileSystemLoader(TEMPLATE_PROJECT_DIR),
)


class Config:
    """
    Project config.

    :param name: Project name
    :param author: Author
    :param line_length: Line length
    :param python2: Python 2 compatibility
    :param docs: Sphinx docs enabled
    :param mypy: Mypy enabled
    :param pylint: Pylint enabled
    :param flake8: Flake8 enabled
    :param isort: Isort enabled
    :param coverage: Coverage percentage check value
                     (if less than 0 - coverage is disabled)
    """
    def __init__(self,
                 name: str,
                 author: str,
                 line_length: int = DEFAULT_LINE_LENGTH,
                 python2: bool = False,
                 docs: bool = True,
                 mypy: bool = True,
                 pylint: bool = True,
                 flake8: bool = True,
                 isort: bool = True,
                 coverage: int = DEFAULT_COVERAGE,
                 ) -> None:
        self.name = name
        self.author = author
        self.line_length = line_length
        self.python2 = python2
        self.docs = docs
        self.mypy = mypy
        self.pylint = pylint
        self.flake8 = flake8
        self.isort = isort
        self.coverage = coverage >= 0
        self.coverage_fail = coverage

        self.year = date.today().year

    def get_context(self
                    ) -> dict:
        """
        :return: Project config as a dict
        """
        return {
            'name': self.name,
            'author': self.author,
            'line_length': self.line_length,
            'python2': self.python2,
            'docs': self.docs,
            'mypy': self.mypy,
            'pylint': self.pylint,
            'flake8': self.flake8,
            'isort': self.isort,
            'coverage': self.coverage,
            'coverage_fail': self.coverage_fail,
            'year': self.year,
        }


class Builder:
    """
    Project builder

    :param base_dir: Project directory
    :param config: Project config
    """

    # Template files postfix
    template_postfix: str = '_template'

    def __init__(self,
                 base_dir: str,
                 config: Config
                 ) -> None:
        self.base_dir = base_dir
        self.config = config

    @classmethod
    def _listdir(cls,
                 directory: str,
                 prefix: str,
                 skip: Iterable = ()
                 ) -> Iterator[str]:
        """
        List directory files

        :param directory: Working directory
        :param prefix: Files prefix
        :return: Iterator over file names
        """
        for file_path in listdir(directory):
            file_path = path.join(directory, file_path)
            if path.isdir(file_path):
                yield from cls._listdir(file_path, prefix, skip)
                continue

            file_path = file_path.replace(prefix, '')

            if skip:
                need_skip = False
                for skip_pattern in skip:
                    if re.match(skip_pattern, file_path):
                        need_skip = True
                        break

                if need_skip:
                    continue

            yield file_path

    @classmethod
    def _iterate_project_files(cls,
                               skip: Iterable = (),
                               ) -> Iterator[str]:
        """
        Iterate project files

        :return: Iterator over template project file names
        """
        return cls._listdir(TEMPLATE_PROJECT_DIR,
                            path.join(TEMPLATE_PROJECT_DIR, ''),
                            skip)

    @classmethod
    def _check_template(cls,
                        file_path: str
                        ) -> bool:
        """
        Checking that the file is a template

        :param file_path: File path
        :return: Is file a template or not
        """
        return file_path.endswith(cls.template_postfix)

    def _handle_template(self,
                         template_path: str
                         ) -> None:
        """
        Handle template files

        :param template_path: Template path
        """
        template = env.get_template(template_path)

        template_path = template_path[:-len(self.template_postfix)]

        with open(path.join(self.base_dir, template_path), mode='w') as f:
            f.write(template.render(self.config.get_context()))

    def _handle_file(self,
                     file_path: str
                     ) -> None:
        """
        Handle simple files

        :param file_path: File path
        """
        copyfile(path.join(TEMPLATE_PROJECT_DIR, file_path),
                 path.join(self.base_dir, file_path))

    def build(self
              ) -> None:
        """
        Build the project
        """
        if not path.exists(self.base_dir):
            makedirs(self.base_dir)

        src_dir = path.join(self.base_dir, 'src', self.config.name)
        if not path.exists(src_dir):
            makedirs(src_dir)
            with open(path.join(src_dir, '__init__.py'), mode='w'):
                pass

        skip = []

        if not self.config.docs:
            skip.append('docs/')

        if not self.config.coverage:
            skip.append('.coveragerc')

        if not self.config.flake8:
            skip.append('.flake8')

        if not self.config.isort:
            skip.append('.isort.cfg')

        if not self.config.mypy:
            skip.append('mypy.ini')

        if not self.config.pylint:
            skip.append('.pylintrc')

        for file_path in self._iterate_project_files(skip=skip):
            is_template = self._check_template(file_path)

            dirname = path.join(self.base_dir, path.dirname(file_path))

            if not path.exists(dirname):
                makedirs(dirname)

            if is_template:
                self._handle_template(file_path)
            else:
                self._handle_file(file_path)
