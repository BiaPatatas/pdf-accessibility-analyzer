from pdfixsdk.Pdfix import *

def browseTags(parent: PdsStructElement):
    figures =0
    struct_type = parent.GetType(True)  # Obtém o tipo da estrutura

    if struct_type == "Figure":  # Verifica se a tag é <Figure>
        num_attrs = parent.GetNumAttrObjects()  # Obtém o número de atributos
        print("oi")
        figures += 1
        print(figures)


    count = parent.GetNumChildren()
    for i in range(count):
        if parent.GetChildType(i) == kPdsStructChildElement:
            child_element = structTree.GetStructElementFromObject(parent.GetChildObject(i))
            browseTags(child_element)


pdf_path = "PDF_testes_individuais/alt_text/pdf_com_alt_text.pdf"

pdfix = GetPdfix()
doc = pdfix.OpenDoc(pdf_path, "")

if doc:
    structTree = doc.GetStructTree()
    if structTree:
        rootElement = structTree.GetStructElementFromObject(structTree.GetObject())
        browseTags(rootElement)
    doc.Close()
else:
    print("Erro ao abrir o PDF.")
