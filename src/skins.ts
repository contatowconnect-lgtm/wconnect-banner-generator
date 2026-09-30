import designSystem from "../config/design_system.json";

type SkinConfig = {
  cor: string;
  nomeExibicao: string;
};

const skins: Record<string, SkinConfig> = Object.fromEntries(
  Object.entries(designSystem.categories).map(([key, value]) => [
    key,
    { cor: value.color, nomeExibicao: value.label }
  ])
);

export function getSkin(categoria: string): SkinConfig | null {
  const chave = (categoria || "")
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .trim();

  return skins[chave] ?? null;
}
