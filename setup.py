import pathlib
from io import open
from os import path

from setuptools import find_packages, setup

# directory with current setup.py file
HERE = pathlib.Path(__file__).parent

# Readme file as text
README = (HERE / "Readme.rst").read_text()

# Automatically collects all_modules to requirements.txt for install_requires and set dependency links
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup(
    name='piper',
    version='0.0.2',
    packages=find_packages(),  # list of all packages
    install_requires=install_requires,
    include_package_data=True,
    python_requires='>=2.7',  # any python greater than 2.7
    entry_points='''
        [console_scripts]
        piper=piper.__main__:main
    ''',
    zip_safe=False,
    long_description=README,
    long_description_content_type="text/markdown",
    dependency_links=dependency_links,
)
