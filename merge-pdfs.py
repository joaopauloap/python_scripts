import os
from pypdf import PdfReader, PdfWriter

def juntar_pdfs_em_pasta(pasta):
    escritor = PdfWriter()
    arquivos = sorted(f for f in os.listdir(pasta) if f.endswith(".pdf"))

    for nome_arquivo in arquivos:
        caminho = os.path.join(pasta, nome_arquivo)
        leitor = PdfReader(caminho)
        for pagina in leitor.pages:
            escritor.add_page(pagina)

    nome_saida = os.path.basename(pasta) + "_merge.pdf"
    caminho_saida = os.path.join(pasta, nome_saida)
    with open(caminho_saida, "wb") as f:
        escritor.write(f)

    print(f"✅ PDF mesclado salvo em: {caminho_saida}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        pasta = sys.argv[1]
    else:
        pasta = "."

    juntar_pdfs_em_pasta(pasta)
