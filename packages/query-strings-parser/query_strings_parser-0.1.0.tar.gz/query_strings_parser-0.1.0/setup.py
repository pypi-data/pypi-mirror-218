from setuptools import setup, find_packages

setup(
    name='query_strings_parser',
    version='0.1.0',
    license='Apache License 2.0',
    author="Jefferson Sampaio de Medeiros",
    author_email='jefferson.medeiros@nutes.uepb.edu.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://dev.azure.com/SHS-DI-DH-Brasil/Predict%20to%20Win/_git/p2w_devops?path=/libraries/query_strings_parser',
    keywords='query query-strings sql parser'
)
