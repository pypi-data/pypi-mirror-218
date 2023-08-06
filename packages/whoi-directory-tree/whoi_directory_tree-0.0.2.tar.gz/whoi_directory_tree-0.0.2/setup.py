# Importing Packages
from setuptools import setup

# Reading README and Storing Info as `Long Description`
with open("README.md", "r") as fh:
    long_description = fh.read()

# Configuring Setup
setup(

    name = 'whoi_directory_tree',
    version = '0.0.2',
    description = 'whoi_directory_tree',
    url = "https://git.whoi.edu/acomms/whoi_directory_tree/",
    author = "WHOI Acomms Group",

    classifiers = [
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],

    long_description = long_description,
    long_description_content_type = "text/markdown",

)
