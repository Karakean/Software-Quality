#!/bin/bash

# List of Python versions to test
python_versions=("python2.7" "python3.7")

# Install requests for each Python version
for version in "${python_versions[@]}"
do
    # Create a virtual environment for each Python version
    virtualenv -p $version env

    # Activate the virtual environment
    source env/bin/activate

    # Install the requests library
    pip install requests

    # Test importing the requests library
    if python -c "import requests"; then
        echo "Requests library installation successful for Python version $version"
    else
        echo "Failed to import requests library for Python version $version"
    fi


    # Deactivate the virtual environment
    deactivate

    # Remove the virtual environment
    rm -rf env
done
