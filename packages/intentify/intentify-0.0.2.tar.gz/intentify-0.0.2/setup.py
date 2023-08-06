from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
LONG_DESCRIPTION = (this_directory / "README.md").read_text()

VERSION = '0.0.2'
DESCRIPTION = 'An intent classification library for AI Models.'

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