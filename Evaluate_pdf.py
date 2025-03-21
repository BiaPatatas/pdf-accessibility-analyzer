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

def lists_not_marked_as_lists(pdf_path):
    """ Identifies unmarked lists."""
    doc = fitz.open(pdf_path)
    unmarked_lists = 0
    unmarked_pages = []
    
    for page_num, page in enumerate(doc, start=1):
        text_dict = page.get_text("dict")
        page_has_unmarked_list = False
        
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if text.startswith(('- ', '* ', '•')):
                        page_has_unmarked_list = True
                 
        
        if page_has_unmarked_list:
            unmarked_lists += 1
            unmarked_pages.append(page_num)
            return False
       
    return True


def tables_marked_as_tables(pdf_path):
    pass

def links_identified(pdf_path):
    pass


# PDF Accessibility Check -----------------------------------------------------

def check_pdf_accessibility(pdf_path):
    """Runs an accessibility evaluation on the PDF."""
    accessibility_report = {
        "Title": None,
        "Author": None,
        "Language": None,
        "Images without alt text": 0,
        "PDF only image": False,
        "Lists marked as Lists": False,
    }

    print("Evaluating PDF accessibility...\n")

    # Metadata
    title, author = extract_metadata(pdf_path)
    accessibility_report["Title"] = title
    accessibility_report["Author"] = author

    # Language detection
    language = detect_pdf_language(pdf_path)
    accessibility_report["Language"] = language

    # Count images without alternative text
    accessibility_report["Images without alt text"] = count_images_with_alt_text(pdf_path)

    # Check if the PDF is image-only
    accessibility_report["PDF only image"] = pdf_only_image(pdf_path)

    #Lists
    accessibility_report["Lists marked as Lists"] = lists_not_marked_as_lists(pdf_path)

    return accessibility_report


# Run Analysis -----------------------------------------------------------

pdf_file_path = input("Enter PDF name: ")
pdf_file_path = "PDF_testes_individuais/lists/" + pdf_file_path + ".pdf"

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