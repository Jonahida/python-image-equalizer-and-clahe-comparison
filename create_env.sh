#!/bin/bash

# Function to check if python3.9 is installed
check_python() {
    if ! command -v python3.9 &> /dev/null; then
        echo "python3.9 is not installed on your system. Please install it before running this script."
        exit 1
    fi
}


check_python

# Create a virtual environment
echo "Creating virtual environment..."
python3.9 -m venv env39

if [[ $? -ne 0 ]]; then
    echo "Failed to create virtual environment. Please check your python3.9 installation."
    exit 1
fi

# Activate the virtual environment
source env39/bin/activate

# Upgrade pip
pip3 install --upgrade pip

# Use a here document to pipe the list of packages into pip install -r
pip3 install -r <(cat <<EOF
contourpy==1.2.1
cycler==0.12.1
fonttools==4.52.4
importlib_resources==6.4.0
kiwisolver==1.4.5
matplotlib==3.9.0
numpy==1.26.4
opencv-python==4.9.0.80
packaging==24.0
pillow==10.3.0
pyparsing==3.1.2
python-dateutil==2.9.0.post0
six==1.16.0
zipp==3.19.0
EOF
)

# Check if pip install was successful
if [[ $? -eq 0 ]]; then
    echo "All packages installed successfully."
else
    echo "There was an error installing the packages."
    exit 1
fi
