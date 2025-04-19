from pdfixsdk.Pdfix import *

def browseTags(pdf_path: str):
    pdfix = GetPdfix()
    doc = pdfix.OpenDoc(pdf_path, "")
    if not doc:
        return
    
    structTree = doc.GetStructTree()
    if not structTree:
        return
    
    def recursiveBrowse(parent: PdsStructElement):
        elem_type = parent.GetType(True)
        alt_text = parent.GetAlt()
        print(elem_type, parent.GetText(True), alt_text)
        
        if elem_type.lower() == "figure":
            if alt_text:
                print("Imagem com texto alternativo encontrada!")
            else:
                print("Não há alt text")
        
        
        for i in range(parent.GetNumChildren()):
            if parent.GetChildType(i) == kPdsStructChildElement:
                recursiveBrowse(structTree.GetStructElementFromObject(parent.GetChildObject(i)))
    
    root_elem = structTree.GetStructElementFromObject(structTree.GetObject())
    if root_elem:
        recursiveBrowse(root_elem)
    
    doc.Close()

browseTags("PDF_testes_individuais/alt_text/pdf_sem_alt_text.pdf")





