export const skins = {
  padrao: {
    fundo: '#ffffff',
    texto: '#1f2937',
    destaque: '#2563eb',
    botaoFundo: '#2563eb',
    botaoTexto: '#ffffff',
  },
  escuro: {
    fundo: '#1f2937',
    texto: '#ffffff',
    destaque: '#f59e0b',
    botaoFundo: '#f59e0b',
    botaoTexto: '#1f2937',
  },
  promocao: {
    fundo: '#dc2626',
    texto: '#ffffff',
    destaque: '#fef08a',
    botaoFundo: '#ffffff',
    botaoTexto: '#dc2626',
  },
} as const;

export type SkinId = keyof typeof skins;

