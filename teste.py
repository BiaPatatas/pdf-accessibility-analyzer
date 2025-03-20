import fitz  # PyMuPDF
from langdetect import detect

def lists_marked_as_lists(pdf_path):
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
    """Checks if tables are correctly marked in the PDF."""
    doc = fitz.open(pdf_path)
    tables_found = 0
    
    for page in doc:
        if page.find_tables():  
            tables_found += 1
    
    return tables_found > 0

def links_identified(pdf_path):
    """Checks if links are properly tagged and have descriptive text."""
    doc = fitz.open(pdf_path)
    links_found = 0
    
    for page in doc:
        links = page.get_links()
        if links:
            links_found += len(links)
    
    return links_found > 0

def check_pdf_accessibility(pdf_path):
    """Runs an accessibility evaluation on the PDF."""
    lists_report = lists_marked_as_lists(pdf_path)
    accessibility_report = {
        "Lists properly marked": lists_report,
        "Tables properly marked": tables_marked_as_tables(pdf_path),
        "Links properly identified": links_identified(pdf_path),
    }
    
    return accessibility_report

pdf_file_path = input("Enter PDF name: ")
pdf_file_path = "PDF_testes_individuais/" + pdf_file_path + ".pdf"

report = check_pdf_accessibility(pdf_file_path)

print("\nAccessibility Report -------------------------------------")
for key, value in report.items():
    print(f"{key}: {value}")
