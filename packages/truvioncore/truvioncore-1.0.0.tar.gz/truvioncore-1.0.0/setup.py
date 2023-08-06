from setuptools import setup, find_packages
from pkg_resources import parse_requirements

# Read the requirements from requirements.txt file
with open('requirements.txt') as f:
    requirements = [str(req) for req in parse_requirements(f.read())]


setup(
    name='truvioncore',
    version='1.0.0',
    packages=find_packages(),
    author='Mat Mathews Brown',
    author_email='mbrown@truvion.com',
    description='Truvion Core Classes and DSL',
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=requirements,
)