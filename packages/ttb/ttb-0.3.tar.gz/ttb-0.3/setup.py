from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(name='ttb',
      version='0.3',
      description='Библиотека со всякимим полезностями',
      long_description=long_description,
      author_email='neso_hoshi_official@mail.ru',
      zip_safe=False,
      author='Neso Hiroshi',
      classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
])