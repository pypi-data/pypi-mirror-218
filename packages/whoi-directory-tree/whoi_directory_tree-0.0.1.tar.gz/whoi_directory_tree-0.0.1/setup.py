# Importing Packages
from setuptools import setup

# Reading README and Storing Info as `Long Description`
with open("README.md", "r") as fh:
    long_description = fh.read()

# Configuring Setup
setup(

    name = 'whoi_directory_tree',
    version = '0.0.1',
    description = 'whoi_directory_tree',
    url = "https://github.com/rahulbordoloi/Directory-Tree/",
    author = "WHOI Acomms Group",

    py_modules = ['whoi_directory_tree'],
    package_dir = {'': 'src'},

    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

    long_description = long_description,
    long_description_content_type = "text/markdown",

)
