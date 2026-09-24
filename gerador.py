import json
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
from io import BytesIO
import os

def carregar_config():
    with open("config/design_system.json", "r", encoding="utf-8") as f:
        return json.load(f)

def remover_fundo(caminho_imagem):
    with open(caminho_imagem, "rb") as f:
        img = Image.open(BytesIO(f.read())).convert("RGBA")
    return remove(img)

def gerar_banner(dados_produto, caminho_imagem_original):
    config = carregar_config()
    skin_key = dados_produto["categoria_skin"].upper()
    skin = config["skins"].get(skin_key, config["skins"]["INFORMATICA"])

    # Carregar template
    canvas = Image.open("templates/template_base.png").convert("RGBA")
    draw = ImageDraw.Draw(canvas)

    # Processar produto
    produto = remover_fundo(caminho_imagem_original)
    w, h = produto.size
    ratio = min(600 / h, 1.0)
    novo_tamanho = (int(w * ratio), int(h * ratio))
    produto = produto.resize(novo_tamanho, Image.LANCZOS)

    # Centralizar produto
    x = (config["canvas_size"][0] - novo_tamanho[0]) // 2
    y = config["margins"]["safe_top"] + 100
    canvas.paste(produto, (x, y), produto)

    # Fontes
    try:
        f_titulo = ImageFont.truetype(config["fonts"]["title"]["file"], config["fonts"]["title"]["size"])
        f_preco = ImageFont.truetype(config["fonts"]["price"]["file"], config["fonts"]["price"]["size"])
        f_cat = ImageFont.truetype(config["fonts"]["category"]["file"], config["fonts"]["category"]["size"])
    except IOError:
        f_titulo = f_preco = f_cat = ImageFont.load_default()

    # Título
    draw.text(
        (config["margins"]["safe_left"], config["margins"]["safe_top"]),
        dados_produto["produto_nome_curto"].upper(),
        fill="#FFFFFF", font=f_titulo
    )

    # Preço
    if dados_produto["preco_visivel"]:
        texto_preco = f"R$ {dados_produto['preco_visivel']}"
        cor_preco = skin["primary"]
    else:
        texto_preco = "CONSULTE CONDIÇÕES"
        cor_preco = "#AAAAAA"

    draw.text(
        (config["margins"]["safe_left"], config["canvas_size"][1] - config["margins"]["safe_bottom"] - 120),
        texto_preco, fill=cor_preco, font=f_preco
    )

    # Categoria
    draw.text(
        (config["canvas_size"][0] - config["margins"]["safe_right"] - 300, config["margins"]["safe_top"] + 10),
        skin_key, fill=skin["accent"], font=f_cat
    )

    # Salvar
    os.makedirs("saida", exist_ok=True)
    caminho_saida = f"saida/banner_{dados_produto['produto_nome_curto'].replace(' ', '_')[:20]}.png"
    canvas.convert("RGB").save(caminho_saida, dpi=(config["dpi"], config["dpi"]))
    return caminho_saida
