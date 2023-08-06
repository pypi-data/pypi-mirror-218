import os
from setuptools import setup, find_packages

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='BahnarTextAugmentation',
    version='1.0.2a',
    license='Apache License 2.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    description='Bahnar Text Augmentation',
    long_description=read('README.md'),
    install_requires=['pyvi', 
                      'simalign', 
                      'sentencepiece', 
                      'transformers', 
                      'sacremoses', 
                      'nltk', 
                      'numpy>=1.22.0', 
                      'pandas',
                      'gensim>=4.3.0',
                      'openpyxl'
                      ],
)