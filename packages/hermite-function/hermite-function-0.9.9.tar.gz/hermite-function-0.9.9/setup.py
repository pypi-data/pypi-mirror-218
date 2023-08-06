from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / 'README.md').read_text()
  
setup(
    name = 'hermite-function',
    version = '0.9.9',
    description = 'A Hermite function series module.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    
    author = 'Sebastian Gössl',
    author_email = 'goessl@student.tugraz.at',
    license = 'MIT',
    
    url = 'https://github.com/goessl/hermitefunction',
    py_modules = ['HermiteFunction'],
    python_requires = '>=3.7',
    install_requires = ['numpy', 'scipy', 'hermitefunction'],
    
    classifiers = [
      'Programming Language :: Python :: 3.7',
      'License :: OSI Approved :: MIT License',
      'Operating System :: OS Independent'
    ]
)
