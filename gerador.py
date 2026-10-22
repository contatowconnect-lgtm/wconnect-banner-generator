"""Renderizador determinístico de banners WAYNNE AI, alinhado ao WADS v1.7.0."""
from __future__ import annotations

import io
import os
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

from normalizacao import normalizar_categoria, normalizar_beneficios, formatar_brl

WADS = {
    "institucional": {
        "azul": "#2E6BFF", "violeta": "#7B3FE4", "ciano": "#00D9FF",
        "fundo": "#0A0B10", "texto": "#F2F4F8", "muted": "#8991A6",
    },
    "categorias": {
        "eletronicos": "#C6FF00", "informatica": "#B0B3B8",
        "game": "#39FF14", "moda": "#FF1F8F", "casa": "#C1502E",
        "beleza": "#FF8FA3", "esporte": "#FF6B00",
    },
}
ROTULOS = {
    "eletronicos": "ELETRÔNICOS", "informatica": "INFORMÁTICA",
    "game": "GAME", "moda": "MODA", "casa": "CASA",
    "beleza": "BELEZA", "esporte": "ESPORTE",
}
FORMATOS = {"1:1": (1080, 1080), "4:5": (1080, 1350)}
FONTES = "fontes"


def _rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _font(size, bold=False):
    candidates = (
        ["Montserrat-Bold.ttf", "DejaVuSans-Bold.ttf"] if bold
        else ["Roboto-Regular.ttf", "DejaVuSans.ttf"]
    )
    for name in candidates:
        paths = [os.path.join(FONTES, name), f"/usr/share/fonts/truetype/dejavu/{name}"]
        for path in paths:
            if os.path.isfile(path):
                try:
                    return ImageFont.truetype(path, size)
                except OSError:
                    pass
    return ImageFont.load_default()


