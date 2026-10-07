export const CATEGORIAS = [
  "eletronicos",
  "informatica",
  "game",
  "moda",
  "casa",
  "beleza",
  "esporte"
];

export type TamanhoBanner = "feed" | "stories" | "retangular";

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
