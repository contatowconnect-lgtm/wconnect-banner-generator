import base64
import json
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from gerador import gerar_banners
from normalizacao import normalizar_categoria, normalizar_beneficios

app = FastAPI(title="WAYNNE AI Banner Generator")


def _dados_from_form(raw):
    if not raw:
        return {}
    try:
        value = json.loads(raw)
        if not isinstance(value, dict):
            raise HTTPException(status_code=400, detail="Os dados do produto devem ser um objeto JSON.")
        return value
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Dados do produto inválidos.") from exc


def _extrair_com_openai(image_bytes, content_type="image/jpeg"):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="A extração automática não está configurada. Preencha os dados manualmente ou configure OPENAI_API_KEY.",
        )

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        mime = content_type if content_type in {"image/png", "image/jpeg", "image/webp"} else "image/jpeg"
        b64 = base64.b64encode(image_bytes).decode("ascii")
        prompt = """
Você extrai dados visíveis de catálogos para o WAYNNE AI Banner Generator.
Retorne somente JSON válido. Nunca invente preços, desconto, especificações,
parcelas, garantias, frete ou benefícios. Se algo não estiver visível ou legível,
use string vazia ou lista vazia. O usuário revisará os dados antes de publicar.
Schema:
{"produto":"string","marca":"string","categoria":"eletronicos|informatica|game|moda|casa|beleza|esporte",
"preco_de":"string","preco_por":"string","desconto":"string",
"especificacoes":["string"],"beneficios":["string (até 8)"],
"subtitulo":"string","chamada":"string","cta":"string","parcelas":"string"}
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Extraia apenas os dados visíveis desta imagem."},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ]},
            ],
            response_format={"type": "json_object"},
            temperature=0,
        )
        result = json.loads(response.choices[0].message.content or "{}")
        if not isinstance(result, dict):
            raise ValueError("A extração não retornou um objeto.")
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível extrair os dados deste catálogo. Confira a imagem e tente novamente.",
        ) from exc


def _validar_imagem(image_bytes):
    if not image_bytes:
        raise HTTPException(status_code=400, detail="A imagem enviada está vazia.")
    if len(image_bytes) > 4 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="A imagem ultrapassa o limite de 4 MB.")
    try:
        with Image.open(__import__("io").BytesIO(image_bytes)) as image:
            image.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise HTTPException(status_code=400, detail="Envie uma imagem PNG, JPEG ou WebP válida.") from exc


def _normalizar_dados(raw):
    dados = dict(raw or {})
    dados["categoria"] = normalizar_categoria(dados.get("categoria"))
    beneficios = dados.get("beneficios") or dados.get("especificacoes") or []
    dados["beneficios"] = normalizar_beneficios(beneficios)
    if not dados.get("produto"):
        raise HTTPException(status_code=400, detail="Informe o nome do produto antes de gerar o banner.")
    return dados


@app.get("/")
async def health():
    return {"service": "WAYNNE AI Banner Generator", "status": "ok"}


@app.post("/")
@app.post("/api/gerar-banner")
async def gerar(
    file: UploadFile = File(...),
    dados: str | None = Form(default=None),
):
    image_bytes = await file.read()
    _validar_imagem(image_bytes)

    produto = _dados_from_form(dados)
    if not produto:
        produto = _extrair_com_openai(image_bytes, file.content_type or "image/jpeg")
    produto = _normalizar_dados(produto)

    try:
        banners = gerar_banners(produto, image_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return JSONResponse({
        "status": "sucesso",
        "dados": produto,
        "formatos": {
            formato: {
                "mime": "image/png",
                "base64": base64.b64encode(conteudo).decode("ascii"),
            }
            for formato, conteudo in banners.items()
        },
    })
