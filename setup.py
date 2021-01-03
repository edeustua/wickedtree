from setuptools import setup, find_packages

setup(
    name='wickedtree',
    version='0.1',
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

