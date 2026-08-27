import React from 'react';
import { useApp } from '../../context/AppContext';
import {
  Sparkles,
  Bot,
  Database,
  Globe,
  Cloud,
  Shield,
  Clock,
  Briefcase,
  CheckCircle,
  Layers,
  ArrowRight,
  TrendingUp,
  Cpu,
} from 'lucide-react';

export const CareerExplorer = () => {
  const { careers, currentCareer, selectCareer, setActiveTab } = useApp();

  const careerIcons = {
    'ai-ml-engineer': <Bot className="w-8 h-8 text-cyan-400" />,
    'data-scientist': <Database className="w-8 h-8 text-purple-400" />,
    'full-stack-developer': <Globe className="w-8 h-8 text-emerald-400" />,
    'devops-engineer': <Cloud className="w-8 h-8 text-amber-400" />,
    'cybersecurity-analyst': <Shield className="w-8 h-8 text-rose-400" />,
  };

  const salaries = {
    'ai-ml-engineer': '$145,000 – $245,000',
    'data-scientist': '$125,000 – $210,000',
    'full-stack-developer': '$115,000 – $195,000',
    'devops-engineer': '$130,000 – $220,000',
    'cybersecurity-analyst': '$120,000 – $205,000',
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-cyan">Specialization Tracks</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Explore Tech Career Pathways
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '680px' }}>
          Choose your target software engineering specialization. Each track comes with an industry-vetted skill DAG, prerequisite hierarchy, portfolio projects, and salary benchmarks.
        </p>
      </div>

      {/* Career Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(360px, 1fr))', gap: '20px' }}>
        {careers.map((c) => {
          const isActive = currentCareer?.id === c.id;
          const icon = careerIcons[c.slug] || <Cpu className="w-8 h-8 text-cyan-400" />;
          const salary = salaries[c.slug] || '$120,000 – $200,000';

          return (
            <div
              key={c.id}
              className={`glass-panel ${isActive ? 'glass-panel-elevated' : ''}`}
              style={{
                padding: '24px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '18px',
                border: isActive ? '1px solid rgba(56, 189, 248, 0.5)' : '1px solid var(--border-subtle)',
                background: isActive
                  ? 'linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(30, 27, 75, 0.7))'
                  : 'rgba(15, 23, 42, 0.65)',
                boxShadow: isActive ? '0 10px 30px rgba(56, 189, 248, 0.15)' : 'none',
              }}
            >
              <div>
                {/* Top header row */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '14px' }}>
                  <div
                    style={{
                      padding: '12px',
                      borderRadius: '16px',
                      background: 'rgba(255, 255, 255, 0.05)',
                      border: '1px solid rgba(255, 255, 255, 0.1)',
                    }}
                  >
                    {icon}
                  </div>
                  {isActive ? (
                    <span className="badge badge-emerald" style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <CheckCircle className="w-3.5 h-3.5" /> Active Track
                    </span>
                  ) : (
                    <span className="badge badge-cyan">{c.difficulty || 'Intermediate'}</span>
                  )}
                </div>

                {/* Title & Description */}
                <h3 style={{ fontSize: '1.3rem', fontWeight: 800, marginBottom: '6px', color: 'var(--text-primary)' }}>
                  {c.title}
                </h3>
                <p style={{ fontSize: '0.88rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '16px' }}>
                  {c.description}
                </p>

                {/* Key Metrics */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '10px',
                    padding: '12px',
                    borderRadius: '12px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                    marginBottom: '16px',
                  }}
                >
                  <div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                      Skill Nodes
                    </span>
                    <div style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                      {c.skill_count || 25} Curated Skills
                    </div>
                  </div>
                  <div>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                      Salary Range
                    </span>
                    <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#34d399' }}>
                      {salary}
                    </div>
                  </div>
                </div>

                {/* Major Technologies */}
                <div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600, display: 'block', marginBottom: '8px' }}>
                    Major Technologies & Stacks
                  </span>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                    {(c.major_technologies || []).map((tech, idx) => (
                      <span
                        key={idx}
                        style={{
                          padding: '4px 10px',
                          borderRadius: '8px',
                          background: 'rgba(56, 189, 248, 0.08)',
                          border: '1px solid rgba(56, 189, 248, 0.2)',
                          color: '#38bdf8',
                          fontSize: '0.78rem',
                          fontWeight: 500,
                        }}
                      >
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                {isActive ? (
                  <button
                    onClick={() => setActiveTab('roadmap')}
                    className="btn-primary"
                    style={{ width: '100%', padding: '10px', fontSize: '0.88rem' }}
                  >
                    <Layers className="w-4 h-4" /> Open Skill DAG Visualizer
                  </button>
                ) : (
                  <button
                    onClick={() => {
                      selectCareer(c);
                      setActiveTab('roadmap');
                    }}
                    className="btn-secondary"
                    style={{ width: '100%', padding: '10px', fontSize: '0.88rem' }}
                  >
                    Set as Target Career →
                  </button>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
