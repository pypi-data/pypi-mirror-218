from setuptools import setup, find_packages
setup(
    name='ML_Algo',
    version='1.0.0',
    author='Mr Raj',
    author_email='arunraj14092002@gmail.com',
    description='A package for calculating moving averages',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['pandas'],
)
