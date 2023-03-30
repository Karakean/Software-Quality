#!/bin/bash

# deinstall current version of requests
sudo ./deinstalling-test.sh

# install latest version of requests
pip install --upgrade requests

# check if latest version is installed
python -c "import requests; print(requests.__version__)"