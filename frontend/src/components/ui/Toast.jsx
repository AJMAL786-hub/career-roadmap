import React from 'react';
import { useApp } from '../../context/AppContext';
import { CheckCircle, AlertTriangle, Info, X } from 'lucide-react';

export const Toast = () => {
  const { toastMessage } = useApp();

  if (!toastMessage) return null;

  const icons = {
    success: <CheckCircle className="w-5 h-5 text-emerald-400" />,
    error: <AlertTriangle className="w-5 h-5 text-rose-400" />,
    info: <Info className="w-5 h-5 text-cyan-400" />,
  };

  const borderStyles = {
    success: 'border-emerald-500/40 bg-emerald-950/80 text-emerald-100',
    error: 'border-rose-500/40 bg-rose-950/80 text-rose-100',
    info: 'border-cyan-500/40 bg-slate-900/90 text-cyan-100',
  };

  return (
    <div
      style={{
        position: 'fixed',
        bottom: '24px',
        right: '24px',
        zIndex: 9999,
        animation: 'slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1)',
      }}
      className={`flex items-center gap-3 px-4 py-3 rounded-xl border backdrop-blur-xl shadow-2xl ${
        borderStyles[toastMessage.type] || borderStyles.info
      }`}
    >
      {icons[toastMessage.type] || icons.info}
      <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>{toastMessage.message}</span>
    </div>
  );
};
