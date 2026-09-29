export function getSkin(categoria: string) {
  console.log("📥 Categoria bruta:", JSON.stringify(categoria)); // ← adiciona
  const chave = categoria
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();
  console.log("🔑 Chave buscada:", chave); // ← e essa
  
  return skins[chave] || skins.eletronicos;
}
