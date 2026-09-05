export const skins = {
  padrao: {
    fundo: '#0A0B10',
    texto: '#F2F4F8',
    destaque: '#2E6BFF',
    botaoFundo: '#7B3FE4',
    botaoTexto: '#F2F4F8',
  },
  escuro: {
    fundo: '#0A0B10',
    texto: '#F2F4F8',
    destaque: '#00D9FF',
    botaoFundo: '#2E6BFF',
    botaoTexto: '#F2F4F8',
  },
  promocao: {
    fundo: '#0A0B10',
    texto: '#F2F4F8',
    destaque: '#FFC300',
    botaoFundo: '#7B3FE4',
    botaoTexto: '#F2F4F8',
  },
} as const;

export type SkinId = keyof typeof skins;
