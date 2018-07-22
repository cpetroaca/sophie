from setuptools import setup
from setuptools import Extension


def readme():
    with open('README.md') as f:
        text = f.read()
    return text

setup(
    name='sophie',
    description='Open Information Extraction System',
    packages=['sophie'],
    install_requires=[
        'spacy>=2.0.10'
    ],
    license='Apache',
    version='0.0.1',
    author='Cristian Petroaca',
    author_email='cristian.petroaca@gmail.com',
    url='https://github.com/cpetroaca/sophie',
    long_description=readme()
)