def _text_width(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def _wrap(draw, text, font, max_width, max_lines=2):
    words = re.sub(r"\s+", " ", str(text or "")).strip().split()
    lines, current = [], ""
    for word in words:
        # Break unusually long tokens so they cannot escape the safe area.
        chunks, chunk = [], ""
        for char in word:
            candidate = chunk + char
            if chunk and _text_width(draw, candidate, font) > max_width:
                chunks.append(chunk)
                chunk = char
            else:
                chunk = candidate
        if chunk:
            chunks.append(chunk)

        for part in chunks:
            candidate = f"{current} {part}".strip()
            if _text_width(draw, candidate, font) <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = part
    if current:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and _text_width(draw, last + "…", font) > max_width:
            last = last[:-1].rstrip()
        lines[-1] = (last + "…") if last else "…"
    return lines


def _draw_fit(draw, text, xy, max_width, max_lines=2, max_size=40,
              min_size=13, fill="#F2F4F8", bold=True, align="left", gap=3):
    text = str(text or "").strip()
    if not text:
        return xy[1]
    chosen, lines = _font(min_size, bold), [text]
    for size in range(max_size, min_size - 1, -1):
        f = _font(size, bold)
        candidate = _wrap(draw, text, f, max_width, max_lines)
        if candidate and max(_text_width(draw, line, f) for line in candidate) <= max_width:
            chosen, lines = f, candidate
            break
    x, y = xy
    for line in lines:
        width = _text_width(draw, line, chosen)
        draw_x = x if align == "left" else x + max(0, (max_width - width) // 2)
        draw.text((draw_x, y), line, font=chosen, fill=fill)
        box = draw.textbbox((draw_x, y), line, font=chosen)
        y += max(1, box[3] - box[1]) + gap
    return y


def _background(size, accent):
    width, height = size
    base = Image.new("RGBA", size, _rgb(WADS["institucional"]["fundo"]) + (255,))
    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    draw.ellipse((-width * .18, -height * .22, width * .62, height * .48),
                 fill=_rgb(WADS["institucional"]["violeta"]) + (90,))
    draw.ellipse((width * .50, 0, width * 1.15, height * .60),
                 fill=_rgb(accent) + (42,))
    base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(max(30, width // 13))))
    ImageDraw.Draw(base).rounded_rectangle(
        (24, 24, width - 24, height - 24), radius=28,
        outline=(255, 255, 255, 24), width=2
    )
    return base


def _benefit_card(draw, x, y, width, height, text, accent):
    draw.rounded_rectangle((x, y, x + width, y + height), radius=14,
                           fill=(18, 20, 29), outline=_rgb(accent), width=2)
    draw.rounded_rectangle((x + 10, y + 13, x + 15, y + height - 13),
                           radius=3, fill=_rgb(accent))
    _draw_fit(draw, text, (x + 25, y + 8), width - 35,
              max_lines=3, max_size=18, min_size=11, gap=2)


def _render(dados, raw, formato):
    if formato not in FORMATOS:
        raise ValueError(f"Formato não suportado: {formato}")
    width, height = FORMATOS[formato]
    category = normalizar_categoria(dados.get("categoria"))
    accent = WADS["categorias"][category]
    image = _background((width, height), accent)
    draw = ImageDraw.Draw(image)
    label = ROTULOS[category]

    # Cabeçalho: marca e categoria dentro da área segura.
    tag_font = _font(17, True)
    tag_width = min(240, _text_width(draw, label, tag_font) + 28)
    draw.rounded_rectangle((54, 48, 54 + tag_width, 88), radius=12, fill=_rgb(accent))
    draw.text((68, 58), label, font=tag_font, fill=(10, 11, 16))
    brand_font = _font(31, True)
    brand = "WAYNNE AI"
    draw.text(((width - _text_width(draw, brand, brand_font)) // 2, 54),
              brand, font=brand_font, fill=WADS["institucional"]["texto"])
    draw.line((width // 2 - 68, 98, width // 2 + 68, 98),
              fill=_rgb(WADS["institucional"]["ciano"]), width=3)

    title = str(dados.get("produto") or "Produto").strip()[:120]
    subtitle = str(dados.get("subtitulo") or dados.get("chamada") or "").strip()[:140]
    title_end = _draw_fit(draw, title, (78, 118), width - 156, max_lines=2,
                           max_size=40, min_size=23, align="center")
    content_end = title_end
    if subtitle:
        subtitle_y = max(title_end + 5, 190)
        content_end = _draw_fit(draw, subtitle, (100, subtitle_y), width - 200,
                                max_lines=2, max_size=22, min_size=15,
                                fill=accent, align="center")

    # Região central dimensionada por formato, com foto real e sem placeholder.
    hero_top = max(270, content_end + 14)
    hero_bottom = 680 if formato == "1:1" else 875
    hero_width = 430
    hero_x = (width - hero_width) // 2
    draw.rounded_rectangle((hero_x - 8, hero_top - 8, hero_x + hero_width + 8,
                            hero_bottom + 8), radius=24, outline=_rgb(accent), width=2)
    try:
        product = Image.open(io.BytesIO(raw))
        product = ImageOps.exif_transpose(product).convert("RGBA")
        product.thumbnail((hero_width - 24, hero_bottom - hero_top - 24), Image.Resampling.LANCZOS)
    except Exception as exc:
        raise ValueError("A foto do produto não é uma imagem válida.") from exc
    image.alpha_composite(product, (hero_x + (hero_width - product.width) // 2,
                                    hero_top + (hero_bottom - hero_top - product.height) // 2))
    draw = ImageDraw.Draw(image)

    benefits = normalizar_beneficios(dados.get("beneficios") or dados.get("especificacoes") or [])
    card_width = 224
    card_height = 68 if formato == "1:1" else 82
    card_gap = 10 if formato == "1:1" else 12
    total_height = 4 * card_height + 3 * card_gap
    card_start_y = hero_top + max(0, (hero_bottom - hero_top - total_height) // 2)
    left_x, right_x = 48, width - 48 - card_width
    for index, benefit in enumerate(benefits[:8]):
        x = left_x if index % 2 == 0 else right_x
        y = card_start_y + (index // 2) * (card_height + card_gap)
        _benefit_card(draw, x, y, card_width, card_height, benefit, accent)

    # Preço/CTA num painel próprio, afastado da área de benefícios.
    price_top = height - (218 if formato == "1:1" else 245)
    draw.rounded_rectangle((58, price_top, width - 58, height - 78), radius=22,
                           fill=(12, 14, 22, 240), outline=(255, 255, 255, 34), width=2)
    old_price = str(dados.get("preco_de") or dados.get("precoAntigo") or "").strip()
    price = formatar_brl(dados.get("preco_por") or dados.get("preco") or "")
    if old_price:
        _draw_fit(draw, "De " + formatar_brl(old_price), (82, price_top + 15),
                  width // 2 - 100, max_lines=1, max_size=18, min_size=13,
                  fill=WADS["institucional"]["muted"], bold=False)
    _draw_fit(draw, price, (82, price_top + (43 if old_price else 22)),
              width // 2 - 105, max_lines=1, max_size=36, min_size=21)
    parts = []
    discount = str(dados.get("desconto") or "").strip()
    installments = str(dados.get("parcelas") or dados.get("parcelamento") or "").strip()
    if discount:
        parts.append(discount if "%" in discount else discount + "% OFF")
    if installments:
        parts.append(installments)
    if parts:
        _draw_fit(draw, " · ".join(parts), (82, price_top + 94),
                  width // 2 - 105, max_lines=2, max_size=15, min_size=11, fill=accent)

    cta = str(dados.get("cta") or dados.get("botaoTexto") or "VER OFERTA →").strip()
    cta_x, cta_y, cta_w, cta_h = width - 345, price_top + 43, 255, 66
    draw.rounded_rectangle((cta_x, cta_y, cta_x + cta_w, cta_y + cta_h),
                           radius=16, fill=_rgb(WADS["institucional"]["azul"]),
                           outline=_rgb(WADS["institucional"]["ciano"]), width=2)
    _draw_fit(draw, cta, (cta_x + 12, cta_y + 20), cta_w - 24,
              max_lines=1, max_size=20, min_size=12, align="center")

    footer_y = height - 55
    draw.line((70, footer_y - 12, width - 70, footer_y - 12),
              fill=(255, 255, 255, 28), width=1)
    footer = "WAYNNE AI  ·  TECNOLOGIA QUE TE ACOMPANHA"
    footer_font = _font(14, True)
    draw.text(((width - _text_width(draw, footer, footer_font)) // 2, footer_y),
              footer, font=footer_font, fill=WADS["institucional"]["muted"])

    output = io.BytesIO()
    image.convert("RGB").save(output, format="PNG", optimize=True)
    return output.getvalue()


def gerar_banners(dados, imagem_bytes):
    """Retorna PNGs nos dois formatos oficiais, com a mesma normalização."""
    payload = dict(dados or {})
    payload["categoria"] = normalizar_categoria(payload.get("categoria"))
    payload["beneficios"] = normalizar_beneficios(
        payload.get("beneficios") or payload.get("especificacoes") or []
    )
    return {formato: _render(payload, imagem_bytes, formato) for formato in FORMATOS}


def gerar_banner(dados, caminho_imagem):
    with open(caminho_imagem, "rb") as arquivo:
        result = _render(dados, arquivo.read(), "1:1")
    os.makedirs("saida", exist_ok=True)
    caminho_saida = "saida/banner_final.png"
    with open(caminho_saida, "wb") as arquivo:
        arquivo.write(result)
    return caminho_saida
