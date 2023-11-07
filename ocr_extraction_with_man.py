
"""OCR Extraction Script

This script extracts text from an image based on annotations provided in a CSV file.

Usage:
    python ocr_extraction.py <image_path> <annotations_csv_path> <output_csv_path>

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
provided in the annotations, and the 'Content' column contains the extracted text or the status of checkboxes ('yes'/'no').
"""

import sys
import pandas as pd
from PIL import Image
import pytesseract

def is_checkbox_checked_with_x(checkbox_image):
    # Convert image to grayscale
    gray = checkbox_image.convert('L')
    
    # Use a threshold to get a binary image (binarization)
    thresh = 128
    fn = lambda x: 255 if x > thresh else 0
    binary_image = gray.point(fn, mode='1')
    
    # Apply OCR to the binary image to detect the presence of "X"
    detected_text = pytesseract.image_to_string(binary_image, config='--psm 10 -c tessedit_char_whitelist=Xx')
    
    # Check if "X" is detected in the checkbox area
    return "X" in detected_text or "x" in detected_text

def main(image_path, annotations_csv_path, output_csv_path):
    # Load the annotations and image
    annotations_df = pd.read_csv(annotations_csv_path)
    png_image = Image.open(image_path)

    # Convert string representations of dictionaries to actual dictionaries
    annotations_df['region_shape_attributes'] = annotations_df['region_shape_attributes'].apply(eval)
    annotations_df['region_attributes'] = annotations_df['region_attributes'].apply(eval)

    # Process annotations and extract text or checkbox status
    output_data = []
    for _, row in annotations_df.iterrows():
        region_type = row['region_attributes']['type']
        label = row['region_attributes']['label']
        x = row['region_shape_attributes']['x']
        y = row['region_shape_attributes']['y']
        width = row['region_shape_attributes']['width']
        height = row['region_shape_attributes']['height']
        cropped_image = png_image.crop((x, y, x + width, y + height))

        if region_type == 'text' or region_type == 'num':
            text = pytesseract.image_to_string(cropped_image, config='--psm 6').strip()
            output_data.append({'Label': label, 'Content': text if text else 'no text detected'})
        elif region_type == 'checkbox':
            is_checked = is_checkbox_checked_with_x(cropped_image)
            output_data.append({'Label': label, 'Content': 'yes' if is_checked else 'no'})
        elif region_type == 'image':
            continue  # Images are not included in the CSV
        else:
            output_data.append({'Label': label, 'Content': 'unrecognized region type'})

    # Create a DataFrame from the output data
    output_df = pd.DataFrame(output_data)

    # Save the results to the specified CSV file path
    output_df.to_csv(output_csv_path, index=False)
    print(f"Output saved to {output_csv_path}")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
    elif len(sys.argv) != 4:
        print("Incorrect number of arguments provided.", file=sys.stderr)
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

