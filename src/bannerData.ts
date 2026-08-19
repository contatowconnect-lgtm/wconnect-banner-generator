export interface BannerData {
  produto: string;
  preco: string;
  precoAntigo?: string;
  categoria: string;
  imagemProduto: string;
  descricao?: string;
  botaoTexto: string;
  link?: string;
}

export const CATEGORIAS = [
  { id: 'eletronicos', nome: 'Eletrônicos', cor: '#2563EB' },
  { id: 'moda', nome: 'Moda', cor: '#DC2626' },
  { id: 'casa', nome: 'Casa', cor: '#059669' },
  { id: 'beleza', nome: 'Beleza', cor: '#D97706' },
  { id: 'esportes', nome: 'Esportes', cor: '#7C3AED' },
] as const;

export type CategoriaId = typeof CATEGORIAS[number]['id'];

export const TAMANHOS = {
  feed: { largura: 1080, altura: 1080 },
  stories: { largura: 1080, altura: 1920 },
} as const;

export type TamanhoBanner = keyof typeof TAMANHOS;
