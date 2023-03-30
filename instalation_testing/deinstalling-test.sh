#!/bin/bash

# Test if pip is installed
if ! command -v pip &> /dev/null
then
    echo "Pip packet manager is not installed. Please install pip and try again!"
    exit 1
fi

# Checking whether the requests library is installed
if python -c "import requests" &> /dev/null
then
    # Uninstall library requests
    pip uninstall requests -y
    echo "The requests library has been correctly removed."
else
    echo "The requests library is not installed."
fi

exit 0