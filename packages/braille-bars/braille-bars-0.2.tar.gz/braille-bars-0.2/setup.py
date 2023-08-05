from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text()

setup(
    name='braille-bars',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.2',
    license='MIT',
    author="Morgan Heijdemann",
    author_email='targhan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='progress bar, asci, braille, terminal, cli, braille bars',
    install_requires=[]
)