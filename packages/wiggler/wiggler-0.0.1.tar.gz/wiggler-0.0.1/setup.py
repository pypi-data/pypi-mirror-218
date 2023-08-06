from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'WiggleR - Desktop research unit for making controlled experiments'
LONG_DESCRIPTION = 'WiggleR is a desktop research unit for making controlled experiments with worms. WiggleR can also be used inside the WiggleBin'

setup(
    name="wiggler",
    version=VERSION,
    author="Vincent Kranendonk",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[]
)
