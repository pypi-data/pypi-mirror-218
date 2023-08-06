from setuptools import setup, find_packages


setup(
    name='plugen',
    version='0.6',
    license='MIT',
    author="Clarembeau Alexis",
    author_email='alexis.clarembeau@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/aclarembeau/plugen',
    keywords='static website generator',
    install_requires=[],
)
