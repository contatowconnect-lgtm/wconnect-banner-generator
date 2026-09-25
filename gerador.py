
from PIL import Image, ImageDraw, ImageFont
import os

LARGURA, ALTURA = 1080, 1080

CORES = {
    "fundo": (10, 15, 55),
    "azul_neon": (0, 183, 255),
    "branco": (255, 255, 255),
    "cinza_claro": (220, 220, 220),
    "cinza_texto": (200, 200, 200),
    "verde_oferta": (0, 230, 90),
    "preco_destaque": (255, 255, 0),
    "cinza_riscado": (140, 140, 140)
}

CAMINHO_FONTES = "fontes/"

TAM = {
    "categoria": 22,
    "marca": 42,
    "produto": 34,
    "subtitulo": 22,
    "preco_de": 20,
    "preco_por": 48,
    "desconto": 22,
    "especificacoes": 19,
    "chamada": 24
}

def fonte(arquivo, tam):
    caminho = os.path.join(CAMINHO_FONTES, arquivo)
    if os.path.exists(caminho):
        return ImageFont.truetype(caminho, tam)
    return ImageFont.load_default()

def centralizar(draw, y, txt, f, cor):
    b = draw.textbbox((0, 0), txt, font=f)
    x = (LARGURA - (b[2] - b[0])) // 2
    draw.text((x, y), txt, font=f, fill=cor)

def esq(draw, x, y, txt, f, cor):
    draw.text((x, y), txt, font=f, fill=cor)

def carregar_foto(cam, lmax):
    if not os.path.exists(cam):
        return None, 0
    img = Image.open(cam).convert("RGBA")
    dados = img.getdata()
    nova = []
    for r, g, b, a in dados:
        if r > 245 and g > 245 and b > 245:
            nova.append((0, 0, 0, 0))
        else:
            nova.append((r, g, b, a))
    img.putdata(nova)
    prop = lmax / img.width
    return img.resize((lmax, int(img.height * prop)), Image.Resampling.LANCZOS), int(img.height * prop)

def gerar_banner(dados, caminho_imagem):
    """Recebe dados extraídos e caminho da imagem → retorna caminho do banner gerado"""
    img = Image.new("RGB", (LARGURA, ALTURA), CORES["fundo"])
    draw = ImageDraw.Draw(img)

    f_cat = fonte("Roboto-Regular.ttf", TAM["categoria"])
    f_marca = fonte("Montserrat-Bold.ttf", TAM["marca"])
    f_prod = fonte("Montserrat-Bold.ttf", TAM["produto"])
    f_sub = fonte("Roboto-Regular.ttf", TAM["subtitulo"])
    f_pde = fonte("Roboto-Regular.ttf", TAM["preco_de"])
    f_por = fonte("Montserrat-Bold.ttf", TAM["preco_por"])
    f_desc = fonte("Roboto-Regular.ttf", TAM["desconto"])
    f_esp = fonte("Roboto-Regular.ttf", TAM["especificacoes"])
    f_cham = fonte("Montserrat-Bold.ttf", TAM["chamada"])

    m = 50
    y = 25

    centralizar(draw, y, dados.get("categoria", ""), f_cat, CORES["azul_neon"])
    y += 32
    centralizar(draw, y, dados.get("marca", "WAYNNE AI"), f_marca, CORES["branco"])
    y += 60

    esq(draw, m, y, dados.get("produto", ""), f_prod, CORES["branco"])
    y += 45
    esq(draw, m, y, dados.get("subtitulo", ""), f_sub, CORES["cinza_claro"])
    y += 32

    preco_de = dados.get("preco_de", "")
    if preco_de:
        esq(draw, m, y, preco_de, f_pde, CORES["cinza_riscado"])
        bb = draw.textbbox((m, y), preco_de, font=f_pde)
        meio = (bb[1] + bb[3]) // 2
        draw.line((bb[0], meio, bb[2], meio), fill=CORES["cinza_riscado"], width=2)
    y += 28

    esq(draw, m, y, dados.get("preco_por", ""), f_por, CORES["preco_destaque"])
    bb_por = draw.textbbox((m, y), dados.get("preco_por", ""), font=f_por)
    desconto = dados.get("desconto", "")
    if desconto:
        draw.text((bb_por[2] + 20, y + 10), desconto, font=f_desc, fill=CORES["verde_oferta"])
    y += 60

    foto, alt_foto = carregar_foto(caminho_imagem, LARGURA - m * 2 - 80)
    if foto:
        img.paste(foto, (m + 40, y), foto)
        y += alt_foto + 8

    for item in dados.get("especificacoes", []):
        esq(draw, m, y, item, f_esp, CORES["cinza_texto"])
        y += 30

    y = ALTURA - 45
    centralizar(draw, y, dados.get("chamada", "Oferta imperdível! Garanta já o seu!"), f_cham, CORES["azul_neon"])

    os.makedirs("saida", exist_ok=True)
    caminho_saida = "saida/banner_final.png"
    img.save(caminho_saida)
    return caminho_saida
