from __future__ import annotations

import base64
import json
import mimetypes
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from openai import OpenAI

from gerador import gerar_banner
from validador import validar_banner


app = FastAPI(title="WAYNNE AI Banner Generator")

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path(__file__).resolve().parent
PROMPT_PATH = BASE_DIR / "config" / "prompt_extracao.txt"
OUTPUT_DIR = BASE_DIR / "saida"

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024


def ler_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise RuntimeError(f"Prompt de extração não encontrado: {PROMPT_PATH}")
    return PROMPT_PATH.read_text(encoding="utf-8")


def validar_contrato(dados: dict) -> None:
    """Validação mínima do contrato canônico antes do renderizador."""
    required_objects = ("produto", "comercial", "conteudo", "banner", "extracao")
    for key in required_objects:
        if not isinstance(dados.get(key), dict):
            raise ValueError(f"Contrato inválido: '{key}' deve ser um objeto.")

    produto = dados["produto"]
    if not produto.get("nome"):
        raise ValueError("Contrato inválido: produto.nome está ausente.")
    if not produto.get("categoria"):
        raise ValueError("Contrato inválido: produto.categoria está ausente.")

    formato = dados["banner"].get("formato") or "1:1"
    if formato not in {"1:1", "4:5"}:
        raise ValueError(f"Formato inválido: {formato}")


@app.post("/gerar-banner")
async def criar_banner(
    file: UploadFile = File(...),
    formato: str | None = Form(None),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Envie uma imagem JPEG, PNG ou WebP.",
        )

    conteudo = await file.read()

    if not conteudo:
        raise HTTPException(status_code=400, detail="A imagem enviada está vazia.")

    if len(conteudo) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="A imagem excede o limite de 10 MB.",
        )

    mime_type = file.content_type
    extensao = mimetypes.guess_extension(mime_type) or ".jpg"

    b64_imagem = base64.b64encode(conteudo).decode("utf-8")

    try:
        resp = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": ler_prompt()},
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Retorne somente o JSON canônico solicitado no prompt. "
                                "O formato final será definido pelo campo formato do formulário, "
                                "quando fornecido. Não invente dados."
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{b64_imagem}"
                            },
                        }
                    ],
                },
            ],
            response_format={"type": "json_object"},
        )

        dados = json.loads(resp.choices[0].message.content or "{}")
        validar_contrato(dados)

        if formato:
            if formato not in {"1:1", "4:5"}:
                raise HTTPException(status_code=400, detail="Formato deve ser 1:1 ou 4:5.")
            dados["banner"]["formato"] = formato

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            prefix="produto_",
            suffix=extensao,
            dir=OUTPUT_DIR,
            delete=False,
        ) as temp:
            temp.write(conteudo)
            caminho_temp = temp.name

        caminho_banner = gerar_banner(dados, caminho_temp)
        validacao = validar_banner(caminho_banner, dados["banner"]["formato"])

    except HTTPException:
        raise
    except (json.JSONDecodeError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Falha durante a geração do banner: {exc}",
        ) from exc

    return {
        "status": "sucesso",
        "validacao": validacao,
        "dados_extraidos": dados,
        "caminho_banner": caminho_banner,
    }
