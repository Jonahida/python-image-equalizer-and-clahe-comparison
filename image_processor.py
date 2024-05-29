import numpy as np
import cv2 as cv
import os
import argparse

def equalize_histogram(image_path, output_path):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    assert img is not None, f"File {image_path} could not be read, check with os.path.exists()"
    equ = cv.equalizeHist(img)
    res = np.hstack((img, equ))  # stacking images side-by-side
    cv.imwrite(output_path, res)
    print(f"Equalized histogram saved to {output_path}")

def apply_clahe(image_path, output_path, clip_limit, tile_grid_size):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
    assert img is not None, f"File {image_path} could not be read, check with os.path.exists()"
    clahe = cv.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    cl_img = clahe.apply(img)
    res = np.hstack((img, cl_img))  # stacking images side-by-side
    cv.imwrite(output_path, res)
    print(f"CLAHE applied and saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Image processing script with histogram equalization and CLAHE.")
    parser.add_argument("input_path", type=str, help="Path to the input image file.")
    parser.add_argument("output_path", type=str, help="Path to save the processed image file.")
    parser.add_argument("conversion_type", choices=["equalize", "clahe"], help="Type of conversion to apply: 'equalize' or 'clahe'.")
    parser.add_argument("--clip_limit", type=float, default=100.0, help="Clip limit for CLAHE. Default is 100.0")
    parser.add_argument("--tile_grid_size", type=int, nargs=2, default=(8, 8), help="Tile grid size for CLAHE. Default is (8, 8)")

    args = parser.parse_args()

    if args.conversion_type == "equalize":
        equalize_histogram(args.input_path, args.output_path)
    elif args.conversion_type == "clahe":
        apply_clahe(args.input_path, args.output_path, args.clip_limit, tuple(args.tile_grid_size))

if __name__ == "__main__":
    main()
