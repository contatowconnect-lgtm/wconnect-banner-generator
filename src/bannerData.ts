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
 { id: 'eletronicos', nome: 'Eletrônico', cor: '#C6FF00' },
{ id: 'informatica', nome: 'Informática', cor: '#B0B3B8' },
{ id: 'games', nome: 'Game', cor: '#39FF14' },
{ id: 'moda', nome: 'Moda', cor: '#FF1F8F' },
{ id: 'casa', nome: 'Casa', cor: '#C1502E' },
{ id: 'beleza', nome: 'Beleza', cor: '#FF8FA3' },
{ id: 'esportes', nome: 'Esporte', cor: '#FF6B00' },
] as const;

export type CategoriaId = typeof CATEGORIAS[number]['id'];

export const TAMANHOS = {
  feed: { largura: 1080, altura: 1080 },
  stories: { largura: 1080, altura: 1920 },
} as const;

export type TamanhoBanner = keyof typeof TAMANHOS;
