from os import path

from setuptools import setup, find_packages


def read(name):
    with open(path.join(
            path.abspath(path.dirname(__file__)),
            name
    ), encoding='utf-8') as f:
        return f.read()


setup(
    name='ASTFormula',
    version='0.0.3',
    author='Oleh Rybalchenko',
    author_email='rv.oleg.ua@gmail.com',
    url='https://github.com/oryba/astformula',
    description='A simple and extensible AST-based Python formula engine '
                'to execute string calculation statements',
    download_url='https://github.com/oryba/astformula/archive/v0.0.3.zip',
    license='OSI Approved (BSD)',
    packages=find_packages(),
    install_requires=['astunparse'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
