#!/bin/bash

# Download the source file from the Github server
wget https://github.com/psf/requests/archive/refs/tags/v2.28.0.tar.gz

# Unpacking the archive
tar -xzf v2.28.0.tar.gz

# Moving to the directory with the source code
cd requests-2.28.0/

# Installing the dependencies
pip install -r requirements-dev.txt

# Installing the library
python setup.py install

# Return to the original directory
cd ..

# Test importing the requests library
python -c "import requests"

# Confirm that the import was successful
echo "Import of requests library was successful"

# Clean up after yourself
rm -rf requests-2.28.0/ v2.28.0.tar.gz
