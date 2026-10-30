import unittest

from normalizacao import (
    normalizar_categoria, normalizar_beneficios, parse_brl,
    formatar_brl, validar_dados_comerciais,
)


class TestNormalizacao(unittest.TestCase):
    def test_categoria_aceita_aliases_sem_perder_identidade(self):
        self.assertEqual(normalizar_categoria("Eletrônicos"), "eletronicos")
        self.assertEqual(normalizar_categoria("informática"), "informatica")
        self.assertEqual(normalizar_categoria("esportes"), "esporte")
        self.assertEqual(normalizar_categoria("GAME"), "game")

    def test_categoria_desconhecida_nao_e_classificada_como_eletronicos(self):
        with self.assertRaisesRegex(ValueError, "categoria"):
            normalizar_categoria("categoria inventada")

    def test_categoria_vazia_nao_e_classificada_como_eletronicos(self):
        with self.assertRaisesRegex(ValueError, "categoria"):
            normalizar_categoria("")

    def test_beneficios_limpos_e_limitados_a_oito(self):
        entrada = ["  Wi-Fi  ", "", None, "Bluetooth"] + [f"Benefício {i}" for i in range(10)]
        resultado = normalizar_beneficios(entrada)
        self.assertEqual(resultado[0], "Wi-Fi")
        self.assertEqual(resultado[1], "Bluetooth")
        self.assertEqual(len(resultado), 8)
        self.assertTrue(all(resultado))

    def test_beneficios_string_e_convertida_em_lista(self):
        self.assertEqual(normalizar_beneficios("Wi-Fi\\nBluetooth\\n\\nUSB-C"), ["Wi-Fi", "Bluetooth", "USB-C"])

    def test_preco_brasileiro_com_virgula(self):
        self.assertEqual(parse_brl("R$ 1.459,90"), 1459.90)

    def test_preco_brasileiro_com_ponto_decimal(self):
        self.assertEqual(parse_brl("1459.90"), 1459.90)

    def test_preco_invalido_nao_vira_zero(self):
        self.assertIsNone(parse_brl("consulte a loja"))

    def test_formatacao_de_preco_nao_duplica_simbolo(self):
        self.assertEqual(formatar_brl("R$ 99,90"), "R$ 99,90")
        self.assertEqual(formatar_brl("99,90"), "R$ 99,90")

    def test_rejeita_preco_atual_invalido(self):
        with self.assertRaisesRegex(ValueError, "preço atual"):
            validar_dados_comerciais({"preco_por": "consulte a loja"})

    def test_rejeita_preco_anterior_sem_preco_atual(self):
        with self.assertRaisesRegex(ValueError, "preço atual"):
            validar_dados_comerciais({"preco_de": "R$ 120,00"})

    def test_rejeita_preco_anterior_menor_ou_igual_ao_atual(self):
        with self.assertRaisesRegex(ValueError, "maior"):
            validar_dados_comerciais({
                "preco_por": "R$ 100,00", "preco_de": "R$ 100,00"
            })

    def test_aceita_preco_atual_e_anterior_validos(self):
        result = validar_dados_comerciais({
            "preco_por": "R$ 89,90", "preco_de": "R$ 120,00"
        })
        self.assertEqual(result["preco_por"], "R$ 89,90")
        self.assertEqual(result["preco_de"], "R$ 120,00")

    def test_rejeita_desconto_fora_do_intervalo(self):
        with self.assertRaisesRegex(ValueError, "desconto"):
            validar_dados_comerciais({"desconto": "120%"})

    def test_nao_inventa_preco_ou_desconto_ausente(self):
        result = validar_dados_comerciais({})
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
