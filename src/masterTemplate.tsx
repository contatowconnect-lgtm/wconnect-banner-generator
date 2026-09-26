import React from 'react';
import type { BannerData } from './bannerData';

interface Props {
  produto: BannerData;
  tamanho?: string;
}

export const MasterTemplate: React.FC<Props> = ({ produto, tamanho = "feed" }) => {
  if (!produto) {
    return <div>Carregando...</div>;
  }

  const {
    produto: nomeProduto,
    preco,
    precoAntigo,
    categoria,
    imagemProduto,
    descricao,
    botaoTexto,
    link,
    beneficios = []
  } = produto;

  return (
    <div style={{
      background: '#0A0B10',
      color: '#F2F4F8',
      borderRadius: '16px',
      padding: '32px',
      maxWidth: '500px',
      margin: '0 auto',
      fontFamily: "'Inter', sans-serif"
    }}>
      {/* Categoria */}
      <span style={{
        display: 'inline-block',
        background: '#2E6BFF',
        color: '#FFFFFF',
        padding: '6px 14px',
        borderRadius: '20px',
        fontSize: '13px',
        fontWeight: 600,
        marginBottom: '20px',
        textTransform: 'uppercase',
        letterSpacing: '0.5px'
      }}>
        {categoria}
      </span>

      {/* Nome do Produto */}
      <h3 style={{
        fontFamily: "'Space Grotesk', sans-serif",
        fontSize: '26px',
        fontWeight: 700,
        margin: '0 0 10px 0',
        color: '#FFFFFF'
      }}>
        {nomeProduto}
      </h3>

      {/* Descrição */}
      <p style={{
        color: '#8991A6',
        fontSize: '15px',
        margin: '0 0 20px 0',
        lineHeight: '1.5'
      }}>
        {descricao}
      </p>

      {/* Imagem do Produto */}
      <img
        src={imagemProduto}
        alt={nomeProduto}
        style={{
          width: '100%',
          height: '200px',
          objectFit: 'cover',
          borderRadius: '12px',
          marginBottom: '24px'
        }}
      />

      {/* Preços */}
      <div style={{ marginBottom: '20px' }}>
        <div style={{
          fontSize: '32px',
          fontWeight: 700,
          color: '#FFFFFF',
          fontFamily: "'Space Grotesk', sans-serif"
        }}>
          {preco}
        </div>
        {precoAntigo && (
          <div style={{
            color: '#6B7280',
            textDecoration: 'line-through',
            fontSize: '15px',
            marginTop: '4px'
          }}>
            De {precoAntigo}
          </div>
        )}
      </div>

      {/* Benefícios */}
      {beneficios.length > 0 && (
        <ul style={{
          padding: '0 0 0 20px',
          margin: '0 0 24px 0'
        }}>
          {beneficios.map((b, i) => (
            <li key={i} style={{
              color: '#D1D5DB',
              marginBottom: '6px',
              fontSize: '14px'
            }}>
              {b}
            </li>
          ))}
        </ul>
      )}

      {/* Botão */}
      <a
        href={link}
        style={{
          display: 'block',
          textAlign: 'center',
          padding: '14px 24px',
          background: 'linear-gradient(90deg, #2E6BFF, #7B3FE4)',
          color: '#FFFFFF',
          borderRadius: '10px',
          textDecoration: 'none',
          fontWeight: 600,
          fontSize: '16px',
          fontFamily: "'Space Grotesk', sans-serif"
        }}
      >
        {botaoTexto}
      </a>
    </div>
  );
};
