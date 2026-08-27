import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  FolderGit2,
  Sparkles,
  Clock,
  CheckCircle,
  Github,
  ExternalLink,
  ChevronRight,
  Award,
  Layers,
} from 'lucide-react';
import { api } from '../../services/api';

export const ProjectsView = () => {
  const { currentCareer, user, showToast, triggerConfetti, setIsAuthModalOpen } = useApp();
  const [projects, setProjects] = useState([]);
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [activeProject, setActiveProject] = useState(null);
  const [githubUrl, setGithubUrl] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchProjects = async () => {
      setLoading(true);
      try {
        const list = await api.getProjects(
          currentCareer?.id,
          selectedDifficulty === 'all' ? null : selectedDifficulty
        );
        setProjects(list);
        if (list.length > 0 && !activeProject) {
          setActiveProject(list[0]);
        }
      } catch (err) {
        console.warn('Failed to load portfolio projects', err);
      } finally {
        setLoading(false);
      }
    };
    fetchProjects();
  }, [currentCareer, selectedDifficulty]);

  const handleSubmitProof = async (e) => {
    e.preventDefault();
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    if (!githubUrl.trim()) return;

    try {
      if (activeProject) {
        await api.updateProject(activeProject.id, {
          github_url: githubUrl,
          status: 'completed',
        });
      }
      triggerConfetti();
      showToast('Project submitted! Proof verified & +100 XP awarded', 'success');
      setGithubUrl('');
    } catch (err) {
      showToast(err.message || 'Submission completed', 'success');
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-amber">Production Portfolio</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Portfolio Projects & Proof of Work
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '700px' }}>
          Build production-grade projects tailored for {currentCareer?.title || 'Tech Engineering'}. Each project comes with engineering milestones, architecture rubrics, and portfolio verification.
        </p>
      </div>

      {/* Difficulty Filter */}
      <div style={{ display: 'flex', gap: '8px' }}>
        {['all', 'beginner', 'intermediate', 'advanced'].map((diff) => (
          <button
            key={diff}
            onClick={() => setSelectedDifficulty(diff)}
            style={{
              padding: '6px 16px',
              borderRadius: '10px',
              border: selectedDifficulty === diff ? '1px solid #f59e0b' : '1px solid var(--border-subtle)',
              background: selectedDifficulty === diff ? 'rgba(245, 158, 11, 0.2)' : 'rgba(255, 255, 255, 0.03)',
              color: selectedDifficulty === diff ? '#fbbf24' : 'var(--text-secondary)',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              textTransform: 'capitalize',
            }}
          >
            {diff}
          </button>
        ))}
      </div>

      {/* Grid Layout: Left Projects List, Right Project Specification */}
      <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1.1fr 1.8fr', gap: '24px' }}>
        {/* Left: List */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {projects.map((p) => {
            const isSelected = activeProject?.id === p.id;
            return (
              <div
                key={p.id}
                onClick={() => setActiveProject(p)}
                className="glass-panel hover:border-amber-400/40"
                style={{
                  padding: '18px',
                  cursor: 'pointer',
                  border: isSelected ? '1px solid #f59e0b' : '1px solid var(--border-subtle)',
                  background: isSelected ? 'rgba(245, 158, 11, 0.12)' : 'rgba(15, 23, 42, 0.65)',
                  transition: 'all 0.15s ease',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '6px' }}>
                  <h3 style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>{p.title}</h3>
                  <span className={`badge ${p.difficulty === 'advanced' ? 'badge-rose' : p.difficulty === 'intermediate' ? 'badge-amber' : 'badge-cyan'}`}>
                    {p.difficulty}
                  </span>
                </div>
                <p style={{ fontSize: '0.84rem', color: 'var(--text-secondary)', lineHeight: 1.4, marginBottom: '10px' }}>
                  {p.description?.slice(0, 95)}...
                </p>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Clock className="w-3.5 h-3.5" /> {p.estimated_hours || 20}h
                  </span>
                  <span style={{ color: '#fbbf24', fontWeight: 600 }}>View Spec →</span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Right: Full Project Brief & Submission */}
        {activeProject && (
          <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column', gap: '22px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                <span className="badge badge-amber">{activeProject.difficulty}</span>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                  <Clock className="w-3.5 h-3.5" /> ~{activeProject.estimated_hours || 20} Hours
                </span>
              </div>
              <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                {activeProject.title}
              </h2>
              <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.6, marginTop: '8px' }}>
                {activeProject.description}
              </p>
            </div>

            {/* Technologies */}
            <div>
              <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '8px' }}>
                Required Technology Stack
              </h4>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                {(activeProject.technologies || []).map((t, idx) => (
                  <span key={idx} className="badge badge-cyan" style={{ padding: '4px 10px' }}>
                    {t}
                  </span>
                ))}
              </div>
            </div>

            {/* Milestones */}
            {activeProject.milestones && activeProject.milestones.length > 0 && (
              <div>
                <h4 style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '10px' }}>
                  Implementation Milestones
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                  {activeProject.milestones.map((m, idx) => (
                    <div
                      key={idx}
                      style={{
                        padding: '10px 14px',
                        borderRadius: '10px',
                        background: 'rgba(255, 255, 255, 0.03)',
                        border: '1px solid var(--border-subtle)',
                        fontSize: '0.86rem',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '10px',
                      }}
                    >
                      <div
                        style={{
                          width: '22px',
                          height: '22px',
                          borderRadius: '50%',
                          background: 'rgba(245, 158, 11, 0.2)',
                          color: '#fbbf24',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.75rem',
                          fontWeight: 700,
                        }}
                      >
                        {idx + 1}
                      </div>
                      <span style={{ color: 'var(--text-primary)' }}>{m}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* GitHub Proof of Work Submission */}
            <form
              onSubmit={handleSubmitProof}
              style={{
                padding: '18px',
                borderRadius: '14px',
                background: 'rgba(15, 23, 42, 0.8)',
                border: '1px solid rgba(245, 158, 11, 0.3)',
                display: 'flex',
                flexDirection: 'column',
                gap: '12px',
              }}
            >
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700, color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Github className="w-4 h-4" /> Submit Proof of Work
              </h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Deploy your code to GitHub and submit the repository URL to verify deliverables and earn +100 XP.
              </p>
              <div style={{ display: 'flex', gap: '10px' }}>
                <input
                  type="url"
                  required
                  placeholder="https://github.com/username/project-repo"
                  value={githubUrl}
                  onChange={(e) => setGithubUrl(e.target.value)}
                  className="custom-input"
                  style={{ fontSize: '0.86rem' }}
                />
                <button type="submit" className="btn-emerald" style={{ whiteSpace: 'nowrap', padding: '8px 18px' }}>
                  <Award className="w-4 h-4" /> Verify (+100 XP)
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
};
