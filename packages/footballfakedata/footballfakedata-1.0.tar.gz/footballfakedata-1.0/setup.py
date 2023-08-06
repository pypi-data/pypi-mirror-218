from setuptools import setup

VERSION = '1.0' 
DESCRIPTION = 'A package to generate fake footballer data'
LONG_DESCRIPTION = 'A package to generate fake footballer data for data science training purpose'

setup(
    name='footballfakedata',
    version='1.0',
    description='A package to generate fake footballer data',
    author='Marek Zarzycki',
    author_email='contact@mazarzycki.com',
    author_website='https://mazarzycki.com/',
    packages=['fakefootballer'],
    install_requires=[
        'pandas',
    ],
)
