type SkinConfig = {
  [key: string]: {
    cor: string;
    nomeExibicao: string;
  };
};

// ✅ LISTA DAS CATEGORIAS — ESTAVA FALTANDO!
const skins: SkinConfig = {
  eletronicos: { cor: "#C6FF00", nomeExibicao: "ELETRÔNICOS" },
  moda:        { cor: "#FF1FBF", nomeExibicao: "MODA" },
  casa:        { cor: "#FF9100", nomeExibicao: "CASA" },
  beleza:      { cor: "#FF80AB", nomeExibicao: "BELEZA" },
  game:        { cor: "#39FF14", nomeExibicao: "GAME" },
  esportes:    { cor: "#FFC107", nomeExibicao: "ESPORTES" }
};

export function getSkin(categoria: string) {
  console.log("📥 Categoria bruta:", JSON.stringify(categoria));
  const chave = categoria
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();
  console.log("🔑 Chave buscada:", chave);
  console.log("✅ Encontrada:", skins[chave] ? "SIM" : "NÃO");
  
  return skins[chave] || skins.eletronicos;
}
