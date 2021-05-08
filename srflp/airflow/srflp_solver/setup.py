from setuptools import setup
import setuptools

packages=setuptools.find_packages()

setup(
    name='srflp',
    version='0.1.0',
    description='A package that solves srflp problem',
    url='TBD',
    author='Edvard Dimand',
    author_email='edi.dimand@gmail.com',
    package_dir={"srflp": "srflp"},
    packages=packages,
    install_requires=[
            'wheel',
            'pandas',
            'numpy',
            'pysftp',
            ],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python :: 3.7+',
    ],
)