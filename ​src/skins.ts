import { CategoriaId, CATEGORIAS } from './bannerData';

export const SKINS: Record<CategoriaId, {
  primaria: string;
  secundaria: string;
  texto: string;
  botao: string;
  botaoTexto: string;
}> = {
  eletronicos: {
    primaria: '#2563EB',
    secundaria: '#EFF6FF',
    texto: '#1E40AF',
    botao: '#2563EB',
    botaoTexto: '#FFFFFF',
  },
  moda: {
    primaria: '#DC2626',
    secundaria: '#FEF2F2',
    texto: '#B91C1C',
    botao: '#DC2626',
    botaoTexto: '#FFFFFF',
  },
  casa: {
    primaria: '#059669',
    secundaria: '#ECFDF5',
    texto: '#047857',
    botao: '#059669',
    botaoTexto: '#FFFFFF',
  },
  beleza: {
    primaria: '#D97706',
    secundaria: '#FFFBEB',
    texto: '#B45309',
    botao: '#D97706',
    botaoTexto: '#FFFFFF',
  },
  esportes: {
    primaria: '#7C3AED',
    secundaria: '#F5F3FF',
    texto: '#6D28D9',
    botao: '#7C3AED',
    botaoTexto: '#FFFFFF',
  },
};

export function getSkin(categoriaId: CategoriaId) {
  return SKINS[categoriaId] || SKINS.eletronicos;
}
