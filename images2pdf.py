import os
from PIL import Image

# Diretório onde o script está
DIRETORIO_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Agora esse é o caminho raiz das imagens E o local de saída dos PDFs
CAMINHO_RAIZ = DIRETORIO_SCRIPT
DIRETORIO_SAIDA = DIRETORIO_SCRIPT

EXTENSOES_VALIDAS = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tif', '.tiff')
LARGURA_MAXIMA = 720
QUALIDADE_JPEG = 60

def redimensionar(imagem, largura_maxima):
    largura, altura = imagem.size
    if largura > largura_maxima:
        nova_altura = int((largura_maxima / largura) * altura)
        return imagem.resize((largura_maxima, nova_altura), Image.LANCZOS)
    return imagem

def processar_pasta(pasta_path):
    imagens = []
    arquivos = sorted(os.listdir(pasta_path))

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
                    frame = redimensionar(img.copy().convert('RGB'), LARGURA_MAXIMA)
                    imagens.append(frame)
            else:
                imagens.append(img)

        except Exception as e:
            print(f"❌ Erro na imagem '{caminho_completo}': {e}")

    if imagens:
        nome_pasta = os.path.basename(pasta_path)
        caminho_pdf = os.path.join(DIRETORIO_SAIDA, f"{nome_pasta}.pdf")
        imagens[0].save(
            caminho_pdf,
            save_all=True,
            append_images=imagens[1:],
            quality=QUALIDADE_JPEG,
            optimize=True
        )
        print(f"✅ PDF salvo: {caminho_pdf}")
    else:
        print(f"⚠️ Nenhuma imagem válida em: {pasta_path}")

# Coletar subpastas no mesmo diretório do script
subpastas = [os.path.join(CAMINHO_RAIZ, p) for p in os.listdir(CAMINHO_RAIZ) if os.path.isdir(os.path.join(CAMINHO_RAIZ, p))]

# Progresso simples
total = len(subpastas)
for i, pasta in enumerate(subpastas, 1):
    nome = os.path.basename(pasta)
    print(f"\n[{i}/{total}] Processando: {nome}")
    processar_pasta(pasta)
