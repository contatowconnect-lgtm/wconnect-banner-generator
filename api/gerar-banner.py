import base64
import json
import os

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from gerador import gerar_banners

app = FastAPI(title="WAYNNE AI Banner Generator")


def _dados_from_form(raw):
    if not raw:
        return {}
    try:
        value = json.loads(raw)
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="dados inválidos") from exc


def _extrair_com_openai(image_bytes):
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=400,
            detail="Envie os dados do produto ou configure OPENAI_API_KEY.",
        )

    client = OpenAI(api_key=api_key)
    prompt = """
Você é o extrator de dados do WAYNNE AI Banner Generator.
Retorne somente JSON válido, sem markdown.
Nunca invente preço, desconto, especificação ou benefício.
Use strings vazias ou listas vazias quando a informação não estiver visível.
Schema:
{"produto":"string","marca":"string","categoria":"eletronicos|game|moda|casa|beleza|esportes","preco_de":"string","preco_por":"string","desconto":"string","especificacoes":["string"],"beneficios":["string"],"chamada":"string"}
"""
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": [
                {"type": "text", "text": "Extraia os dados visíveis desta imagem."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ]},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


@app.post("/")
async def gerar(
    file: UploadFile = File(...),
    dados: str | None = Form(default=None),
):
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="imagem vazia")

    produto = _dados_from_form(dados)
    if not produto:
        produto = _extrair_com_openai(image_bytes)

    banners = gerar_banners(produto, image_bytes)

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
