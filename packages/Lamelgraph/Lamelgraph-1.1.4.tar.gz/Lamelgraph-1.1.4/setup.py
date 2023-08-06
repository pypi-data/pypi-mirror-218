
from setuptools import setup
from setuptools import find_packages


version = '1.1.4'

long_description = 'Lamelgraph'

setup(
    name = 'Lamelgraph',
    version = version,

    author = 'Nikita Goltsev',
    author_email = 'n.goltsev@g.nsu.ru',

    description = 'Lamelgraph',
    long_description = long_description,

    url = 'https://github.com/NikitaGoltsev/Lamel_project_copy',

    packages = ['src/Lamel_window'],
    install_requires = ['numpy', 'PyQt5'],
    )