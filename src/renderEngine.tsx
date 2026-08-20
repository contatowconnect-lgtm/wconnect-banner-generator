import type { BannerData, TamanhoBanner } from './bannerData';
import { MasterTemplate } from './masterTemplate';

interface RenderEngineProps {
  dados: BannerData;
  tamanho: TamanhoBanner;
}

export function RenderEngine({ dados, tamanho }: RenderEngineProps) {
  return (
    <div className="render-engine">
      <MasterTemplate dados={dados} tamanho={tamanho} />
    </div>
  );
}

export async function gerarBannerComoImagem(
  dados: BannerData,
  tamanho: TamanhoBanner
): Promise<Blob | null> {
  console.log('Gerando banner:', dados.produto, 'no tamanho:', tamanho);
  return null;
}

