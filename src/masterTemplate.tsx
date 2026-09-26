import React from 'react';
import type { BannerData } from './bannerData';

interface Props {
  produto: BannerData;
  tamanho?: string;
}

export const MasterTemplate: React.FC<Props> = ({ produto, tamanho = "feed" }) => {
  if (!produto) return <div>Carregando...</div>;

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
      <span style={{
        display: 'inline-block',
        background: '#2E6BFF',
        color: '#FFF',
        padding: '6px 14px',
        borderRadius: '20px',
        fontSize: '13px',
        fontWeight: 600,
        marginBottom: '20px',
        textTransform: 'uppercase'
      }}>
        {categoria}
      </span>

      <h3 style={{
        fontFamily: "'Space Grotesk', sans-serif",
        fontSize: '26px',
        fontWeight: 700,
        margin: '0 0 10px 0'
      }}>
        {nomeProduto}
      </h3>

      <p style={{ color: '#8991A6', margin: '0 0 20px 0' }}>
        {descricao}
      </p>

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

      <div style={{ marginBottom: '20px' }}>
        <div style={{
          fontSize: '32px',
          fontWeight: 700,
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

      {beneficios.length > 0 && (
        <ul style={{ padding: '0 0 0 20px', margin: '0 0 24px 0' }}>
          {beneficios.map((b, i) => (
            <li key={i} style={{ color: '#D1D5DB', marginBottom: '6px', listStyle: 'none', paddingLeft: '0' }}>
              {b}
            </li>
          ))}
        </ul>
      )}

      <a
        href={link}
        style={{
          display: 'block',
          textAlign: 'center',
          padding: '14px',
          background: 'linear-gradient(90deg, #2E6BFF, #7B3FE4)',
          color: '#FFF',
          borderRadius: '10px',
          textDecoration: 'none',
          fontWeight: 600,
          fontFamily: "'Space Grotesk', sans-serif"
        }}
      >
        {botaoTexto}
      </a>
    </div>
  );
};
