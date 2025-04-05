import os
from pypdf import PdfMerger

def juntar_pdfs_em_pasta(pasta, nome_saida="pdf_merged.pdf"):
    merger = PdfMerger()

    # Lista todos os arquivos .pdf na pasta, ordenados pelo nome
    pdfs = sorted([f for f in os.listdir(pasta) if f.lower().endswith(".pdf")])

    if not pdfs:
        print("Nenhum PDF encontrado na pasta.")
        return

    print(f"PDFs encontrados ({len(pdfs)}):")
    for pdf in pdfs:
        caminho = os.path.join(pasta, pdf)
        print(f" - Adicionando: {pdf}")
        merger.append(caminho)

    saida = os.path.join(pasta, nome_saida)
    merger.write(saida)
    merger.close()
    print(f"\nPDF final salvo em: {saida}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pasta = sys.argv[1]
    else:
        pasta = "."

    juntar_pdfs_em_pasta(pasta)
