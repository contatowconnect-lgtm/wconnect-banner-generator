"""Normalização determinística dos dados usados pelo gerador de banners.

Este módulo não infere atributos comerciais: apenas limpa e valida valores
fornecidos pelo usuário ou extraídos e conferidos por ele.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Any

CATEGORIAS_VALIDAS = {
    "eletronicos", "informatica", "game", "moda", "casa", "beleza", "esporte",
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
    if categoria not in CATEGORIAS_VALIDAS:
        raise ValueError("Informe uma categoria válida para o produto.")
    return categoria


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
        raw = raw.replace(".", "").replace(",", ".")
    elif raw.count(".") > 1:
        raw = raw.replace(".", "")
    elif raw.count(".") == 1 and len(raw.rsplit(".", 1)[1]) == 3:
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


def validar_dados_comerciais(dados: dict[str, Any]) -> dict[str, str]:
    """Valida somente valores comerciais explicitamente informados."""
    result: dict[str, str] = {}
    atual_raw = str(dados.get("preco_por") or dados.get("preco") or "").strip()
    anterior_raw = str(dados.get("preco_de") or dados.get("precoAntigo") or "").strip()

    atual = parse_brl(atual_raw) if atual_raw else None
    anterior = parse_brl(anterior_raw) if anterior_raw else None

    if atual_raw and atual is None:
        raise ValueError("O preço atual informado é inválido. Confira o valor em reais.")
    if anterior_raw and anterior is None:
        raise ValueError("O preço anterior informado é inválido. Confira o valor em reais.")
    if anterior_raw and not atual_raw:
        raise ValueError("Informe o preço atual para usar um preço anterior.")
    if anterior is not None and atual is not None and anterior <= atual:
        raise ValueError("O preço anterior precisa ser maior que o preço atual.")

    if atual_raw:
        result["preco_por"] = formatar_brl(atual_raw)
    if anterior_raw:
        result["preco_de"] = formatar_brl(anterior_raw)

    desconto_raw = str(dados.get("desconto") or "").strip()
    if desconto_raw:
        match = re.fullmatch(r"(\d+(?:[.,]\d+)?)\s*%?", desconto_raw)
        if not match:
            raise ValueError("O desconto deve ser informado como percentual numérico confirmado.")
        desconto = float(match.group(1).replace(",", "."))
        if not 0 < desconto <= 100:
            raise ValueError("O desconto deve ser maior que 0% e não pode ultrapassar 100%.")
        result["desconto"] = f"{desconto:g}%"

    parcelas = str(dados.get("parcelas") or dados.get("parcelamento") or "").strip()
    if parcelas:
        result["parcelas"] = parcelas
    return result
