from setuptools import setup, find_packages
import os

VERSION = '0.0.1'
DESCRIPTION = 'An intent classification library for AI Models.'
LONG_DESCRIPTION = 'A library for training and testing small to large scale intent classification models.'

# Setting up
setup(
    name="intentify",
    version=VERSION,
    author="Ice (Rishan Pancham)",
    author_email="<rishanpan@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pickle', 'numpy', 'tensorflow', 'nltk', 'keras'],
    keywords=['python', 'intent', 'intents', 'ai', 'intent classification'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)