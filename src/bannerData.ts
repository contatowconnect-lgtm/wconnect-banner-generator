export const CATEGORIAS = [
  "eletronicos",
  "moda",
  "casa",
  "beleza",
  "esportes",
  "alimentacao",
  "servicos",
  "outros"
];

export interface BannerData {
  produto: string;
  preco: string;
  precoAntigo?: string;
  categoria: string;
  imagemProduto: string;
  descricao: string;
  botaoTexto: string;
  link: string;
  beneficios?: string[];
}
