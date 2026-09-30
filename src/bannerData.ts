export const CATEGORIAS = [
  "eletronicos",
  "informatica",
  "game",
  "moda",
  "casa",
  "beleza",
  "esportes"
] as const;

export type Categoria = typeof CATEGORIAS[number];
export type FormatoBanner = "1:1" | "4:5";

export interface ProdutoComercial {
  preco_original: number | null;
  preco_promocional: number | null;
  desconto_percentual: number | null;
  parcelamento: string;
}

export interface ProdutoConteudo {
  especificacoes: string[];
  beneficios: string[];
}

export interface BannerData {
  produto: {
    nome: string;
    marca: string;
    categoria: Categoria | "";
    imagem: string;
  };
  comercial: ProdutoComercial;
  conteudo: ProdutoConteudo;
  banner: {
    formato: FormatoBanner;
    cta: string;
  };
  extracao: {
    confianca: number;
    campos_confirmados: string[];
    campos_ausentes: string[];
  };
}
