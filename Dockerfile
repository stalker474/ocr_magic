# Start from a Python 3 base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the script and any necessary files into the container
COPY ocr_extraction_with_man.py .
COPY requirements.txt .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Tesseract OCR
RUN apt-get update \
    && apt-get install -y tesseract-ocr \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Command to run the script
ENTRYPOINT ["python", "./ocr_extraction_with_man.py"]
