# Image Equalizer and CLAHE

This script processes images using OpenCV. It can either equalize the histogram of an image or apply  CLAHE (Contrast Limited Adaptive Histogram Equalization) to enhance the image's contrast.


## Main Components:

### Command-Line Arguments:
The script uses argparse to handle input and output file paths, the type of conversion, and optional parameters for CLAHE.

### Functions:
`equalize_histogram(image_path, output_path)`: Reads an image, equalizes its histogram, and saves the result.

`apply_clahe(image_path, output_path, clip_limit, tile_grid_size)`: Reads an image, applies CLAHE with specified parameters, and saves the result.

### Main Execution:
The script parses command-line arguments, determines the type of conversion, and calls the appropriate function with the provided arguments.
Usage:

1) To equalize an image histogram:

```bash
python script_name.py input_image.bmp output_image.bmp equalize
```

2) To apply CLAHE with optional parameters:

```bash
python script_name.py input_image.bmp output_image.bmp clahe --clip_limit 40.0 --tile_grid_size 8 8
```

This makes the script versatile for different image processing tasks based on user input.


# Notes

The `create_env.sh` script is a Bash script designed to set up a Python virtual environment and install a list of required Python packages. Here’s a general explanation of what the script does:

1) **Create a Virtual Environment**: The script creates an isolated Python environment using venv. This ensures that the packages installed in this environment do not affect the global Python installation.
2) **Install Dependencies**: The script installs a predefined list of Python packages into the virtual environment using pip.

## Run script to create a new virtual environment

```bash
bash create_env.sh
```
