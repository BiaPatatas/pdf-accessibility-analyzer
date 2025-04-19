import re
import fitz


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

lists_correctly_marked = lists_not_marked_as_lists("PDF_testes_individuais\lists\lists_marked.pdf")
print("As listas estão corretamente marcadas?", lists_correctly_marked)