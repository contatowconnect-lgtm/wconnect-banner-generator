from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import os
import textwrap

WADS = {
    "institucional": {
        "azul": "#2E6BFF",
        "violeta": "#7B3FE4",
        "ciano": "#00D9FF",
        "fundo": "#0A0B10",
        "texto": "#F2F4F8",
        "muted": "#8991A6",
    },
    "categorias": {
        "eletronicos": "#C6FF00",
        "game": "#39FF14",
        "moda": "#FF1FBF",
        "casa": "#C1502E",
        "beleza": "#FFB3A3",
        "esportes": "#FF6B00",
    },
}

FORMATOS = {
    "1:1": (1080, 1080),
    "4:5": (1080, 1350),
}

FONTES = "fontes"


def _font(name, size):
    path = os.path.join(FONTES, name)
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _hex(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _fit_text(draw, text, font, max_width):
    text = str(text or "").strip()
    if not text:
        return []
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_wrapped(draw, xy, text, font, fill, max_width, spacing=8, max_lines=3):
    x, y = xy
    lines = _fit_text(draw, text, font, max_width)[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += draw.textbbox((x, y), line, font=font)[3] - draw.textbbox((x, y), line, font=font)[1] + spacing
    return y


def _gradient_background(size):
    w, h = size
    img = Image.new("RGB", size, _hex(WADS["institucional"]["fundo"]))
    px = img.load()
    blue = _hex(WADS["institucional"]["azul"])
    violet = _hex(WADS["institucional"]["violeta"])
    for y in range(h):
        for x in range(w):
            glow = max(0.0, 1.0 - (((x - w * .15) / w) ** 2 + ((y - h * .18) / h) ** 2) * 3.2)
            if glow > 0:
                px[x, y] = tuple(
                    int(px[x, y][i] * (1 - glow * .18) + violet[i] * glow * .18)
                    for i in range(3)
                )
    return img


def _prepare_product(raw, box):
    img = Image.open(io.BytesIO(raw)).convert("RGBA")
    # Preserve the product while fitting it into the central hero area.
    return ImageOps.contain(img, box, Image.Resampling.LANCZOS)


def _render(dados, raw, formato):
    width, height = FORMATOS[formato]
    img = _gradient_background((width, height))
    draw = ImageDraw.Draw(img)

    safe = 56
    category = str(dados.get("categoria", "eletronicos")).lower().strip()
    skin = WADS["categorias"].get(category, WADS["categorias"]["eletronicos"])
    skin_rgb = _hex(skin)

    f_tag = _font("Roboto-Regular.ttf", 25)
    f_logo = _font("Montserrat-Bold.ttf", 39)
    f_title = _font("Montserrat-Bold.ttf", 54 if formato == "1:1" else 58)
    f_specs = _font("Roboto-Regular.ttf", 24)
    f_price = _font("Montserrat-Bold.ttf", 52)
    f_small = _font("Roboto-Regular.ttf", 22)
    f_cta = _font("Montserrat-Bold.ttf", 24)
    f_footer = _font("Roboto-Regular.ttf", 18)

    # Category tag — fixed top-left position.
    tag = str(dados.get("categoria", "ELETRÔNICOS")).upper()
    bbox = draw.textbbox((0, 0), tag, font=f_tag)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.rounded_rectangle((safe, safe, safe + tw + 28, safe + th + 18), radius=18, fill=skin_rgb)
    draw.text((safe + 14, safe + 9), tag, font=f_tag, fill=(0, 0, 0))

    # WAYNNE AI identity. Official transparent logo can replace this fallback later.
    logo = "WAYNNE AI"
    lb = draw.textbbox((0, 0), logo, font=f_logo)
    draw.text(((width - (lb[2] - lb[0])) / 2, safe - 4), logo, font=f_logo, fill=_hex(WADS["institucional"]["texto"]))

    # Trust badge top-right.
    badge = "WADS"
    bb = draw.textbbox((0, 0), badge, font=f_small)
    bx = width - safe - (bb[2] - bb[0]) - 22
    draw.rounded_rectangle((bx, safe, width - safe, safe + 42), radius=14, outline=_hex(WADS["institucional"]["ciano"]), width=2)
    draw.text((bx + 11, safe + 9), badge, font=f_small, fill=_hex(WADS["institucional"]["ciano"]))

    # Central product area.
    hero_top = 165
    hero_bottom = int(height * 0.56)
    product = _prepare_product(raw, (width - safe * 2, hero_bottom - hero_top))
    px = (width - product.width) // 2
    py = hero_top + (hero_bottom - hero_top - product.height) // 2
    img.paste(product, (px, py), product)

    # Name and specs.
    name_y = hero_bottom + 24
    name = str(dados.get("produto", "Produto")).strip()
    name_y = _draw_wrapped(draw, (safe, name_y), name, f_title, _hex(WADS["institucional"]["texto"]), width - safe * 2, spacing=6, max_lines=2)

    specs = dados.get("especificacoes") or dados.get("beneficios") or []
    specs = [str(x).strip() for x in specs if str(x).strip()][:3]
    for item in specs:
        draw.text((safe, name_y + 8), "• " + item, font=f_specs, fill=_hex(WADS["institucional"]["muted"]))
        name_y += 34

    # Price area bottom-left.
    price_y = height - 185
    old = str(dados.get("preco_de") or dados.get("precoAntigo") or "").strip()
    price = str(dados.get("preco_por") or dados.get("preco") or "").strip()
    if old:
        draw.text((safe, price_y), f"De {old}", font=f_small, fill=(130, 135, 150))
    draw.text((safe, price_y + 28), price, font=f_price, fill=_hex(WADS["institucional"]["texto"]))

    # CTA bottom-right.
    cta = str(dados.get("chamada") or dados.get("botaoTexto") or "Confira a oferta").strip()
    ctb = draw.textbbox((0, 0), cta, font=f_cta)
    cw = min(ctb[2] - ctb[0] + 40, width // 2)
    ch = 60
    cx = width - safe - cw
    cy = price_y + 30
    draw.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=18, fill=_hex(WADS["institucional"]["azul"]))
    # Truncate CTA visually if needed.
    draw.text((cx + 20, cy + 17), cta[:28], font=f_cta, fill=(255, 255, 255))

    # Footer fixed at bottom.
    footer = "Tecnologia que te acompanha"
    fb = draw.textbbox((0, 0), footer, font=f_footer)
    draw.text(((width - (fb[2] - fb[0])) / 2, height - 45), footer, font=f_footer, fill=_hex(WADS["institucional"]["muted"]))

    out = io.BytesIO()
    img.save(out, format="PNG", optimize=True)
    return out.getvalue()


def gerar_banners(dados, imagem_bytes):
    return {formato: _render(dados, imagem_bytes, formato) for formato in FORMATOS}


def gerar_banner(dados, caminho_imagem):
    with open(caminho_imagem, "rb") as f:
        result = _render(dados, f.read(), "1:1")
    os.makedirs("saida", exist_ok=True)
    caminho_saida = "saida/banner_final.png"
    with open(caminho_saida, "wb") as f:
        f.write(result)
    return caminho_saida
