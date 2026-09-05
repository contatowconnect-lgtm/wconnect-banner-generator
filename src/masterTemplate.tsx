import type { BannerData, TamanhoBanner } from './bannerData';
import { skins } from './skins';

interface MasterTemplateProps {
  dados: BannerData;
  tamanho: TamanhoBanner;
}

export function MasterTemplate({ dados, tamanho }: MasterTemplateProps) {
  const skin = skins.padrao;

  const dimensoes =
    tamanho === 'feed'
      ? { largura: '1080px', aspectRatio: '1/1' }
      : { largura: '1080px', aspectRatio: '4/5' };

  // Encontra a cor da categoria
  const categoriaInfo = dados.categoria;
  const corCategoria = skin.destaque;

  return (
    <div
      style={{
        ...dimensoes,
        backgroundColor: skin.fundo,
        color: skin.texto,
        borderRadius: '16px',
        padding: '40px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        boxSizing: 'border-box',
        overflow: 'hidden',
        position: 'relative',
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* ===== REGIÃO 1: Tag de Categoria (Superior Esquerdo) ===== */}
      <div
        style={{
          position: 'absolute',
          top: '40px',
          left: '40px',
          backgroundColor: skin.destaque,
          color: '#FFFFFF',
          padding: '8px 20px',
          borderRadius: '8px',
          fontSize: '18px',
          fontWeight: 600,
          textTransform: 'uppercase',
          letterSpacing: '1px',
        }}
      >
        {dados.categoria}
      </div>

      {/* ===== REGIÃO 2: Logo + WAYNNE AI (Topo Central) ===== */}
      <div
        style={{
          textAlign: 'center',
          marginTop: '10px',
          marginBottom: '20px',
        }}
      >
        <div
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '12px',
          }}
        >
          {/* Logo placeholder — substituir pela imagem SVG/png */}
          <div
            style={{
              width: '60px',
              height: '60px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #2E6BFF 0%, #7B3FE4 50%, #00D9FF 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              fontWeight: 'bold',
              color: '#FFFFFF',
            }}
          >
            W
          </div>
          <h1
            style={{
              margin: 0,
              fontSize: '32px',
              fontWeight: 700,
              fontFamily: "'Space Grotesk', sans-serif",
            }}
          >
            <span style={{ color: '#F2F4F8' }}>WAYNNE</span>{' '}
            <span
              style={{
                background: 'linear-gradient(90deg, #2E6BFF, #00D9FF)',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                backgroundClip: 'text',
              }}
            >
              AI
            </span>
          </h1>
        </div>
      </div>

      {/* ===== REGIÃO 3: Selo de Confiança (Superior Direito) ===== */}
      <div
        style={{
          position: 'absolute',
          top: '40px',
          right: '40px',
          width: '100px',
          height: '100px',
          borderRadius: '50%',
          border: '4px solid #FFC300',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          backgroundColor: 'rgba(10, 11, 16, 0.8)',
          color: '#FFC300',
          fontSize: '10px',
          textAlign: 'center',
          padding: '8px',
          lineHeight: 1.2,
        }}
      >
        <div style={{ fontSize: '24px', marginBottom: '2px' }}>✓</div>
        <div>Produto</div>
        <div>Selecionado</div>
      </div>

      {/* ===== REGIÃO 4: Título do Produto ===== */}
      <h2
        style={{
          margin: '0 0 10px 0',
          fontSize: '36px',
          fontWeight: 700,
          textAlign: 'center',
          fontFamily: "'Space Grotesk', sans-serif",
          lineHeight: 1.2,
        }}
      >
        {dados.produto}
      </h2>

      {/* ===== REGIÃO 5: Imagem do Produto ===== */}
      {dados.imagemProduto && (
        <div
          style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            margin: '20px 0',
            position: 'relative',
          }}
        >
          <img
            src={dados.imagemProduto}
            alt={dados.produto}
            style={{
              maxWidth: '60%',
              height: 'auto',
              borderRadius: '12px',
              objectFit: 'contain',
            }}
          />
        </div>
      )}

      {/* ===== REGIÃO 6: Cards de Benefício — 8 itens ===== */}
      {dados.beneficios && dados.beneficios.length > 0 && (
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: '1fr 1fr',
            gap: '12px 20px',
            margin: '20px 0',
          }}
        >
          {dados.beneficios.slice(0, 8).map((beneficio, index) => (
            <div
              key={index}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '10px',
                backgroundColor: skin.panel,
                padding: '12px 16px',
                borderRadius: '8px',
              }}
            >
              <div
                style={{
                  width: '24px',
                  height: '24px',
                  borderRadius: '50%',
                  backgroundColor: skin.destaque,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: '#FFFFFF',
                  fontSize: '14px',
                  flexShrink: 0,
                }}
              >
                ✓
              </div>
              <span
                style={{
                  fontSize: '14px',
                  lineHeight: 1.3,
                  color: skin.texto,
                }}
              >
                {beneficio}
              </span>
            </div>
          ))}
        </div>
      )}

      {/* ===== REGIÃO 7: Preço ===== */}
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          margin: '20px 0',
        }}
      >
        {dados.precoAntigo && (
          <p
            style={{
              textDecoration: 'line-through',
              color: '#888888',
              margin: '0 0 8px 0',
              fontSize: '18px',
            }}
          >
            {dados.precoAntigo}
          </p>
        )}
        <p
          style={{
            fontSize: '42px',
            fontWeight: 700,
            color: skin.destaque,
            margin: 0,
            fontFamily: "'Space Grotesk', sans-serif",
          }}
        >
          {dados.preco}
        </p>
      </div>

      {/* ===== REGIÃO 8: Botão CTA ===== */}
      <button
        style={{
          backgroundColor: skin.botaoFundo,
          color: skin.botaoTexto,
          border: 'none',
          borderRadius: '8px',
          padding: '16px 32px',
          fontSize: '20px',
          fontWeight: 600,
          cursor: 'pointer',
          width: '100%',
          fontFamily: "'Inter', sans-serif",
          transition: 'transform 0.2s ease',
        }}
        onMouseOver={(e) => {
          e.currentTarget.style.transform = 'scale(1.02)';
        }}
        onMouseOut={(e) => {
          e.currentTarget.style.transform = 'scale(1)';
        }}
      >
        🛒 {dados.botaoTexto || 'VER OFERTA'}
      </button>

      {/* ===== REGIÃO 9: Ícones de Confiança ===== */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-around',
          marginTop: '24px',
          padding: '0 20px',
          fontSize: '12px',
          color: '#8991A6',
          flexWrap: 'wrap',
          gap: '10px',
        }}
      >
        <span>🚚 Envio Rápido</span>
        <span>✓ Compra Segura</span>
        <span>🛡️ Garantia</span>
        <span>🎧 Suporte</span>
      </div>

      {/* ===== REGIÃO 10: Rodapé ===== */}
      <div
        style={{
          textAlign: 'center',
          marginTop: '20px',
          paddingTop: '15px',
          borderTop: '1px solid #171A24',
          fontSize: '14px',
          color: '#8991A6',
        }}
      >
        <span style={{ fontWeight: 600, color: '#F2F4F8' }}>WAYNNE AI</span> — Tecnologia que te acompanha
      </div>
    </div>
  );
}
