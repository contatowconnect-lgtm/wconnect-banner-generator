"""Renderizador determinístico de banners WAYNNE AI (WADS).

Este módulo é o único responsável pela renderização PNG no MVP.
Ele recebe o contrato JSON canônico, lê o WADS em config/design_system.json
e produz pixels previsíveis com Pillow.

Regras importantes:
- não inventa dados;
- não escolhe categoria desconhecida;
- não altera a posição estrutural dos blocos;
- mantém o produto como elemento central;
- suporta 1:1 e 4:5;
- não depende do frontend para renderização.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont, ImageOps


BASE_DIR = Path(__file__).resolve().parent
DESIGN_SYSTEM_PATH = BASE_DIR / "config" / "design_system.json"
FONT_DIR = BASE_DIR / "fontes"
OUTPUT_DIR = BASE_DIR / "saida"


def _load_design_system() -> dict[str, Any]:
    with DESIGN_SYSTEM_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


WADS = _load_design_system()


def _hex(value: str, fallback: str = "#FFFFFF") -> tuple[int, int, int]:
    value = value or fallback
    value = value.lstrip("#")
    if len(value) != 6:
        value = fallback.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def _font(name: str, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    path = FONT_DIR / name
    if path.exists():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _font_bold(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return _font("Montserrat-Bold.ttf", size)


def _font_regular(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return _font("Roboto-Regular.ttf", size)


def _normalize_category(value: str) -> str:
    value = (value or "").lower().strip()
    return re.sub(r"[^a-z0-9]", "", value)


def _category_config(category: str) -> dict[str, Any]:
    key = _normalize_category(category)
    categories = WADS["categories"]
    if key not in categories:
        raise ValueError(f"Categoria WADS inválida ou ausente: {category!r}")
    return categories[key]


def _money(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)

    if number.is_integer():
        return f"R$ {number:,.0f}".replace(",", ".")
    return f"R$ {number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _safe_text(value: Any) -> str:
    return str(value).strip() if value not in (None, "") else ""


def _wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.ImageFont,
    max_width: int,
) -> list[str]:
    words = text.split()
    if not words:
        return []

    lines: list[str] = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        width = draw.textbbox((0, 0), candidate, font=font)[2]
        if width <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def _draw_wrapped(
    draw: ImageDraw.ImageDraw,
    text: str,
    xy: tuple[int, int],
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    max_width: int,
    spacing: int = 6,
    max_lines: int = 3,
) -> int:
    lines = _wrap_text(draw, text, font, max_width)[:max_lines]
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y = bbox[3] + spacing
    return y


def _fit_image(
    path: str,
    max_width: int,
    max_height: int,
) -> Image.Image | None:
    source = Path(path)
    if not source.exists():
        return None

    with Image.open(source) as original:
        image = original.convert("RGBA")

    image.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)

    # Não remove fundo por cor: isso pode destruir produtos brancos.
    # O MVP preserva a imagem original até termos uma etapa de recorte validada.
    return image


def _draw_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    canvas_width: int,
) -> int:
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    x = (canvas_width - width) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def _draw_category_tag(
    draw: ImageDraw.ImageDraw,
    label: str,
    color: tuple[int, int, int],
    x: int,
    y: int,
    font: ImageFont.ImageFont,
) -> None:
    bbox = draw.textbbox((0, 0), label, font=font)
    pad_x, pad_y = 18, 10
    width = bbox[2] - bbox[0] + pad_x * 2
    height = bbox[3] - bbox[1] + pad_y * 2
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=height // 2,
        fill=color,
    )
    draw.text(
        (x + pad_x, y + pad_y - 1),
        label,
        font=font,
        fill=(0, 0, 0),
    )


def _draw_price_area(
    draw: ImageDraw.ImageDraw,
    comercial: dict[str, Any],
    x: int,
    y: int,
    accent: tuple[int, int, int],
    width: int,
) -> int:
    original = _money(comercial.get("preco_original"))
    promo = _money(comercial.get("preco_promocional"))
    discount = comercial.get("desconto_percentual")
    installment = _safe_text(comercial.get("parcelamento"))

    if original:
        font_original = _font_regular(22)
        draw.text((x, y), original, font=font_original, fill=(150, 150, 150))
        bbox = draw.textbbox((x, y), original, font=font_original)
        mid_y = (bbox[1] + bbox[3]) // 2
        draw.line((bbox[0], mid_y, bbox[2], mid_y), fill=(150, 150, 150), width=2)
        y = bbox[3] + 6

    if promo:
        font_promo = _font_bold(54)
        draw.text((x, y), promo, font=font_promo, fill=accent)
        y = draw.textbbox((x, y), promo, font=font_promo)[3] + 4

    if discount not in (None, ""):
        try:
            discount_text = f"{float(discount):g}% OFF"
        except (TypeError, ValueError):
            discount_text = _safe_text(discount)
        font_discount = _font_bold(22)
        draw.text((x, y), discount_text, font=font_discount, fill=accent)
        y = draw.textbbox((x, y), discount_text, font=font_discount)[3] + 4

    if installment:
        font_installment = _font_regular(19)
        lines = _wrap_text(draw, installment, font_installment, width)
        for line in lines[:2]:
            draw.text((x, y), line, font=font_installment, fill=(210, 210, 210))
            y = draw.textbbox((x, y), line, font=font_installment)[3] + 3

    return y


def gerar_banner(dados: dict[str, Any], caminho_imagem: str) -> str:
    """Renderiza um banner WADS e retorna o caminho absoluto do PNG."""

    if not isinstance(dados, dict):
        raise ValueError("O contrato de produto precisa ser um objeto JSON.")

    produto = dados.get("produto") or {}
    comercial = dados.get("comercial") or {}
    conteudo = dados.get("conteudo") or {}
    banner = dados.get("banner") or {}

    nome = _safe_text(produto.get("nome"))
    marca = _safe_text(produto.get("marca"))
    categoria = _safe_text(produto.get("categoria"))
    cta = _safe_text(banner.get("cta"))
    formato = _safe_text(banner.get("formato")) or "1:1"

    if not nome:
        raise ValueError("O campo produto.nome é obrigatório para renderização.")
    if not categoria:
        raise ValueError("O campo produto.categoria é obrigatório para renderização.")

    category = _category_config(categoria)
    accent = _hex(category["color"])
    institutional = WADS["identity"]["colors_institutional"]
    blue = _hex(institutional["azul"])
    violet = _hex(institutional["violeta"])
    cyan = _hex(institutional["ciano"])

    formats = WADS["layout"]["formats"]
    if formato not in formats:
        raise ValueError(f"Formato WADS inválido: {formato}")
    width = int(formats[formato]["width"])
    height = int(formats[formato]["height"])

    safe = int(WADS["layout"]["margins"]["safe_area"])
    protection = int(WADS["layout"]["margins"]["protection"])

    # Fundo institucional discreto e determinístico.
    image = Image.new("RGB", (width, height), (8, 10, 24))
    draw = ImageDraw.Draw(image)

    # Faixas institucionais: azul → violeta → ciano.
    draw.rectangle((0, 0, width // 3, 8), fill=blue)
    draw.rectangle((width // 3, 0, 2 * width // 3, 8), fill=violet)
    draw.rectangle((2 * width // 3, 0, width, 8), fill=cyan)

    # Estrutura superior fixa: categoria | logo | trust badge.
    cat_font = _font_bold(22)
    _draw_category_tag(
        draw,
        category["label"],
        accent,
        safe,
        safe + 12,
        cat_font,
    )

    logo_font = _font_bold(27)
    logo = WADS["identity"]["logo_text"]
    logo_box = draw.textbbox((0, 0), logo, font=logo_font)
    draw.text(
        ((width - (logo_box[2] - logo_box[0])) // 2, safe + 17),
        logo,
        font=logo_font,
        fill=(255, 255, 255),
    )

    trust = "IA • AUTOMAÇÃO"
    trust_font = _font_regular(16)
    trust_box = draw.textbbox((0, 0), trust, font=trust_font)
    draw.rounded_rectangle(
        (
            width - safe - (trust_box[2] - trust_box[0]) - 20,
            safe + 10,
            width - safe,
            safe + 44,
        ),
        radius=17,
        outline=cyan,
        width=1,
    )
    draw.text(
        (
            width - safe - (trust_box[2] - trust_box[0]) - 10,
            safe + 18,
        ),
        trust,
        font=trust_font,
        fill=cyan,
    )

    top = safe + 72
    bottom = height - safe - 82

    # Produto permanece central: área reservada independente do conteúdo textual.
    image_area_top = top + 80
    image_area_bottom = int(height * (0.59 if formato == "1:1" else 0.61))
    product = _fit_image(
        caminho_imagem,
        width - protection * 2,
        max(180, image_area_bottom - image_area_top),
    )
    if product:
        px = (width - product.width) // 2
        py = image_area_top + (image_area_bottom - image_area_top - product.height) // 2
        image.paste(product, (px, py), product)

    # Nome e marca: sempre abaixo da imagem.
    name_font = _font_bold(38 if formato == "1:1" else 42)
    name_y = image_area_bottom + 18
    name_bottom = _draw_wrapped(
        draw,
        nome,
        (safe, name_y),
        name_font,
        (255, 255, 255),
        width - safe * 2,
        spacing=5,
        max_lines=2,
    )

    if marca:
        brand_font = _font_regular(20)
        draw.text((safe, name_bottom + 4), marca, font=brand_font, fill=(185, 190, 205))

    # Especificações e benefícios: apenas dados fornecidos.
    specs = [str(x).strip() for x in (conteudo.get("especificacoes") or []) if str(x).strip()]
    benefits = [str(x).strip() for x in (conteudo.get("beneficios") or []) if str(x).strip()]

    info_y = name_bottom + (34 if marca else 14)
    info_bottom = bottom - 130

    if specs:
        spec_font = _font_regular(17)
        draw.text((safe, info_y), "ESPECIFICAÇÕES", font=_font_bold(15), fill=accent)
        info_y += 25
        for spec in specs[:4]:
            next_y = _draw_wrapped(
                draw,
                f"• {spec}",
                (safe, info_y),
                spec_font,
                (205, 210, 220),
                int(width * 0.43),
                spacing=3,
                max_lines=2,
            )
            info_y = min(next_y + 2, info_bottom)

    if benefits:
        benefit_font = _font_regular(17)
        bx = int(width * 0.57)
        by = name_bottom + (34 if marca else 14)
        draw.text((bx, by), "BENEFÍCIOS", font=_font_bold(15), fill=accent)
        by += 25
        for benefit in benefits[:3]:
            next_y = _draw_wrapped(
                draw,
                f"• {benefit}",
                (bx, by),
                benefit_font,
                (205, 210, 220),
                width - safe - bx,
                spacing=3,
                max_lines=2,
            )
            by = min(next_y + 2, info_bottom)

    # Rodapé comercial fixo: preço à esquerda, CTA à direita.
    footer_y = height - safe - 92
    _draw_price_area(
        draw,
        comercial,
        safe,
        footer_y,
        accent,
        int(width * 0.48),
    )

    if cta:
        cta_font = _font_bold(22)
        cta_box = draw.textbbox((0, 0), cta, font=cta_font)
        cta_width = cta_box[2] - cta_box[0] + 36
        cta_height = cta_box[3] - cta_box[1] + 24
        cx = width - safe - cta_width
        cy = footer_y + 18
        draw.rounded_rectangle(
            (cx, cy, cx + cta_width, cy + cta_height),
            radius=cta_height // 2,
            fill=accent,
        )
        draw.text(
            (
                cx + (cta_width - (cta_box[2] - cta_box[0])) // 2,
                cy + 10,
            ),
            cta,
            font=cta_font,
            fill=(0, 0, 0),
        )

    # Footer institucional.
    footer_font = _font_regular(14)
    tagline = WADS["identity"]["tagline"]
    draw.text(
        (safe, height - safe - 18),
        tagline,
        font=footer_font,
        fill=(115, 120, 140),
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"banner_{formato.replace(':', 'x')}.png"
    image.save(output_path, format="PNG", optimize=True)
    return str(output_path)
