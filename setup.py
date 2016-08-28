from setuptools import setup, find_packages
from distutils.util import convert_path
import sys


if sys.version_info[0] == 3:
    if sys.version_info[1] == 5:
        if sys.version_info[2] < 1:
            sys.exit("Urban Journey requires python 3.5.1 or higher")
    elif sys.version_info[1] < 5:
        sys.exit("Urban Journey requires python 3.5.1 or higher")
elif sys.version_info[0] < 3:
    sys.exit("Urban Journey requires python 3.5.1 or higher")


main_ns = {}
ver_path = convert_path('urban_journey/__init__.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)

setup(
    name='urban_journey',
    version=main_ns['__version__'],
    description='Publisher subscriber framework',
    author='Aaron de Windt',
    author_email='',
    url='https://github.com/aarondewindt/urban-journey',

    install_requires=['numpy', 'scipy', 'lxml', 'gitpython', 'pip', 'PyYAML'],
    packages=find_packages('.', exclude=["test"]),

    entry_points={
          'console_scripts': [
              'uj = urban_journey.__main__:main'
          ]
    },

    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Development Status :: 2 - Pre-Alpha'],
)
