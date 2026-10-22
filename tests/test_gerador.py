import io
import unittest
from PIL import Image

from gerador import FORMATOS, gerar_banners


class TestGeracaoBanners(unittest.TestCase):
    def setUp(self):
        image = Image.new("RGB", (320, 240), (230, 230, 230))
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        self.product_image = buffer.getvalue()

    def test_gera_png_nos_dois_formatos_oficiais(self):
        dados = {
            "produto": "Notebook de teste",
            "categoria": "informática",
            "preco_por": "R$ 1.459,90",
            "beneficios": ["Wi-Fi", "Bluetooth", "SSD", "Tela Full HD",
                           "USB-C", "Webcam", "Teclado ABNT", "Garantia informada"],
        }
        result = gerar_banners(dados, self.product_image)
        self.assertEqual(set(result), set(FORMATOS))
        for formato, conteudo in result.items():
            with Image.open(io.BytesIO(conteudo)) as banner:
                self.assertEqual(banner.format, "PNG")
                self.assertEqual(banner.size, FORMATOS[formato])

    def test_foto_invalida_falha_com_erro_claro(self):
        with self.assertRaisesRegex(ValueError, "foto do produto"):
            gerar_banners({"produto": "Teste"}, b"isto nao e imagem")


if __name__ == "__main__":
    unittest.main()
