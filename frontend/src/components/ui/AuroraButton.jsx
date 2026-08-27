import React from 'react';
import BorderGlow from '../effects/BorderGlow';

export const AuroraButton = ({
  children,
  onClick,
  disabled,
  type = 'button',
  className = '',
  style = {},
  variant = 'primary',
}) => {
  const colorMap = {
    primary: {
      bg: 'linear-gradient(135deg, #059669 0%, #0891b2 100%)',
      glow: '160 80 60',
      colors: ['#34d399', '#22d3ee', '#a78bfa'],
      text: '#ffffff',
    },
    emerald: {
      bg: 'linear-gradient(135deg, #34d399 0%, #22d3ee 100%)',
      glow: '160 80 65',
      colors: ['#34d399', '#22d3ee', '#a78bfa'],
      text: '#ffffff',
    },
    secondary: {
      bg: 'rgba(52, 211, 153, 0.04)',
      glow: '160 80 60',
      colors: ['#34d399', '#22d3ee', '#a78bfa'],
      text: 'var(--text-primary)',
    },
    amber: {
      bg: 'linear-gradient(135deg, #f59e0b 0%, #f97316 100%)',
      glow: '40 90 60',
      colors: ['#fbbf24', '#f59e0b', '#f97316'],
      text: '#ffffff',
    },
  };

  const v = colorMap[variant] || colorMap.primary;

  return (
    <BorderGlow
      edgeSensitivity={25}
      glowColor={v.glow}
      backgroundColor="transparent"
      borderRadius={14}
      glowRadius={20}
      glowIntensity={0.8}
      coneSpread={30}
      colors={v.colors}
      fillOpacity={0.3}
      as="button"
      className={className}
      style={{
        padding: '11px 22px',
        fontWeight: 600,
        fontSize: '0.92rem',
        color: v.text,
        background: v.bg,
        border: '1px solid rgba(52, 211, 153, 0.2)',
        boxShadow: '0 4px 20px rgba(5, 150, 105, 0.35), inset 0 1px 0 rgba(255, 255, 255, 0.15)',
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.6 : 1,
        transition: 'all 0.25s cubic-bezier(0.16, 1, 0.3, 1)',
        width: '100%',
        ...style,
      }}
      onClick={disabled ? undefined : onClick}
      {...(type === 'submit' ? { type: 'submit' } : {})}
    >
      {children}
    </BorderGlow>
  );
};

export default AuroraButton;
