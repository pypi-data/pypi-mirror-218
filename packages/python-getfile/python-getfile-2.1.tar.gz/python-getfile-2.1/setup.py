from setuptools import setup, find_packages

setup(
    name='python-getfile',
    version='2.1',
    author='Adithyan',
    description='A package for downloading files from URLs',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
