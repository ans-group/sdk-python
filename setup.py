# pylint:disable=missing-module-docstring
from setuptools import setup, find_packages

__author__ = 'UKFast'
__email__ = 'support@ukfast.co.uk'
__copyright__ = 'Copyright (c) 2020 UKFast'
__license__ = 'MIT'
__url__ = 'https://github.com/ukfast/sdk-python'
__download_url__ = 'https://pypi.python.org/ukfast/sdk-python'
__description__ = 'Python interface for the UKFast API.'

exclusions = ["*.tests", "*.tests.*", "tests.*", "tests"]

with open('VERSION', 'r') as version_file:
    version = version_file.read().strip()

with open('requirements.txt', 'r') as requirements_file:
    requirements = [requirement for requirement in requirements_file.read().split('\n')
                    if len(requirement)]

setup(
    name="UKFastAPI",
    author=__author__,
    author_email=__email__,
    url=__url__,
    description=__description__,
    version=version,
    install_requires=requirements,
    packages=find_packages(exclude=exclusions),
    data_files=[('', ['VERSION', 'requirements.txt', 'setup.py'])],
    include_package_data=True,
)
