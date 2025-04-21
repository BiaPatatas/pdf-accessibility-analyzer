import fitz  # PyMuPDF
import requests

def get_links_info(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)

    external_links = []
    internal_links = []
    fake_links = []

    for page_num, page in enumerate(doc):
        links = page.get_links()
        for link in links:
            uri = link.get("uri", "")
            kind = link.get("kind", None)
            dest_page = link.get("page", None)

            if uri.startswith("http://") or uri.startswith("https://"):
                external_links.append(uri)
            elif kind == 1:  # internal link
                if dest_page is not None and 0 <= dest_page < total_pages:
                    internal_links.append((page_num, dest_page))
                else:
                    fake_links.append((page_num, "invalid internal"))
            else:
                if not uri and dest_page is None:
                    fake_links.append((page_num, "no uri or dest"))

    doc.close()
    return external_links, internal_links, fake_links


def check_external_links(links):
    results = []

    for link in links:
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            results.append(response.status_code == 200)
        except Exception:
            results.append(False)

    return results


if __name__ == "__main__":
    pdf_path = input("Caminho para o PDF: ").strip()

    external, internal, fake = get_links_info(pdf_path)
    checked_links = check_external_links(external)

    # Verificar se existe algum link válido
    link_valid = any(checked_links) or bool(internal) or bool(fake)

    # Imprimir o resultado final
    print("\nLink Valid:", link_valid)
