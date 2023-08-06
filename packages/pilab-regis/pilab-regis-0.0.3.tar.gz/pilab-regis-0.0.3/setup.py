from setuptools import setup

import regis

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='pilab-regis',
    version=regis.__version__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PiLAB-Medical-Imaging/registration',
    author='PiLAB',
    author_email='nicolas.delinte@uclouvain.be',
    packages=['regis'],
    install_requires=['dipy',
                      'nibabel',
                      'numpy',
                      ],

    classifiers=['Natural Language :: English',
                 'Programming Language :: Python'],
)
