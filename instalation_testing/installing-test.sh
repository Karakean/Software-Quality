#!/bin/bash

# Test if pip is installed
if ! command -v pip &> /dev/null
then
	echo "Pip packet manager is not installed. Please install pip and try again!"
	exit 1
fi

# Instalation of requests library
pip install requests

# Test if requests library has been installed correctly
if python -c "import requests" &> /dev/null
then
	echo "Library requests has been installed correctly"
else
	echo "An error occurred while installing the requests library"
	exit 1
fi

# Perform a simple HTTP operation using the requests library
if python -c "import requests; response=requests.get('https://www.google.com'); print(response.status_code)" | grep -q "200"
then
	echo "Requests library is working correctly"
else
	echo "An error occurred while performing HTTP operations using the requests library"
	exit 1
fi

exit 0
