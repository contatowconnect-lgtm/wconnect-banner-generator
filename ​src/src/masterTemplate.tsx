import type { BannerData, TamanhoBanner } from './bannerData';
import { getSkin } from './skins';

interface MasterTemplateProps {
  dados: BannerData;
  tamanho: TamanhoBanner;
}

export function MasterTemplate({ dados, tamanho }: MasterTemplateProps) {
  const skin = getSkin(dados.categoria as any);
  const dimensoes = tamanho === 'feed' 
    ? { largura: 1080, altura: 1080 }
    : { largura: 1080, altura: 1920 };

  return (
    <div style={{
      width: dimensoes.largura,
      height: dimensoes.altura,
      backgroundColor: skin.secundaria,
      position: 'relative',
      overflow: 'hidden',
      fontFamily: 'system-ui, sans-serif',
    }}>
      {/* Bloco 1 — Cabeçalho / Logo */}
      <div style={{
        position: 'absolute',
        top: 40,
        left: 40,
        right: 40,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <span style={{ fontSize: 28, fontWeight: 700, color: skin.texto }}>W Connect</span>
        <span style={{
          padding: '8px 20px',
          backgroundColor: skin.primaria,
          color: '#fff',
          borderRadius: 20,
          fontSize: 18,
        }}>{dados.categoria}</span>
      </div>

      {/* Bloco 2 — Espaçamento topo */}
      <div style={{ height: 120 }} />

      {/* Bloco 3 — Imagem do Produto */}
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '20px 40px',
      }}>
        <img
          src={dados.imagemProduto}
          alt={dados.produto}
          style={{
            maxWidth: '80%',
            maxHeight: 400,
            objectFit: 'contain',
          }}
        />
      </div>

      {/* Bloco 4 — Nome do Produto */}
      <div style={{ padding: '20px 40px 10px' }}>
        <h2 style={{
          fontSize: 36,
          fontWeight: 700,
          color: skin.texto,
          margin: 0,
        }}>{dados.produto}</h2>
      </div>

      {/* Bloco 5 — Descrição */}
      {dados.descricao && (
        <div style={{ padding: '0 40px 10px' }}>
          <p style={{
            fontSize: 22,
            color: '#4B5563',
            margin: 0,
          }}>{dados.descricao}</p>
        </div>
      )}

      {/* Bloco 6 — Preços */}
      <div style={{ padding: '10px 40px' }}>
        {dados.precoAntigo && (
          <p style={{
            fontSize: 22,
            color: '#9CA3AF',
            textDecoration: 'line-through',
            margin: '0 0 5px',
          }}>De: {dados.precoAntigo}</p>
        )}
        <p style={{
          fontSize: 48,
          fontWeight: 800,
          color: skin.primaria,
          margin: 0,
        }}>{dados.preco}</p>
      </div>

      {/* Bloco 7 — Botão de Ação */}
      <div style={{
        position: 'absolute',
        bottom: 60,
        left: 40,
        right: 40,
        display: 'flex',
        justifyContent: 'center',
      }}>
        <button style={{
          padding: '20px 60px',
          backgroundColor: skin.botao,
          color: skin.botaoTexto,
          border: 'none',
          borderRadius: 12,
          fontSize: 24,
          fontWeight: 600,
          cursor: 'pointer',
          width: '100%',
          maxWidth: 500,
        }}>{dados.botaoTexto}</button>
      </div>

      {/* Bloco 8 — Rodapé */}
      <div style={{
        position: 'absolute',
        bottom: 15,
        left: 0,
        right: 0,
        textAlign: 'center',
        fontSize: 14,
        color: '#9CA3AF',
      }}>
        W Connect — Produtos Selecionados
      </div>
    </div>
  );
}
