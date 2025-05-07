import fitz  # PyMuPDF
import requests
from pdfixsdk.Pdfix import *

def check_headers(pdf_path: str):
    pdfix = GetPdfix()
    doc = pdfix.OpenDoc(pdf_path, "")
    if not doc:
        return
    
    structTree = doc.GetStructTree()
    if not structTree:
        return
    
    def recursiveBrowse(parent: PdsStructElement):
        elem_type = parent.GetType(True)
        
        if elem_type == "Table":
            has_thead = False
            for i in range(parent.GetNumChildren()):
                child_obj = parent.GetChildObject(i)  
                child_elem = structTree.GetStructElementFromObject(child_obj) 
                if not child_elem:
                    continue  
                if child_elem.GetType(True) == "THead":
                    has_thead = True
                    print("Há cabeçalho na tabela!")
                recursiveBrowse(child_elem)
            if not has_thead:
                print("Não há cabeçalho")
        else:
            print("Não há tabela!")
        
        for i in range(parent.GetNumChildren()):
            if parent.GetChildType(i) == kPdsStructChildElement:
                recursiveBrowse(structTree.GetStructElementFromObject(parent.GetChildObject(i)))
    
    root_elem = structTree.GetStructElementFromObject(structTree.GetObject())
    if root_elem:
        recursiveBrowse(root_elem)
    
    doc.Close()

check_headers("PDF_testes_individuais\\alt_text\pdf_com_alt_text.pdf")