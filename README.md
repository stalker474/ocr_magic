# ocr_magic

## requirements
pandas
Pillow
pytesseract

## How to use with python3

OCR Extraction Script

This script extracts text from an image based on annotations provided in a CSV file.

Usage:
    python ocr_extraction_with_man.py <image_path> <annotations_csv_path> <output_csv_path>

Arguments:
    image_path            Path to the image file in PNG format.
    annotations_csv_path  Path to the annotations CSV file. The CSV should have the following columns:
                          - 'region_shape_attributes': A stringified JSON containing 'x', 'y', 'width', 'height'.
                          - 'region_attributes': A stringified JSON containing 'type' and 'label'. The 'type' can be
                            'text', 'num', or 'checkbox'. The 'label' is used for identifying the extracted content.
    output_csv_path       Path where the output CSV file will be saved.

Example:
    python ocr_extraction.py image.png annotations.csv output.csv

The script outputs a CSV file with two columns: 'Label' and 'Content'. The 'Label' column contains the labels
provided in the annotations, and the 'Content' column contains the extracted text or the status of checkboxes ('yes'/'no')

## How to dockerize

docker build -t ocr-script .

## How to use dockerized image

docker run -v path/to/data/folder:/data ocr-script /data/input.png /data/input.csv /data/output.csv


