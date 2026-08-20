import type { BannerData, TamanhoBanner } from './bannerData';
import { skins } from './skins';

interface MasterTemplateProps {
  dados: BannerData;
  tamanho: TamanhoBanner;
}

export function MasterTemplate({ dados, tamanho }: MasterTemplateProps) {
  const skin = skins.padrao;
  const dimensoes = tamanho === 'feed' 
    ? { largura: '100%', aspectRatio: '1/1' }
    : { largura: '320px', aspectRatio: '9/16' };

  return (
    <div style={{
      ...dimensoes,
      backgroundColor: skin.fundo,
      color: skin.texto,
      borderRadius: '16px',
      padding: '24px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between',
      boxSizing: 'border-box',
      overflow: 'hidden',
    }}>
      <div style={{ textAlign: 'center' }}>
        <h3 style={{ margin: 0, fontSize: '18px', fontWeight: 600 }}>
          {dados.produto}
        </h3>
      </div>
      
      <div style={{ textAlign: 'center', margin: '16px 0' }}>
        <img 
          src={dados.imagemProduto} 
          alt={dados.produto}
          style={{ maxWidth: '60%', height: 'auto', borderRadius: '8px' }}
        />
      </div>
      
      <div style={{ textAlign: 'center' }}>
        {dados.precoAntigo && (
          <p style={{ 
            textDecoration: 'line-through', 
            color: '#888', 
            margin: 0, 
            fontSize: '14px' 
          }}>
            {dados.precoAntigo}
          </p>
        )}
        <p style={{ 
          fontSize: '24px', 
          fontWeight: 700, 
          color: skin.destaque, 
          margin: '8px 0' 
        }}>
          {dados.preco}
        </p>
        <button style={{
          backgroundColor: skin.botaoFundo,
          color: skin.botaoTexto,
          border: 'none',
          borderRadius: '8px',
          padding: '12px 24px',
          fontSize: '16px',
          fontWeight: 600,
          cursor: 'pointer',
          width: '100%',
        }}>
          {dados.botaoTexto}
        </button>
      </div>
    </div>
  );
}
