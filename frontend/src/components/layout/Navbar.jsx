import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Sparkles,
  ChevronDown,
  Bell,
  User,
  LogOut,
  Flame,
  Zap,
  Code2,
  Layers,
  ShieldCheck,
  Menu,
} from 'lucide-react';

export const Navbar = () => {
  const {
    careers,
    currentCareer,
    selectCareer,
    user,
    unreadCount,
    setIsNotificationDrawerOpen,
    setIsAuthModalOpen,
    logout,
    setActiveTab,
    setSidebarOpen,
  } = useApp();

  const [careerMenuOpen, setCareerMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);

  return (
    <header
      className="app-navbar"
      style={{
        height: '68px',
        padding: '0 24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'rgba(4, 6, 10, 0.88)',
        backdropFilter: 'blur(16px)',
        borderBottom: '1px solid var(--border-subtle)',
        position: 'sticky',
        top: 0,
        zIndex: 50,
      }}
    >
      {/* Left: Brand & Career Dropdown */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        {/* Mobile hamburger */}
        <button
          className="app-hamburger"
          aria-label="Open navigation menu"
          onClick={() => setSidebarOpen(true)}
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '8px',
            borderRadius: '10px',
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-primary)',
            cursor: 'pointer',
          }}
        >
          <Menu className="w-5 h-5" />
        </button>

        {/* Brand */}
        <div
          onClick={() => setActiveTab('dashboard')}
          style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}
        >
          <div
            style={{
              width: '38px',
              height: '38px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #059669 0%, #22d3ee 100%)',
              border: '1px solid rgba(52, 211, 153, 0.25)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: '0 0 20px rgba(52, 211, 153, 0.35)',
            }}
          >
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <div>
            <div style={{ fontSize: '1.2rem', fontWeight: 800, letterSpacing: '-0.03em', lineHeight: 1.1 }}>
              CareerPath <span className="gradient-text-cyan">AI</span>
            </div>
            <div className="nav-brand-sub" style={{ fontSize: '0.68rem', color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.04em' }}>
              TECH SKILL DAG ENGINE
            </div>
          </div>
        </div>

        {/* Divider */}
        <div style={{ width: '1px', height: '24px', background: 'var(--border-subtle)' }} />

        {/* Career Selector Dropdown */}
        <div className="nav-career-selector" style={{ position: 'relative' }}>
          <button
            onClick={() => setCareerMenuOpen(!careerMenuOpen)}
            style={{
              padding: '7px 14px',
              borderRadius: '10px',
              background: 'rgba(255, 255, 255, 0.04)',
              border: '1px solid rgba(52, 211, 153, 0.3)',
              color: 'var(--text-primary)',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.15s ease',
            }}
            className="hover:border-cyan-400/60"
          >
            <Layers className="w-4 h-4 text-emerald-400" />
            <span>{currentCareer?.title || 'Select Career Path'}</span>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {careerMenuOpen && (
            <div
              className="glass-panel-elevated"
              style={{
                position: 'absolute',
                top: '42px',
                left: 0,
                width: '260px',
                padding: '8px',
                zIndex: 100,
                display: 'flex',
                flexDirection: 'column',
                gap: '4px',
                background: 'rgba(6, 8, 14, 0.98)',
              }}
            >
              <div style={{ padding: '6px 10px', fontSize: '0.72rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>
                Active Specialization Tracks
              </div>
              {careers.map((c) => (
                <button
                  key={c.id}
                  onClick={() => {
                    selectCareer(c);
                    setCareerMenuOpen(false);
                  }}
                  style={{
                    padding: '8px 12px',
                    borderRadius: '8px',
                    border: 'none',
                    background: currentCareer?.id === c.id ? 'rgba(52, 211, 153, 0.15)' : 'transparent',
                    color: currentCareer?.id === c.id ? '#34d399' : 'var(--text-primary)',
                    fontSize: '0.84rem',
                    fontWeight: 600,
                    textAlign: 'left',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                  className="hover:bg-slate-800/60"
                >
                  <span>{c.title}</span>
                  {currentCareer?.id === c.id && <span style={{ fontSize: '0.75rem', color: '#34d399' }}>✓</span>}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Right Toolbar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
        {/* Streak & XP Badges */}
        <div className="nav-stats" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div
            style={{
              padding: '6px 12px',
              borderRadius: '999px',
              background: 'rgba(244, 63, 94, 0.12)',
              border: '1px solid rgba(244, 63, 94, 0.3)',
              color: '#fb7185',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
            }}
          >
            <Flame className="w-4 h-4" /> 7d Streak
          </div>

          <div
            style={{
              padding: '6px 12px',
              borderRadius: '999px',
              background: 'linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(34, 211, 238, 0.15))',
              border: '1px solid rgba(52, 211, 153, 0.3)',
              color: '#34d399',
              fontSize: '0.82rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '5px',
            }}
          >
            <Zap className="w-4 h-4 text-amber-400" /> {user?.xp || 650} XP
          </div>
        </div>

        {/* API Docs Link */}
        <a
          href="/docs"
          target="_blank"
          rel="noopener noreferrer"
          title="Open FastAPI Swagger Documentation"
          style={{
            padding: '7px 12px',
            borderRadius: '10px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-secondary)',
            fontSize: '0.8rem',
            fontWeight: 600,
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
          }}
          className="nav-api-link hover:border-slate-500 hover:text-white"
        >
          <Code2 className="w-3.5 h-3.5 text-cyan-400" />
          <span>Swagger API</span>
        </a>

        {/* Notification Bell */}
        <button
          onClick={() => setIsNotificationDrawerOpen(true)}
          style={{
            position: 'relative',
            padding: '8px',
            borderRadius: '10px',
            background: 'rgba(255, 255, 255, 0.04)',
            border: '1px solid var(--border-subtle)',
            color: 'var(--text-secondary)',
            cursor: 'pointer',
            display: 'flex',
          }}
        >
          <Bell className="w-4 h-4" />
          {unreadCount > 0 && (
            <span
              style={{
                position: 'absolute',
                top: '-3px',
                right: '-3px',
                width: '14px',
                height: '14px',
                borderRadius: '50%',
                background: '#f43f5e',
                color: '#fff',
                fontSize: '0.62rem',
                fontWeight: 800,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              {unreadCount}
            </span>
          )}
        </button>

        {/* User Profile / Auth Action */}
        {user ? (
          <div style={{ position: 'relative' }}>
            <button
              onClick={() => setUserMenuOpen(!userMenuOpen)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '5px 12px 5px 6px',
                borderRadius: '999px',
                background: 'rgba(255, 255, 255, 0.06)',
                border: '1px solid var(--border-subtle)',
                color: 'var(--text-primary)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              <div
                style={{
                  width: '28px',
                  height: '28px',
                  borderRadius: '50%',
                  background: 'linear-gradient(135deg, #059669, #22d3ee)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.8rem',
                  fontWeight: 800,
                  color: '#fff',
                }}
              >
                {(user.full_name || user.username || 'U').charAt(0).toUpperCase()}
              </div>
              <span className="nav-username">{user.full_name || user.username}</span>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {userMenuOpen && (
              <div
                className="glass-panel-elevated"
                style={{
                  position: 'absolute',
                  top: '42px',
                  right: 0,
                  width: '200px',
                  padding: '8px',
                  zIndex: 100,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '4px',
                  background: 'rgba(6, 8, 14, 0.98)',
                }}
              >
                <div style={{ padding: '6px 10px', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Signed in as <strong>{user.email}</strong>
                </div>
                <button
                  onClick={() => {
                    setActiveTab('resume');
                    setUserMenuOpen(false);
                  }}
                  style={{
                    padding: '8px 10px',
                    borderRadius: '8px',
                    border: 'none',
                    background: 'transparent',
                    color: 'var(--text-primary)',
                    fontSize: '0.84rem',
                    textAlign: 'left',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                  className="hover:bg-slate-800/60"
                >
                  <User className="w-4 h-4 text-cyan-400" /> Profile & Resume
                </button>
                <button
                  onClick={() => {
                    logout();
                    setUserMenuOpen(false);
                  }}
                  style={{
                    padding: '8px 10px',
                    borderRadius: '8px',
                    border: 'none',
                    background: 'transparent',
                    color: '#fb7185',
                    fontSize: '0.84rem',
                    textAlign: 'left',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                  }}
                  className="hover:bg-rose-950/40"
                >
                  <LogOut className="w-4 h-4" /> Sign Out
                </button>
              </div>
            )}
          </div>
        ) : (
          <button
            onClick={() => setIsAuthModalOpen(true)}
            className="btn-primary"
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <ShieldCheck className="w-4 h-4" /> Sign In / Demo
          </button>
        )}
      </div>
    </header>
  );
};
