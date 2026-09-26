export const CATEGORIAS = [
  "eletronicos",
  "moda",
  "casa",
  "beleza",
  "esportes",
  "alimentacao",
  "servicos",
  "outros"
] as const;

export type CategoriaId = typeof CATEGORIAS[number];

export interface BannerData {
  produto: string;
  preco: string;
  precoAntigo?: string;
  categoria: CategoriaId;
  imagemProduto: string;
  descricao: string;
  botaoTexto: string;
  link: string;
  beneficios?: string[];
}
