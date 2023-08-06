from setuptools import setup, find_packages

from src.logPPP import __version__

setup(
    name='logPPP',
    version=__version__,
    description='logPPP',
    author='Aurorax-own',
    author_email='15047150695@163.com',
    packages=find_packages('src'),
    package_dir={'logPPP': 'src/logPPP'},
    include_package_data=True,
    install_requires=[
    ]
)
