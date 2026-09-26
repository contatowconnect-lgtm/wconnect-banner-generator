type SkinConfig = {
  [key: string]: {
    cor: string;
    nomeExibicao: string;
  };
};

// Tudo minúsculo = igual ao formulário → combina direto!
const skins: SkinConfig = {
  eletronicos: { cor: "#C6FF00", nomeExibicao: "ELETRÔNICOS" },
  moda:        { cor: "#FF1FBF", nomeExibicao: "MODA" },
  casa:        { cor: "#FF9100", nomeExibicao: "CASA" },
  beleza:      { cor: "#FF80AB", nomeExibicao: "BELEZA" },
  game:        { cor: "#39FF14", nomeExibicao: "GAME" },
  esportes:    { cor: "#FFC107", nomeExibicao: "ESPORTES" }
};

export function getSkin(categoria: string) {
  // Converte pra minúsculo e remove acentos → não tem erro de digitação!
  const chave = categoria
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
  
  return skins[chave] || skins.eletronicos; // Padrão = eletrônicos
}
