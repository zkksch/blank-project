import argparse

from blank_project import DEFAULT_COVERAGE
from blank_project import DEFAULT_LINE_LENGTH
from blank_project import Builder
from blank_project import Config


def _get_parser():
    """
    :return: Argument parser
    """
    parser = argparse.ArgumentParser(description='Create blank project')
    parser.add_argument('dir', type=str, help='Project directory')
    parser.add_argument('name', type=str, help='Name of the project')
    parser.add_argument('author', type=str, help='Author')
    parser.add_argument('--line_length', type=int, required=False,
                        help='Line length', default=DEFAULT_LINE_LENGTH)
    parser.add_argument('--python2', action='store_true',
                        help='Python 2 compatible')
    parser.add_argument('--no-docs', action='store_true',
                        help='Disable sphinx')
    parser.add_argument('--no-mypy', action='store_true', help='Disable mypy')
    parser.add_argument('--no-pylint', action='store_true',
                        help='Disable pylint')
    parser.add_argument('--no-flake8', action='store_true',
                        help='Disable flake8')
    parser.add_argument('--no-isort', action='store_true',
                        help='Disable isort')
    parser.add_argument('--coverage', type=int, required=False,
                        help='Coverage --fail-under config',
                        default=DEFAULT_COVERAGE)
    parser.add_argument('--no-coverage', action='store_true',
                        help='Disable coverage')

    return parser


def main():
    """
    Building the project by provided params
    """
    parser = _get_parser()
    args = parser.parse_args()

    params = {
        'name': args.name,
        'author': args.author,
        'line_length': args.line_length,
        'python2': args.python2,
        'docs': not args.no_docs,
        'mypy': not args.no_mypy,
        'pylint': not args.no_pylint,
        'flake8': not args.no_flake8,
        'isort': not args.no_isort,
        'coverage': -1 if args.no_coverage else args.coverage,
    }

    Builder(args.dir, Config(**params)).build()


if __name__ == '__main__':
    main()
