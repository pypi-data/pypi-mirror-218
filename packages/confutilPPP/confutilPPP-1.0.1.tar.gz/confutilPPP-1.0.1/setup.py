from setuptools import setup, find_packages

from src.confutilPPP import __version__

setup(
    name='confutilPPP',
    version=__version__,
    description='A simple configuration file tool',
    author='Aurorax-own',
    author_email='15047150695@163.com',
    packages=find_packages('src'),
    package_dir={'confutilPPP': 'src/confutilPPP'},
    include_package_data=True,
    install_requires=[
        'PyYAML',
        'logPPP'
    ],
)
