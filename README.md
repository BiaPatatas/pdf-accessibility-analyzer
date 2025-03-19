# PDF Accessibility Checker

This script analyzes the accessibility of a PDF file by checking its metadata, language, semantic tagging, image alt-texts, font sizes, and headers.

## Features

-> Extracts PDF metadata (title and author)

-> Detects the language of the PDF

-> Checks if the PDF contains only images (without selectable text)

->Detects headers based on font size

## Requirements

Ensure you have the following Python libraries installed:

pip install PyMuPDF PyPDF2 langdetect pikepdf pdfplumber

## Usage

Run the script and provide the PDF filename when prompted:

python Evaluate_pdf.py

Place the PDF files in a folder named PDFS/ before running the script.

## Output

The script generates an accessibility report indicating which checks passed or failed, along with a summary of the results.