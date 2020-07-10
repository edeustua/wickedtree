from setuptools import setup, find_packages

import versioneer

setup(
    name='wickedtree',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Implementation of Wick's theorem using a binary tree",
    author='J. Emiliano Deustua',
    author_email='edeustua@gmail.com',
    install_requires=[
        'click',
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-pep8',
            'pytest-cov'
        ]
    },
    packages=find_packages(),
)
