import requests
import os
import sys

# ================= CONFIGURAÇÃO =================
# Depois do deploy, troque pela URL real do seu projeto
URL_API = "COLOQUE_SUA_URL_AQUI/gerar-banner"
IMAGEM_TESTE = "teste_produto.jpg"
# =================================================

def testar():
    print("🚀 Teste Waynne AI Banner Generator...")

    if not os.path.exists(IMAGEM_TESTE):
        print(f"❌ ERRO: Coloque uma foto de produto chamada '{IMAGEM_TESTE}' na pasta")
        return False

    with open(IMAGEM_TESTE, "rb") as f:
        arquivos = {"file": (IMAGEM_TESTE, f, "image/jpeg")}
        print("📤 Enviando imagem...")

        try:
            resp = requests.post(URL_API, files=arquivos, timeout=60)

            if resp.status_code != 200:
                print(f"❌ ERRO HTTP {resp.status_code}")
                print(resp.text[:300])
                return False

            dados = resp.json()
            if dados.get("status") != "sucesso":
                print(f"❌ Falha: {dados}")
                return False

            extraidos = dados["dados_extraidos"]
            print("\n✅ SUCESSO! Dados extraídos:")
            print(f"   Produto: {extraidos['produto_nome_curto']}")
            print(f"   Categoria: {extraidos['categoria_skin']}")
            print(f"   Confiança: {extraidos['confianca_extracao']:.2%}")
            print(f"   Banner salvo em: {dados['caminho_banner']}")
            return True

        except Exception as e:
            print(f"❌ ERRO: {str(e)}")
            return False

if __name__ == "__main__":
    sucesso = testar()
    sys.exit(0 if sucesso else 1)
