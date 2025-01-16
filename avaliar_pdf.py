import PyPDF2
from langdetect import detect
import pdfplumber
import fitz  # PyMuPDF

def extract_metadata(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        metadata = reader.metadata
        title = metadata.get("/Title", "No Title Found")
        author = metadata.get("/Author", "No Author Found")
        tagged = "/MarkInfo" in metadata and metadata["/MarkInfo"].get("/Marked", False)
    
    return title, author, tagged

def count_images_with_alt_text(pdf_path):
    total_images = 0
    images_with_alt_text = 0

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            for img in page.images:
                total_images += 1
                if "alt" in img:  
                    images_with_alt_text += 1
    
    images_without_alt_text = total_images - images_with_alt_text

    return images_without_alt_text

def detect_pdf_language(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)

        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()

        language = detect(text)
    return language

def pdf_only_image(pdf_path):
    with open(pdf_path,"rb") as f:
        pdf = fitz.open(f)
        res = []
        for page in pdf:
            image_area = 0.0
            text_area = 0.0
            for b in page.get_text("blocks"):
                if '<image:' in b[4]:
                    r = fitz.Rect(b[:4])
                    image_area = image_area + abs(r)
                else:
                    r = fitz.Rect(b[:4])
                    text_area = text_area + abs(r)
            if image_area == 0.0 and text_area != 0.0:
                res.append(1)
            if text_area == 0.0 and image_area != 0.0:
                res.append(0) 
        return res



def contrast(pdf_path): # fitz(PyMuPDF)
    return 

def check_text_size(pdf_path):
    return 

def check_headers(pdf_path):
    return 

def check_screen_reader_accessibility(pdf_path): #pdfminer.six
    return 

def check_pdf_semantics(pdf_path): #pdfium
    return 



def check_pdf_accessibility(pdf_path):
    accessibility_report = {
        "Title": None,
        "Author": None,
        "language": None,
        "Tagged": False,
        "Images without alt text":0,
        "PDF only image":0,
    }

    # Metadados
    title, author, tagged = extract_metadata(pdf_path)
    accessibility_report["Title"] = title
    accessibility_report["Author"] = author
    accessibility_report["Tagged"] = tagged

    # Imagens e texto alternativo
    accessibility_report["Images without alt text"]= count_images_with_alt_text(pdf_path)

    # Linguagem
    language = detect_pdf_language(pdf_path)
    accessibility_report["language"] = language

    #only image
    accessibility_report["PDF only image"] = pdf_only_image(pdf_path)

    return accessibility_report


pdf_file_path = input("Name of pdf:")
pdf_file_path = "PDFS/" + pdf_file_path + ".pdf"
report = check_pdf_accessibility(pdf_file_path)

print("Evaluating accessibility ...")
print("")
print("Accessibility Report-------------------------------------------------------")


aprovado = 0
com_falha = 0

for key, value in report.items():
    if key == "Images without alt text":
        if value == 0:
            aprovado += 1
        else:
            com_falha +=1
    else:    
        if value in [False, None, "No Title Found", "No Author Found", 0]:
            com_falha += 1
        else:
            aprovado += 1
    print(f"{key}: {value}")

print("")
print("Summary-------------------------------------------------------")
print(f"Approved: {aprovado}")
print(f"Failed: {com_falha}")


