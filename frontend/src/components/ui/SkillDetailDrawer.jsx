import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  X,
  CheckCircle,
  Clock,
  BookOpen,
  Sparkles,
  ExternalLink,
  Github,
  Award,
  Video,
  FileText,
  Bookmark,
  ChevronRight,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';
import { api } from '../../services/api';

export const SkillDetailDrawer = () => {
  const {
    isSkillDrawerOpen,
    closeSkillDrawer,
    selectedSkillId,
    updateSkillProgress,
    openSkillDrawer,
    user,
    setIsAuthModalOpen,
  } = useApp();

  const [skill, setSkill] = useState(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('not_started');
  const [progress, setProgress] = useState(0);
  const [notes, setNotes] = useState('');
  const [githubUrl, setGithubUrl] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!selectedSkillId) return;

    const fetchDetail = async () => {
      setLoading(true);
      try {
        const data = await api.getSkillDetail(selectedSkillId);
        setSkill(data);
        const us = data.user_state || {};
        setStatus(us.status || 'not_started');
        setProgress(us.progress || (us.status === 'completed' ? 100 : us.status === 'in_progress' ? 50 : 0));
        setNotes(us.notes || '');
        setGithubUrl(us.github_url || '');
      } catch (err) {
        console.warn('Failed to load skill details', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDetail();
  }, [selectedSkillId]);

  if (!isSkillDrawerOpen) return null;

  const handleSaveProgress = async (newStatus = status, newProgress = progress) => {
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    setSaving(true);
    try {
      await updateSkillProgress(selectedSkillId, {
        status: newStatus,
        progress: newProgress,
        notes,
        github_url: githubUrl,
      });
      setStatus(newStatus);
      setProgress(newProgress);
    } catch (e) {
      // handled in context
    } finally {
      setSaving(false);
    }
  };

  const handleCompleteQuick = () => {
    handleSaveProgress('completed', 100);
  };

  const getResourceIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="w-4 h-4 text-rose-400" />;
      case 'book':
        return <Bookmark className="w-4 h-4 text-amber-400" />;
      case 'docs':
      case 'tutorial':
        return <FileText className="w-4 h-4 text-cyan-400" />;
      default:
        return <BookOpen className="w-4 h-4 text-indigo-400" />;
    }
  };

  return (
    <div className="modal-backdrop" style={{ justifyContent: 'flex-end', padding: 0 }}>
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '520px',
          height: '100%',
          padding: '28px',
          background: 'rgba(10, 14, 22, 0.96)',
          borderLeft: '1px solid rgba(56, 189, 248, 0.25)',
          borderRadius: 0,
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '-15px 0 40px rgba(0, 0, 0, 0.8)',
          overflowY: 'auto',
        }}
      >
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', flexWrap: 'wrap' }}>
              <span className={`badge ${status === 'completed' ? 'badge-emerald' : status === 'in_progress' ? 'badge-amber' : 'badge-cyan'}`}>
                {status.replace('_', ' ')}
              </span>
              <span className="badge badge-purple">{skill?.level || 'Intermediate'}</span>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <Clock className="w-3.5 h-3.5" /> {skill?.estimated_hours || 10}h est.
              </span>
            </div>
            <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--text-primary)', letterSpacing: '-0.02em' }}>
              {skill?.name || 'Loading skill...'}
            </h2>
          </div>
          <button
            onClick={closeSkillDrawer}
            style={{
              background: 'rgba(255, 255, 255, 0.06)',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              padding: '8px',
              borderRadius: '50%',
              display: 'flex',
            }}
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '60px 0', color: 'var(--text-muted)' }}>
            <Sparkles className="w-8 h-8 mx-auto mb-2 animate-spin text-cyan-400" />
            <p>Loading skill DAG details...</p>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
            {/* Why It Matters Callout */}
            {skill?.why_important && (
              <div
                style={{
                  padding: '16px',
                  borderRadius: '14px',
                  background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(99, 102, 241, 0.08))',
                  border: '1px solid rgba(56, 189, 248, 0.25)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#38bdf8', fontSize: '0.82rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '6px' }}>
                  <Sparkles className="w-4 h-4" /> Why It's Crucial in Production
                </div>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                  {skill.why_important}
                </p>
              </div>
            )}

            {/* Description */}
            <div>
              <h4 style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Overview & Learning Objectives
              </h4>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-primary)', lineHeight: 1.6 }}>
                {skill?.description || 'Core technical competency required for high-velocity software engineering.'}
              </p>
            </div>

            {/* Quick Actions & Status Controller */}
            <div
              style={{
                padding: '18px',
                borderRadius: '14px',
                background: 'rgba(15, 23, 42, 0.7)',
                border: '1px solid var(--border-subtle)',
                display: 'flex',
                flexDirection: 'column',
                gap: '14px',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.88rem', fontWeight: 600 }}>Your Mastery Status</span>
                <span style={{ fontSize: '0.82rem', fontWeight: 700, color: status === 'completed' ? '#34d399' : '#38bdf8' }}>
                  {progress}% Complete
                </span>
              </div>

              {/* Status Buttons */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '8px' }}>
                <button
                  type="button"
                  onClick={() => {
                    setStatus('not_started');
                    setProgress(0);
                    handleSaveProgress('not_started', 0);
                  }}
                  style={{
                    padding: '8px',
                    borderRadius: '10px',
                    border: status === 'not_started' ? '1px solid var(--text-muted)' : '1px solid transparent',
                    background: status === 'not_started' ? 'rgba(255, 255, 255, 0.1)' : 'rgba(255, 255, 255, 0.03)',
                    color: status === 'not_started' ? '#fff' : 'var(--text-muted)',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  Not Started
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setStatus('in_progress');
                    const newProg = progress > 0 ? progress : 50;
                    setProgress(newProg);
                    handleSaveProgress('in_progress', newProg);
                  }}
                  style={{
                    padding: '8px',
                    borderRadius: '10px',
                    border: status === 'in_progress' ? '1px solid #f59e0b' : '1px solid transparent',
                    background: status === 'in_progress' ? 'rgba(245, 158, 11, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                    color: status === 'in_progress' ? '#fbbf24' : 'var(--text-muted)',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  In Progress
                </button>
                <button
                  type="button"
                  onClick={handleCompleteQuick}
                  style={{
                    padding: '8px',
                    borderRadius: '10px',
                    border: status === 'completed' ? '1px solid #10b981' : '1px solid transparent',
                    background: status === 'completed' ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                    color: status === 'completed' ? '#34d399' : 'var(--text-muted)',
                    fontSize: '0.8rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  ✓ Mastered
                </button>
              </div>

              {/* Progress Slider */}
              <div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={progress}
                  onChange={(e) => {
                    const val = Number(e.target.value);
                    setProgress(val);
                    if (val === 100) setStatus('completed');
                    else if (val > 0) setStatus('in_progress');
                    else setStatus('not_started');
                  }}
                  onMouseUp={() => handleSaveProgress()}
                  style={{ width: '100%', accentColor: '#38bdf8', cursor: 'pointer' }}
                />
              </div>

              {status !== 'completed' && (
                <button
                  onClick={handleCompleteQuick}
                  disabled={saving}
                  className="btn-emerald"
                  style={{ width: '100%', padding: '10px', fontSize: '0.88rem' }}
                >
                  <Award className="w-4 h-4" /> Mark as Mastered (+50 XP)
                </button>
              )}
            </div>

            {/* Prerequisites */}
            {skill?.prerequisites && skill.prerequisites.length > 0 && (
              <div>
                <h4 style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '10px' }}>
                  Prerequisite Chain ({skill.prerequisites.length})
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {skill.prerequisites.map((p) => (
                    <div
                      key={p.skill_id}
                      onClick={() => openSkillDrawer(p.skill_id)}
                      style={{
                        padding: '10px 14px',
                        borderRadius: '10px',
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid var(--border-subtle)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        cursor: 'pointer',
                        transition: 'all 0.15s ease',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        {p.status === 'completed' ? (
                          <CheckCircle className="w-4 h-4 text-emerald-400" />
                        ) : (
                          <div style={{ width: '16px', height: '16px', borderRadius: '50%', border: '2px solid #64748b' }} />
                        )}
                        <span style={{ fontSize: '0.88rem', fontWeight: 500, color: p.status === 'completed' ? 'var(--text-primary)' : 'var(--text-secondary)' }}>
                          {p.name}
                        </span>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-500" />
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Dependent Skills Unlocked */}
            {skill?.dependents && skill.dependents.length > 0 && (
              <div>
                <h4 style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '10px' }}>
                  Unlocks Next ({skill.dependents.length})
                </h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                  {skill.dependents.map((d) => (
                    <button
                      key={d.skill_id}
                      onClick={() => openSkillDrawer(d.skill_id)}
                      style={{
                        padding: '6px 12px',
                        borderRadius: '8px',
                        background: 'rgba(56, 189, 248, 0.08)',
                        border: '1px solid rgba(56, 189, 248, 0.25)',
                        color: '#38bdf8',
                        fontSize: '0.82rem',
                        fontWeight: 500,
                        cursor: 'pointer',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '6px',
                      }}
                    >
                      <span>{d.name}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Learning Resources */}
            <div>
              <h4 style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '10px' }}>
                Curated Learning Resources ({skill?.resources?.length || 0})
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {(!skill?.resources || skill.resources.length === 0) ? (
                  <p style={{ fontSize: '0.84rem', color: 'var(--text-muted)' }}>
                    Standard industry documentation and open-source tutorials apply.
                  </p>
                ) : (
                  skill.resources.map((res) => (
                    <a
                      key={res.id}
                      href={res.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        padding: '12px 14px',
                        borderRadius: '12px',
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid var(--border-subtle)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        textDecoration: 'none',
                        transition: 'all 0.2s ease',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        {getResourceIcon(res.resource_type)}
                        <div>
                          <div style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                            {res.title}
                          </div>
                          <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', gap: '8px' }}>
                            <span>{res.platform || 'Online'}</span>
                            <span>•</span>
                            <span>{res.is_free ? 'Free' : 'Paid/Course'}</span>
                          </div>
                        </div>
                      </div>
                      <ExternalLink className="w-4 h-4 text-slate-400" />
                    </a>
                  ))
                )}
              </div>
            </div>

            {/* Notes & Evidence Section */}
            <div style={{ paddingBottom: '20px' }}>
              <h4 style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-secondary)', textTransform: 'uppercase', marginBottom: '10px' }}>
                Project Evidence & Notes
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                    GitHub Repo / Proof Link
                  </label>
                  <div style={{ position: 'relative' }}>
                    <input
                      type="url"
                      placeholder="https://github.com/username/project"
                      value={githubUrl}
                      onChange={(e) => setGithubUrl(e.target.value)}
                      className="custom-input"
                      style={{ paddingLeft: '36px', fontSize: '0.85rem' }}
                    />
                    <Github className="w-4 h-4 text-slate-400" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                  </div>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
                    Personal Learning Notes
                  </label>
                  <textarea
                    placeholder="Key concepts, commands, or architecture notes..."
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    className="custom-textarea"
                    style={{ minHeight: '80px', fontSize: '0.85rem' }}
                  />
                </div>

                <button
                  type="button"
                  onClick={() => handleSaveProgress()}
                  disabled={saving}
                  className="btn-secondary"
                  style={{ width: '100%', fontSize: '0.86rem' }}
                >
                  {saving ? 'Saving...' : '💾 Save Notes & Evidence'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
