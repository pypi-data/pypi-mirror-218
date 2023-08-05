from setuptools import setup, find_packages

setup(
    name='braille-bars',
    version='0.1',
    license='MIT',
    author="Morgan Heijdemann",
    author_email='targhan@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='progress bar, asci, braille, terminal, cli, braille bars',
    install_requires=[]
)