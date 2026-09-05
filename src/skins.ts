export const skins = {
  padrao: {
  fundo: '#0A0B10',
  texto: '#F2F4F8',
  destaque: '#2E6BFF',
  panel: '#12141C',
  botaoFundo: '#7B3FE4',
  botaoTexto: '#FFFFFF',
}

  escuro: {
  fundo: '#0A0B10',
  texto: '#F2F4F8',
  destaque: '#00D9FF',
  panel: '#12141C',
  botaoFundo: '#7B3FE4',
  botaoTexto: '#FFFFFF',
}

  promocao: {
  fundo: '#0A0B10',
  texto: '#F2F4F8',
  destaque: '#FFC300',
  panel: '#1A1720',
  botaoFundo: '#2E6BFF',
  botaoTexto: '#FFFFFF',
}

} as const;

export type SkinId = keyof typeof skins;
