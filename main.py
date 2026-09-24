from fastapi import FastAPI, UploadFile, File
from gerador import gerar_banner
from openai import OpenAI
import json
import os
import base64

app = FastAPI(title="Waynne AI Banner Generator")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def ler_prompt():
    with open("config/prompt_extracao.txt", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/gerar-banner")
async def criar_banner(file: UploadFile = File(...)):
    conteudo = await file.read()

    # Codificar imagem para base64
    b64_imagem = base64.b64encode(conteudo).decode("utf-8")

    # Extrair dados com GPT-4o
    resp = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": ler_prompt()},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{b64_imagem}"
                }}
            ]}
        ],
        response_format={"type": "json_object"}
    )

    dados = json.loads(resp.choices[0].message.content)

    # Salvar imagem temporária
    nome_arquivo = file.filename or "imagem.jpg"
    caminho_temp = f"saida/temp_{nome_arquivo}"
    os.makedirs("saida", exist_ok=True)
    with open(caminho_temp, "wb") as f:
        f.write(conteudo)

    # Gerar banner
    caminho_banner = gerar_banner(dados, caminho_temp)

    return {
        "status": "sucesso",
        "dados_extraidos": dados,
        "caminho_banner": caminho_banner
    }
