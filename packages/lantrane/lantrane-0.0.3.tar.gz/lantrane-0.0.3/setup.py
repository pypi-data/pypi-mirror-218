# Change the content according to your package.
import setuptools
import re

# Configurations
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     install_requires=[],      								  # Dependencies
     python_requires='>=3',                                   # Minimum Python version
     name='lantrane',                                  # Package name
     version="0.0.3",                                     # Version
     author="Adrian Edwards",                                 # Author name
     author_email="adrian@adriancedwards.com",                           # Author mail
     description="Python package for interacting with Trane thermostats locally.",    # Short package description
     long_description=long_description,                       # Long package description
     long_description_content_type="text/markdown",
     url="https://github.com/MoralCode/lantrane",       # Url to your Git Repo
    #  download_url = 'https://github.com/MoralCode/lantrane/archive/'+new_version+'.tar.gz',
     packages=setuptools.find_packages(),                     # Searches throughout all dirs for files to include
     include_package_data=True,                               # Must be true to include files depicted in MANIFEST.in
     license_files=["LICENSE.md"],                               # License file
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
 )