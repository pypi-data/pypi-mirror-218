import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "addfunctions",
    version = "0.0.1",
    author = "Lucas Borges",
    author_email = "lucas.borges@fysik.su.se",
    description = ("additional functions for QDng calculations setups."),
    license = "MIT",
    keywords = "qdng",
    url = "https://gitlab.fysik.su.se/lucas.borges/addfunctions",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Pre-Alpha",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
