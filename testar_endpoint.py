import os
import sys

import requests

# ================= CONFIGURAÇÃO =================
URL_API = os.environ.get(
    "WAYNNE_API_URL",
    "COLOQUE_SUA_URL_AQUI/gerar-banner",
)
IMAGEM_TESTE = os.environ.get("WAYNNE_TEST_IMAGE", "teste_produto.jpg")
FORMATOS = ("1:1", "4:5")
TIMEOUT = 120
# =================================================


def validar_resposta(dados, formato):
    if dados.get("status") != "sucesso":
        raise AssertionError(f"Status inesperado: {dados}")

    extraidos = dados.get("dados_extraidos")
    if not isinstance(extraidos, dict):
        raise AssertionError("dados_extraidos ausente ou inválido.")

    for chave in ("produto", "comercial", "conteudo", "banner", "extracao"):
        if not isinstance(extraidos.get(chave), dict):
            raise AssertionError(f"Contrato inválido: '{chave}'.")

    produto = extraidos["produto"]
    if not produto.get("nome"):
        raise AssertionError("produto.nome ausente.")
    if not produto.get("categoria"):
        raise AssertionError("produto.categoria ausente.")

    if extraidos["banner"].get("formato") != formato:
        raise AssertionError(
            f"Formato retornado diferente do solicitado: "
            f"{extraidos['banner'].get('formato')} != {formato}"
        )

    caminho = dados.get("caminho_banner")
    if not caminho:
        raise AssertionError("caminho_banner ausente.")

    return extraidos, caminho


def testar_formato(formato):
    print(f"\n=== TESTE {formato} ===")

    with open(IMAGEM_TESTE, "rb") as f:
        arquivos = {"file": (IMAGEM_TESTE, f, "image/jpeg")}
        resposta = requests.post(
            URL_API,
            files=arquivos,
            data={"formato": formato},
            timeout=TIMEOUT,
        )

    if resposta.status_code != 200:
        raise AssertionError(
            f"HTTP {resposta.status_code}: {resposta.text[:500]}"
        )

    extraidos, caminho = validar_resposta(resposta.json(), formato)

    print("OK — contrato canônico recebido.")
    print(f"Produto: {extraidos['produto']['nome']}")
    print(f"Categoria: {extraidos['produto']['categoria']}")
    print(f"Confiança: {extraidos['extracao'].get('confianca')}")
    print(f"Banner: {caminho}")


def testar():
    print("WAYNNE AI — teste do endpoint /gerar-banner")

    if "COLOQUE_SUA_URL_AQUI" in URL_API:
        print(
            "ERRO: defina WAYNNE_API_URL ou edite URL_API antes do teste."
        )
        return False

    if not os.path.exists(IMAGEM_TESTE):
        print(f"ERRO: imagem não encontrada: {IMAGEM_TESTE}")
        return False

    try:
        for formato in FORMATOS:
            testar_formato(formato)
        print("\nRESULTADO: todos os testes de contrato passaram.")
        return True
    except Exception as exc:
        print(f"\nRESULTADO: falha — {exc}")
        return False


if __name__ == "__main__":
    sys.exit(0 if testar() else 1)
