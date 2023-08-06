from setuptools import setup, find_packages
setup(
    name='ML_Algo',
    version='1.0.5',
    author='Mr Raj',
    author_email='arunraj14092002@gmail.com',
    description='A package for calculating Series Time Data',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['pandas'],
)
