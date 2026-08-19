import type { BannerData, TamanhoBanner } from './bannerData';
import { MasterTemplate } from './masterTemplate';

interface RenderEngineProps {
  dados: BannerData;
  tamanho: TamanhoBanner;
}

export function RenderEngine({ dados, tamanho }: RenderEngineProps) {
  // Aqui é onde tudo se junta: validação + escolha de template + renderização
  // Futuramente: adicionar validação de dados, cache, etc.
  
  return (
    <div className="render-engine">
      <MasterTemplate dados={dados} tamanho={tamanho} />
    </div>
  );
}

// Função auxiliar pra renderizar e gerar imagem (futuro)
export async function gerarBannerComoImagem(
  dados: BannerData,
  tamanho: TamanhoBanner
): Promise<Blob | null> {
  // Implementação futura: usar html2canvas ou similar
  console.log('Gerando banner:', dados.produto, 'no tamanho:', tamanho);
  return null;
}
