import sys
from os.path import abspath
from os.path import dirname
from os.path import join

import sphinx_rtd_theme


# -- Path setup --------------------------------------------------------------

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, join(BASE_DIR, 'src'))

# -- Project information -----------------------------------------------------

project = 'project'
copyright = '2000, author'
author = 'author'
version = '0.1.0'
release = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx_autodoc_typehints',
]
templates_path = []
language = 'ru'
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_static_path = []

# -- Extension configuration -------------------------------------------------

set_type_checking_flag = True
