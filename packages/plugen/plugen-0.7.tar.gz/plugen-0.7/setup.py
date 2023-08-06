from setuptools import setup, find_packages


setup(
    entry_points={
        'console_scripts': [
            'plugen = main:main',
        ],
    },
    name='plugen',
    version='0.7',
    license='MIT',
    author="Clarembeau Alexis",
    author_email='alexis.clarembeau@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/aclarembeau/plugen',
    keywords='static website generator',
    install_requires=[],
)
