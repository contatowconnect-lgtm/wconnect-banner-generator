import React from 'react';
import type { SkinId } from './skins';

interface Produto {
  produto: string;
  preco: string;
  precoAntigo?: string;
  categoria: string;
  imagemProduto: string;
  descricao: string;
  botaoTexto: string;
  link: string;
  beneficios?: string[];
}

interface Props {
  produto: Produto;
  skin?: SkinId;
}

export const MasterTemplate: React.FC<Props> = ({ produto, skin = 'padrao' }) => {
  // Garante que produto existe antes de usar
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
      padding: '40px',
      borderRadius: '16px',
      background: '#0A0B10',
      color: '#F2F4F8',
      maxWidth: '600px',
      margin: '0 auto'
    }}>
      <span style={{
        background: '#2E6BFF',
        padding: '6px 12px',
        borderRadius: '20px',
        fontSize: '14px',
        display: 'inline-block',
        marginBottom: '16px'
      }}>
        {categoria}
      </span>

      <h2 style={{ margin: '0 0 12px 0', fontSize: '28px' }}>
        {nomeProduto}
      </h2>

      <p style={{ color: '#8991A6', marginBottom: '20px' }}>
        {descricao}
      </p>

      <div style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '8px' }}>
        {preco}
      </div>

      {precoAntigo && (
        <div style={{ color: '#8991A6', textDecoration: 'line-through', marginBottom: '20px' }}>
          {precoAntigo}
        </div>
      )}

      <img 
        src={imagemProduto} 
        alt={nomeProduto}
        style={{ width: '100%', height: 'auto', borderRadius: '8px', marginBottom: '24px' }}
      />

      {beneficios.length > 0 && (
        <ul style={{ paddingLeft: '20px', marginBottom: '24px' }}>
          {beneficios.map((b, i) => (
            <li key={i} style={{ marginBottom: '4px' }}>{b}</li>
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
          color: 'white',
          borderRadius: '8px',
          textDecoration: 'none',
          fontWeight: 'bold'
        }}
      >
        {botaoTexto}
      </a>
    </div>
  );
};
