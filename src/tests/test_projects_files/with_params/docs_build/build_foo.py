import shutil
import subprocess
from os.path import abspath
from os.path import dirname
from os.path import join


BASE_DIR = dirname(abspath(__file__))


def main():
    """
    Построение документации + API

    Перед запуском построения документации так же собирает всё API с
    помощью sphinx-apidoc

    Добавить всё дерево API можно с помощью конструкции:

    .. code:: rst

        .. toctree::
            :caption: API

            api/modules.rst

    """

    # Удаляем старый билд
    shutil.rmtree(join(BASE_DIR, 'build'), ignore_errors=True)

    # Собираем документацию API
    subprocess.call([
        'sphinx-apidoc',
        '-fM', '-o', join(BASE_DIR, 'source', 'api'),
        join(BASE_DIR, '..', 'src', 'foo'),
        # Далее следует добавить модули для которых не надо собирать api
        # например: '../*tests*'
    ])

    # Строим документацию
    subprocess.call([
        'sphinx-build', '-b', 'html',
        join(BASE_DIR, 'source'), join(BASE_DIR, 'build')
    ])

    # Удаляем исходники для документации API
    shutil.rmtree(join(BASE_DIR, 'source', 'api'), ignore_errors=True)


if __name__ == '__main__':
    main()
