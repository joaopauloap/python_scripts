from io import BytesIO
import os
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))
CAMINHO_RAIZ = DIRETORIO_SCRIPT
DIRETORIO_SAIDA = DIRETORIO_SCRIPT

EXTENSOES_VALIDAS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff')
LARGURA_MAXIMA = 500


def redimensionar(imagem, largura_maxima):
    largura, altura = imagem.size
    if largura > largura_maxima:
        nova_altura = int((largura_maxima / largura) * altura)
        return imagem.resize((largura_maxima, nova_altura), Image.LANCZOS)
    return imagem


def aplicar_ocr_em_imagem(imagem, canvas_pdf, largura, altura):
    # Comprimir a imagem em JPEG com qualidade 40
    buffer = BytesIO()
    imagem.save(buffer, format="JPEG", quality=40)
    buffer.seek(0)

    ocr = pytesseract.image_to_data(imagem, lang="por", output_type=pytesseract.Output.DICT)
    canvas_pdf.drawImage(ImageReader(buffer), 0, 0, width=largura, height=altura)

    n = len(ocr['text'])
    for i in range(n):
        if int(ocr['conf'][i]) > 60:
            texto = ocr['text'][i].strip()
            if texto:
                x = ocr['left'][i]
                y = altura - ocr['top'][i] - ocr['height'][i]
                canvas_pdf.setFont("Helvetica", 8)
                canvas_pdf.setFillColorRGB(1, 1, 1, alpha=0)
                canvas_pdf.drawString(x, y, texto)


def processar_pasta(pasta_path):
    arquivos = sorted(os.listdir(pasta_path))
    imagens = []

    for nome_arquivo in arquivos:
        caminho_completo = os.path.join(pasta_path, nome_arquivo)
        if not os.path.isfile(caminho_completo):
            continue
        if not nome_arquivo.lower().endswith(EXTENSOES_VALIDAS):
            continue
        try:
            with Image.open(caminho_completo) as teste:
                teste.verify()

            img = Image.open(caminho_completo).convert('RGB')
            img = redimensionar(img, LARGURA_MAXIMA)

            if hasattr(img, "n_frames") and img.n_frames > 1:
                for i in range(img.n_frames):
                    img.seek(i)
                    imagens.append(redimensionar(img.copy().convert('RGB'), LARGURA_MAXIMA))
            else:
                imagens.append(img)

        except Exception as e:
            print(f"❌ Erro na imagem '{caminho_completo}': {e}")

    if imagens:
        nome_pasta = os.path.basename(pasta_path)
        caminho_pdf = os.path.join(DIRETORIO_SAIDA, f"{nome_pasta}.pdf")
        largura, altura = imagens[0].size

        c = canvas.Canvas(caminho_pdf, pagesize=(largura, altura))
        for imagem in imagens:
            aplicar_ocr_em_imagem(imagem, c, *imagem.size)
            c.showPage()
        c.save()

        print(f"✅ PDF com OCR salvo: {caminho_pdf}")
    else:
        print(f"⚠️ Nenhuma imagem válida em: {pasta_path}")


# Processa todas as subpastas
subpastas = [os.path.join(CAMINHO_RAIZ, p) for p in os.listdir(CAMINHO_RAIZ) if os.path.isdir(os.path.join(CAMINHO_RAIZ, p))]

total = len(subpastas)
for i, pasta in enumerate(subpastas, 1):
    nome = os.path.basename(pasta)
    print(f"\n[{i}/{total}] Processando: {nome}")
    processar_pasta(pasta)