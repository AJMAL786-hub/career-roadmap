import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { Sparkles, Mail, Lock, User, ArrowRight } from 'lucide-react';
import FloatingLines from '../effects/FloatingLines';
import BorderGlow from '../effects/BorderGlow';
import AuroraButton from './AuroraButton';

export const LoginPage = () => {
  const { login, register } = useApp();
  const [mode, setMode] = useState('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [fullName, setFullName] = useState('');
  const [remember, setRemember] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (mode === 'login') {
        await login(email, password, remember);
      } else if (mode === 'register') {
        await register({ email, username, password, full_name: fullName });
      }
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: '#000000',
      zIndex: 999,
    }}>
      {/* FloatingLines Background */}
      <div style={{ position: 'absolute', inset: 0, zIndex: 0 }}>
        <FloatingLines
          linesGradient={['#34d399', '#22d3ee', '#a78bfa', '#34d399']}
          enabledWaves={['top', 'middle', 'bottom']}
          lineCount={[10, 15, 20]}
          lineDistance={[8, 6, 4]}
          bendRadius={5.0}
          bendStrength={-0.5}
          interactive={true}
          parallax={true}
          animationSpeed={0.8}
          mixBlendMode="screen"
        />
      </div>

      {/* Login Card with BorderGlow */}
      <div style={{ position: 'relative', zIndex: 1, width: '100%', maxWidth: '440px', padding: '0 20px' }}>
        <BorderGlow
          edgeSensitivity={30}
          glowColor="160 80 65"
          backgroundColor="rgba(6, 6, 12, 0.88)"
          borderRadius={24}
          glowRadius={40}
          glowIntensity={1.0}
          coneSpread={25}
          colors={['#34d399', '#22d3ee', '#a78bfa']}
          fillOpacity={0.5}
        >
          <div style={{ padding: '40px' }}>
            {/* Brand */}
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <div style={{
                width: '56px',
                height: '56px',
                borderRadius: '16px',
                background: 'linear-gradient(135deg, #059669 0%, #22d3ee 100%)',
                border: '1px solid rgba(52, 211, 153, 0.3)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 16px',
                boxShadow: '0 0 30px rgba(52, 211, 153, 0.3)',
              }}>
                <Sparkles className="w-7 h-7 text-white" />
              </div>
              <h1 style={{
                fontSize: '1.8rem',
                fontWeight: 800,
                letterSpacing: '-0.03em',
                marginBottom: '6px',
              }}>
                CareerPath <span className="gradient-text-cyan">AI</span>
              </h1>
              <p style={{
                fontSize: '0.88rem',
                color: 'var(--text-secondary)',
                lineHeight: 1.5,
              }}>
                Master your tech skill DAG and accelerate your career.
              </p>
            </div>

            {/* Mode Tabs */}
            <div style={{
              display: 'flex',
              gap: '4px',
              padding: '4px',
              borderRadius: '14px',
              background: 'rgba(255, 255, 255, 0.03)',
              border: '1px solid var(--border-subtle)',
              marginBottom: '24px',
            }}>
              {[
                { id: 'login', label: 'Sign In' },
                { id: 'register', label: 'Sign Up' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => { setMode(tab.id); setError(''); }}
                  style={{
                    flex: 1,
                    padding: '10px',
                    borderRadius: '11px',
                    border: 'none',
                    background: mode === tab.id ? 'linear-gradient(135deg, rgba(52, 211, 153, 0.18), rgba(34, 211, 238, 0.18))' : 'transparent',
                    color: mode === tab.id ? '#34d399' : 'var(--text-muted)',
                    fontSize: '0.84rem',
                    fontWeight: mode === tab.id ? 700 : 500,
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {error && (
              <div style={{
                padding: '10px 14px',
                borderRadius: '10px',
                background: 'rgba(244, 63, 94, 0.15)',
                border: '1px solid rgba(244, 63, 94, 0.3)',
                color: '#fb7185',
                fontSize: '0.85rem',
                marginBottom: '16px',
              }}>
                {error}
              </div>
            )}

            {/* Login / Register Forms */}
            <form onSubmit={handleSubmit}>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                  {mode === 'register' && (
                    <>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 600 }}>Full Name</label>
                        <div style={{ position: 'relative' }}>
                          <User className="w-4 h-4" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                          <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            placeholder="Your full name"
                            required
                            className="custom-input"
                            style={{ paddingLeft: '40px' }}
                          />
                        </div>
                      </div>
                      <div>
                        <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 600 }}>Username</label>
                        <div style={{ position: 'relative' }}>
                          <span style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontSize: '0.9rem' }}>@</span>
                          <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="ajmal"
                            required
                            className="custom-input"
                            style={{ paddingLeft: '36px' }}
                          />
                        </div>
                      </div>
                    </>
                  )}
                  <div>
                    <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 600 }}>Email</label>
                    <div style={{ position: 'relative' }}>
                      <Mail className="w-4 h-4" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="you@example.com"
                        required
                        className="custom-input"
                        style={{ paddingLeft: '40px' }}
                      />
                    </div>
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 600 }}>Password</label>
                    <div style={{ position: 'relative' }}>
                      <Lock className="w-4 h-4" style={{ position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
                      <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                        className="custom-input"
                        style={{ paddingLeft: '40px' }}
                      />
                    </div>
                  </div>

                  {mode === 'login' && (
                    <div style={{ display: 'flex', alignItems: 'flex-start', gap: '10px', marginTop: '4px' }}>
                      <input
                        id="remember-me"
                        type="checkbox"
                        checked={remember}
                        onChange={(e) => setRemember(e.target.checked)}
                        style={{ width: '16px', height: '16px', marginTop: '2px', accentColor: '#34d399', cursor: 'pointer' }}
                      />
                      <label htmlFor="remember-me" style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', lineHeight: 1.5, cursor: 'pointer', fontWeight: 500 }}>
                        Keep me signed in
                        <span style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                          Uncheck to end your session when you close the browser. Your password is never stored — only a secure session token (HTTP-only cookie) is kept.
                        </span>
                      </label>
                    </div>
                  )}
                </div>

                <AuroraButton
                  type="submit"
                  disabled={loading}
                  variant="primary"
                  style={{ padding: '14px', fontSize: '0.95rem', marginTop: '20px' }}
                >
                  {loading ? 'Processing...' : <>{mode === 'login' ? 'Sign In' : 'Create Account'} <ArrowRight className="w-4 h-4" /></>}
                </AuroraButton>

                <p style={{ textAlign: 'center', fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: '16px' }}>
                  {mode === 'login' ? (
                    <>Don't have an account?{' '}
                      <span onClick={() => { setMode('register'); setError(''); }} style={{ color: '#34d399', cursor: 'pointer', fontWeight: 600 }}>Sign Up</span>
                    </>
                  ) : (
                    <>Already have an account?{' '}
                      <span onClick={() => { setMode('login'); setError(''); }} style={{ color: '#34d399', cursor: 'pointer', fontWeight: 600 }}>Sign In</span>
                    </>
                  )}
                </p>
              </form>

            {/* Footer */}
            <div style={{ textAlign: 'center', marginTop: '28px', paddingTop: '20px', borderTop: '1px solid var(--border-subtle)' }}>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                DAG Engine v1.0 — Powered by FastAPI
              </p>
            </div>
          </div>
        </BorderGlow>
      </div>
    </div>
  );
};

export default LoginPage;
