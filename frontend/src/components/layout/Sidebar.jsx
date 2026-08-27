import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  LayoutDashboard,
  Layers,
  Compass,
  Briefcase,
  Sparkles,
  FileText,
  Clock,
  BookOpen,
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Command Center', icon: LayoutDashboard, badge: 'Live' },
  { id: 'roadmap', label: 'Skill DAG Roadmap', icon: Layers, badge: 'Interactive' },
  { id: 'careers', label: 'Career Explorer', icon: Compass },
  { id: 'jobs', label: 'Job Gap Analyzer', icon: Briefcase, badge: 'AI' },
  { id: 'interviews', label: 'Interview Arena', icon: Sparkles, badge: '64 Qs' },
  { id: 'resume', label: 'ATS Resume Matcher', icon: FileText },
  { id: 'study', label: 'Pomodoro Focus Hub', icon: Clock },
  { id: 'resources', label: 'Curated Resources', icon: BookOpen },
];

export const Sidebar = () => {
  const { activeTab, setActiveTab, sidebarOpen, setSidebarOpen } = useApp();

  return (
    <aside
      className={`app-sidebar${sidebarOpen ? ' is-open' : ''}`}
      style={{
        width: '260px',
        background: 'rgba(4, 6, 10, 0.78)',
        backdropFilter: 'blur(16px)',
        borderRight: '1px solid var(--border-subtle)',
        padding: '20px 14px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        height: 'calc(100vh - 68px)',
        position: 'sticky',
        top: '68px',
      }}
    >
      {/* Navigation Items */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        <div style={{ padding: '4px 12px 8px 12px', fontSize: '0.72rem', fontWeight: 700, textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.04em' }}>
          NAVIGATION MODULES
        </div>

        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => {
                setActiveTab(item.id);
                setSidebarOpen(false);
              }}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '11px 14px',
                borderRadius: '12px',
                border: 'none',
                background: isActive ? 'linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(34, 211, 238, 0.15))' : 'transparent',
                borderLeft: isActive ? '3px solid #34d399' : '3px solid transparent',
                color: isActive ? '#34d399' : 'var(--text-secondary)',
                fontSize: '0.88rem',
                fontWeight: isActive ? 700 : 500,
                cursor: 'pointer',
                transition: 'all 0.18s ease',
                textAlign: 'left',
              }}
              className="hover:bg-emerald-950/30 hover:text-white"
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <Icon className={`w-4 h-4 ${isActive ? 'text-emerald-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </div>

              {item.badge && (
                <span
                  style={{
                    fontSize: '0.68rem',
                    fontWeight: 700,
                    padding: '2px 7px',
                    borderRadius: '6px',
                    background: isActive ? 'rgba(52, 211, 153, 0.25)' : 'rgba(255, 255, 255, 0.06)',
                    color: isActive ? '#34d399' : 'var(--text-muted)',
                  }}
                >
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* Bottom Mini Card */}
      <div
        style={{
          padding: '14px',
          borderRadius: '14px',
          background: 'linear-gradient(135deg, rgba(52, 211, 153, 0.08), rgba(34, 211, 238, 0.08))',
          border: '1px solid rgba(52, 211, 153, 0.2)',
          display: 'flex',
          flexDirection: 'column',
          gap: '6px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', fontWeight: 700, color: '#34d399' }}>
          <Sparkles className="w-3.5 h-3.5" /> DAG Engine v1.0
        </div>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
          Continuous topological skill sorting & gap analysis powered by FastAPI.
        </p>
      </div>
    </aside>
  );
};
