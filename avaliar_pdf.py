import PyPDF2
from langdetect import detect
import pdfplumber
import fitz  # PyMuPDF
import pikepdf

# Functions -------------------------------------------------------------------

def extract_metadata(pdf_path):
    """Extracts metadata from the PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        title = metadata.get("/Title", "No Title Found")
        author = metadata.get("/Author", "No Author Found")
    
    return title, author


def count_images_with_alt_text(pdf_path):
    """Counts images with and without alternative text in a PDF."""
    total_images = 0
    images_with_alt_text = 0

    doc = fitz.open(pdf_path)
    for page in doc:
        images = page.get_images(full=True)
        total_images += len(images)

        for img in images:
            xref = img[0]

            # Try to find alternative text in the document structure
            for annot in page.annots():
                if annot.type[0] == 8:  # 8 = Figure/Image
                    alt_text = annot.info.get("Contents", "").strip()  # Try to get description
                    if alt_text:
                        images_with_alt_text += 1
                        break  # If Alt Text is found, no need to check further for this image

    images_without_alt_text = total_images - images_with_alt_text
    return images_without_alt_text


def detect_pdf_language(pdf_path):
    """Detects the language of the PDF."""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''.join(page.extract_text() or '' for page in pdf_reader.pages)
    
    if text.strip():
        return detect(text)
    return None


def pdf_only_image(pdf_path):
    """Checks if the PDF contains only images without text."""
    with fitz.open(pdf_path) as pdf:
        only_images = "Only Images"
        for page in pdf:
            text = page.get_text()
            if text.strip():  # If there is any text, it is not just images
                only_images = "PDF with text"
                break
    return only_images


def check_text_size(pdf_path, min_size=10):
    """Checks if there are texts with fonts smaller than the recommended minimum."""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text_info = page.get_text("dict")
            for block in text_info["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if span["size"] < min_size:
                            return False  # Text smaller than the recommended minimum
    return True


def check_headers(pdf_path):
    """Checks if the PDF has headings using larger fonts to identify headers."""
    headers_detected = False
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text_info = page.get_text("dict")
            for block in text_info["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if span["size"] >= 14:  # Assume larger fonts as headings
                            headers_detected = True
                            return headers_detected
    return headers_detected


def check_pdf_semantics(pdf_path):
    """Checks if the PDF has semantic markup ('tagged PDF')."""
    try:
        pdf = pikepdf.Pdf.open(pdf_path)
        return "/StructTreeRoot" in pdf.root  # PDF has semantic structure
    except:
        return False


# PDF Accessibility Check -----------------------------------------------------

def check_pdf_accessibility(pdf_path):
    """Runs an accessibility evaluation on the PDF."""
    accessibility_report = {
        "Title": None,
        "Author": None,
        "Language": None,
        "Tagged PDF": False,
        "Images without alt text": 0,
        "PDF only image": False,
        "Text size adequate": False,
        "Headers detected": False,
    }

    print("Evaluating PDF accessibility...\n")

    # Metadata
    title, author = extract_metadata(pdf_path)
    accessibility_report["Title"] = title
    accessibility_report["Author"] = author

    # Language detection
    language = detect_pdf_language(pdf_path)
    accessibility_report["Language"] = language

    # Semantic markup check
    accessibility_report["Tagged PDF"] = check_pdf_semantics(pdf_path)

    # Count images without alternative text
    accessibility_report["Images without alt text"] = count_images_with_alt_text(pdf_path)

    # Check if the PDF is image-only
    accessibility_report["PDF only image"] = pdf_only_image(pdf_path)

    # Minimum text size check
    accessibility_report["Text size adequate"] = check_text_size(pdf_path)

    # Detect headers
    accessibility_report["Headers detected"] = check_headers(pdf_path)

    return accessibility_report


# Run Analysis -----------------------------------------------------------

pdf_file_path = input("Enter PDF name: ")
pdf_file_path = "PDFS/" + pdf_file_path + ".pdf"

report = check_pdf_accessibility(pdf_file_path)

print("\nAccessibility Report -------------------------------------")

passed = 0
failed = 0

for key, value in report.items():
    if key == "Images without alt text":
        if value == 0:
            passed += 1
        else:
            failed += 1
    
    else:
        if value in [False, None, "No Title Found", "No Author Found", 0, "Only Images"]:
            failed += 1
        else:
            passed += 1
    print(f"{key}: {value}")

print("\nSummary ----------------------------------------------------------")
print(f"Passed: {passed}")
print(f"Failed: {failed}")