from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="taxOrder",
    version="0.2.7",
    #python_requires='>=3.7.0',
    description="Returns list of species in a phylogenetic tree ordered by increasing taxonomic distance to a reference species",
    author="Felix Langschied",
    author_email="langschied@bio.uni-frankfurt.de",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['taxOrder', 'taxOrder.*']),
    package_data={'': ['*']},
    install_requires=[
        'ete3',
        'six',
        'numpy'
    ],
    license="GPL-3.0",
    entry_points={
        'console_scripts': ["taxOrder = taxOrder.cmdline_taxOrder:main"],
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
    ],
)
