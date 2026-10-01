"""Validador pós-renderização dos banners WAYNNE AI (WADS)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image


BASE_DIR = Path(__file__).resolve().parent
DESIGN_SYSTEM_PATH = BASE_DIR / "config" / "design_system.json"


def _load_wads() -> dict[str, Any]:
    with DESIGN_SYSTEM_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def validar_banner(caminho_banner: str, formato: str) -> dict[str, Any]:
    """Valida arquivo, formato e dimensões do PNG renderizado."""
    wads = _load_wads()
    formatos = wads["layout"]["formats"]

    if formato not in formatos:
        raise ValueError(f"Formato WADS inválido: {formato}")

    caminho = Path(caminho_banner).resolve()
    output_dir = (BASE_DIR / "saida").resolve()

    try:
        caminho.relative_to(output_dir)
    except ValueError as exc:
        raise ValueError("O banner gerado está fora do diretório oficial de saída.") from exc

    if not caminho.exists():
        raise ValueError(f"Banner não encontrado: {caminho}")

    if caminho.suffix.lower() != ".png":
        raise ValueError("O resultado final precisa ser PNG.")

    esperado = (
        int(formatos[formato]["width"]),
        int(formatos[formato]["height"]),
    )

    try:
        with Image.open(caminho) as imagem:
            tamanho = imagem.size
            tipo = imagem.format
            if tipo != "PNG":
                raise ValueError(f"Formato de imagem inválido: {tipo}")
            if tamanho != esperado:
                raise ValueError(
                    f"Dimensões inválidas: {tamanho}. Esperado: {esperado}."
                )

            # Força uma leitura dos pixels para detectar arquivo corrompido.
            imagem.verify()

    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(f"PNG inválido ou corrompido: {exc}") from exc

    return {
        "valido": True,
        "formato": formato,
        "dimensoes": {"largura": esperado[0], "altura": esperado[1]},
        "arquivo": str(caminho),
    }
