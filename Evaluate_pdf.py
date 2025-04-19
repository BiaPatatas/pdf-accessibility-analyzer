import re
import PyPDF2
from langdetect import detect
import pdfplumber
import fitz  # PyMuPDF
import pikepdf
from pdfixsdk.Pdfix import *

# Functions -------------------------------------------------------------------

#Structure
def getStructTree(pdf_path: str):
    pdfix = GetPdfix()
    doc = pdfix.OpenDoc(pdf_path, "")
    if not doc:
        return None, None
    
    structTree = doc.GetStructTree()
    if not structTree:
        doc.Close()
        return None, None
    
    return doc, structTree


def extract_metadata(pdf_path):
    """Extracts metadata from the PDF."""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        title = metadata.get("/Title", "No Title Found")
        author = metadata.get("/Author", "No Author Found")
    
    return title, author


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
    """ Identifica listas não marcadas corretamente."""
    doc = fitz.open(pdf_path)
    
    list_pattern = re.compile(r'^(\d+\.|[a-zA-Z]\.|[-*•])\s')
    previous_was_list = False
    
    for page in doc:
        text_dict = page.get_text("dict")
        
        for block in text_dict.get("blocks", []):
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if list_pattern.match(text):
                        if previous_was_list:
                            return False
                        previous_was_list = True
                    else:
                        previous_was_list = False
    
    return True

def allFiguresHaveAltText(pdf_path: str):
    doc, structTree = getStructTree(pdf_path)
    if not doc or not structTree:
        return False
    
    def recursiveBrowse(parent: PdsStructElement):
        elem_type = parent.GetType(True)
        alt_text = parent.GetAlt()
        
        if elem_type.lower() == "figure" and not alt_text:
            return False
        
        for i in range(parent.GetNumChildren()):
            if parent.GetChildType(i) == kPdsStructChildElement:
                if not recursiveBrowse(structTree.GetStructElementFromObject(parent.GetChildObject(i))):
                    return False
        
        return True
    
    root_elem = structTree.GetStructElementFromObject(structTree.GetObject())
    result = recursiveBrowse(root_elem) if root_elem else False
    doc.Close()
    return result




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
        "PDF only image": False,
        "Lists marked as Lists": False,
        "Figures with alt text": False,
    }

    print("Evaluating PDF accessibility...\n")

    # Metadata
    title, author = extract_metadata(pdf_path)
    accessibility_report["Title"] = title
    accessibility_report["Author"] = author

    # Language detection
    language = detect_pdf_language(pdf_path)
    accessibility_report["Language"] = language

    # Check if the PDF is image-only
    accessibility_report["PDF only image"] = pdf_only_image(pdf_path)

    #Check if there is alt text in figures
    accessibility_report["Figures with alt text"] = allFiguresHaveAltText(pdf_path)

    #Lists
    accessibility_report["Lists marked as Lists"] = lists_not_marked_as_lists(pdf_path)

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