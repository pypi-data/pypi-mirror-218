from setuptools import setup, find_packages


setup(
    name='edp_redy_py',
    version='0.1.11',
    license='Apache 2.0',
    author="Fábio Ferreira",
    author_email='fabiorcferreira@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/skyborgff/edp_redy',
    keywords='EDP',
    install_requires=[
        "python-dateutil~=2.8.2",
        "awscrt~=0.16.23",
        "awsiot~=0.1.3",
        "requests~=2.31.0",
        "warrant-ext>=0.6.2",
        "setuptools~=58.1.0",
    ],

)