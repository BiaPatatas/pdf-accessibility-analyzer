from pdfixsdk.Pdfix import *


def browseTags(parent: PdsStructElement):
    print(parent.GetType(True))
    count = parent.GetNumChildren()
    for i in range(0, count):
        if not parent.GetChildType(i) == kPdsStructChildElement:
            continue
        browseTags(structTree.GetStructElementFromObject(parent.GetChildObject(i)))

doc = GetPdfix().OpenDoc("PDF_testes_individuais\\alt_text\pdf_com_alt_text.pdf", "")
structTree = doc.GetStructTree()
childElem = structTree.GetStructElementFromObject(structTree.GetObject())
browseTags(childElem)


