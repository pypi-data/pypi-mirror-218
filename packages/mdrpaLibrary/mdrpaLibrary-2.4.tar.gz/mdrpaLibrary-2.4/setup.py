from setuptools import setup, find_packages

setup(
    name='mdrpaLibrary',
    version='2.4',
    packages=find_packages(),
    package_data={'mdrpaLibrary': ['*.robot', 'utils/*.robot']},
)
