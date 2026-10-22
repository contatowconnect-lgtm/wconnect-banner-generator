"""Normalização determinística dos dados usados pelo gerador de banners.

Este módulo não infere atributos comerciais: apenas limpa e normaliza valores
fornecidos pelo usuário ou extraídos e conferidos por ele.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

CATEGORIAS_VALIDAS = {
    "eletronicos",
    "informatica",
    "game",
    "moda",
    "casa",
    "beleza",
    "esporte",
}


def _sem_acentos(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value)
        if not unicodedata.combining(char)
    )


def normalizar_categoria(value: Any) -> str:
    categoria = _sem_acentos(str(value or "").strip().lower())
    categoria = re.sub(r"\s+", " ", categoria)
    aliases = {
        "eletronico": "eletronicos",
        "eletronicos": "eletronicos",
        "informatica": "informatica",
        "esportes": "esporte",
    }
    categoria = aliases.get(categoria, categoria)
    return categoria if categoria in CATEGORIAS_VALIDAS else "eletronicos"


def normalizar_beneficios(value: Any, limite: int = 8) -> list[str]:
    if isinstance(value, str):
        items = value.splitlines()
    elif isinstance(value, (list, tuple)):
        items = list(value)
    else:
        items = []

    max_items = max(0, min(int(limite), 8))
    if max_items == 0:
        return []

    resultado: list[str] = []
    vistos: set[str] = set()
    for item in items:
        texto = re.sub(r"\s+", " ", str(item or "")).strip()
        if not texto:
            continue
        chave = texto.casefold()
        if chave in vistos:
            continue
        vistos.add(chave)
        resultado.append(texto[:90])
        if len(resultado) >= max_items:
            break
    return resultado


def parse_brl(value: Any) -> float | None:
    raw = str(value or "").strip().replace("R$", "").replace("\u00a0", "").replace(" ", "")
    raw = re.sub(r"[^0-9,.-]", "", raw)
    if not raw or raw in {"-", ".", ","}:
        return None

    if "," in raw:
        # Padrão brasileiro: ponto para milhar e vírgula decimal.
        raw = raw.replace(".", "").replace(",", ".")
    elif raw.count(".") > 1:
        # Vários pontos sem vírgula são tratados como separadores de milhar.
        raw = raw.replace(".", "")
    elif raw.count(".") == 1 and len(raw.rsplit(".", 1)[1]) == 3:
        # Ex.: 1.459 deve ser interpretado como milhar, não como decimal.
        raw = raw.replace(".", "")

    try:
        parsed = float(raw)
    except ValueError:
        return None
    return parsed if parsed >= 0 else None


def formatar_brl(value: Any) -> str:
    texto = str(value or "").strip()
    if not texto:
        return ""
    if texto.upper().startswith("R$"):
        return "R$ " + texto[2:].strip()
    return "R$ " + texto
