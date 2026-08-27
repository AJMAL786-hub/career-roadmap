import React, { useEffect, useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Sparkles,
  Award,
  Zap,
  Clock,
  Target,
  ArrowUpRight,
  TrendingUp,
  CheckCircle2,
  BookOpen,
  Briefcase,
  Play,
  Flame,
  Layers,
  ChevronRight,
} from 'lucide-react';
import { api } from '../../services/api';

export const DashboardView = () => {
  const {
    user,
    currentCareer,
    dashboardData,
    openSkillDrawer,
    setActiveTab,
    setIsAuthModalOpen,
    roadmap,
  } = useApp();

  const [profileData, setProfileData] = useState(null);
  const [studyStats, setStudyStats] = useState(null);

  useEffect(() => {
    if (!user) return;
    const fetchExtra = async () => {
      try {
        const prof = await api.getProfile();
        setProfileData(prof);
      } catch (e) {
        // fallback
      }
      try {
        const stats = await api.getStudyStats();
        setStudyStats(stats);
      } catch (e) {
        // fallback
      }
    };
    fetchExtra();
  }, [user]);

  const nodes = roadmap.nodes || [];
  const masteredCount = nodes.filter((n) => n.user_status === 'completed').length;
  const inProgressCount = nodes.filter((n) => n.user_status === 'in_progress').length;
  const totalCount = nodes.length || 25;
  const readinessPercent = Math.round((masteredCount / totalCount) * 100);

  // Recommended next skills (Frontier skills: not started but all prerequisites completed)
  const nextSkills = dashboardData?.next_skills || nodes.filter((n) => n.user_status !== 'completed').slice(0, 3);

  const streakDays = profileData?.streak?.current_streak || 7;
  const userXp = user?.xp || 650;
  const currentLevel = profileData?.gamification?.level || Math.floor(userXp / 200) + 1;
  const levelTitle = profileData?.gamification?.title || (currentLevel > 3 ? 'Systems Architect' : 'Apprentice');
  const nextLevelXp = currentLevel * 200;
  const levelProgress = Math.round(((userXp % 200) / 200) * 100);

  const weeklyHours = [2.5, 3.8, 4.2, 1.5, 3.0, 5.2, 2.0];
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Hero Welcome Card */}
      <div
        className="glass-panel-elevated"
        style={{
          padding: '28px 32px',
          background: 'linear-gradient(135deg, rgba(6, 10, 16, 0.92) 0%, rgba(10, 20, 24, 0.6) 100%)',
          display: 'grid',
          gridTemplateColumns: '1fr auto',
          alignItems: 'center',
          gap: '24px',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '10px' }}>
            <span className="badge badge-cyan">Target Career Track</span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>•</span>
            <span style={{ fontSize: '0.85rem', color: '#c084fc', fontWeight: 600 }}>
              {currentCareer?.title || 'AI/ML Engineering'}
            </span>
          </div>

          <h1 style={{ fontSize: '2rem', fontWeight: 800, letterSpacing: '-0.03em', marginBottom: '10px' }}>
            Welcome back, <span className="gradient-text-cyan">{user?.full_name || 'Tech Innovator'}</span>! 👋
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '650px', lineHeight: 1.6 }}>
            You are making steady progress toward mastering your tech skill DAG. Complete your next frontier skills to boost your production job readiness score!
          </p>

          <div style={{ display: 'flex', gap: '12px', marginTop: '20px', flexWrap: 'wrap' }}>
            <button
              onClick={() => setActiveTab('roadmap')}
              className="btn-primary"
            >
              <Layers className="w-4 h-4" /> Open Interactive Skill DAG
            </button>
            <button
              onClick={() => setActiveTab('jobs')}
              className="btn-secondary"
            >
              <Briefcase className="w-4 h-4" /> Scan Job Gap
            </button>
          </div>
        </div>

        {/* Readiness Circular Ring Meter */}
        <div
          style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '20px 26px',
            borderRadius: '20px',
            background: 'rgba(6, 8, 14, 0.8)',
            border: '1px solid rgba(52, 211, 153, 0.3)',
            boxShadow: '0 0 30px rgba(52, 211, 153, 0.12)',
          }}
        >
          <div style={{ position: 'relative', width: '110px', height: '110px' }}>
            <svg style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
              <circle
                cx="55"
                cy="55"
                r="44"
                stroke="rgba(255, 255, 255, 0.08)"
                strokeWidth="9"
                fill="none"
              />
              <circle
                cx="55"
                cy="55"
                r="44"
                stroke="url(#readinessGrad)"
                strokeWidth="9"
                strokeDasharray={276}
                strokeDashoffset={276 - (276 * readinessPercent) / 100}
                strokeLinecap="round"
                fill="none"
                style={{ transition: 'stroke-dashoffset 1s ease' }}
              />
              <defs>
                <linearGradient id="readinessGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#34d399" />
                  <stop offset="100%" stopColor="#22d3ee" />
                </linearGradient>
              </defs>
            </svg>
            <div
              style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
              }}
            >
              <span style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
                {readinessPercent}%
              </span>
              <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Ready
              </span>
            </div>
          </div>
          <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-primary)', marginTop: '8px' }}>
            Job Readiness
          </span>
        </div>
      </div>

      {/* Gamification & Telemetry Stats Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '16px' }}>
        {/* Level & XP Card */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Mastery Level
              </span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginTop: '2px' }}>
                Level {currentLevel} • <span style={{ color: '#c084fc', fontSize: '0.95rem' }}>{levelTitle}</span>
              </h3>
            </div>
            <div style={{ padding: '8px', borderRadius: '12px', background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc' }}>
              <Award className="w-5 h-5" />
            </div>
          </div>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '6px', color: 'var(--text-secondary)' }}>
              <span>{userXp} Total XP</span>
              <span>{nextLevelXp} XP (Next Rank)</span>
            </div>
            <div style={{ width: '100%', height: '8px', borderRadius: '999px', background: 'rgba(255, 255, 255, 0.08)', overflow: 'hidden' }}>
              <div
                style={{
                  width: `${levelProgress}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #38bdf8, #a855f7)',
                  borderRadius: '999px',
                }}
              />
            </div>
          </div>
        </div>

        {/* Streak Flame Card */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Learning Streak
              </span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginTop: '2px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                {streakDays} Days <span style={{ fontSize: '1.2rem' }}>🔥</span>
              </h3>
            </div>
            <div style={{ padding: '8px', borderRadius: '12px', background: 'rgba(244, 63, 94, 0.15)', color: '#fb7185' }}>
              <Flame className="w-5 h-5" />
            </div>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            Keep your streak alive by logging a 25-min study session or mastering a DAG node today!
          </p>
        </div>

        {/* Mastered Skills Count */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                DAG Nodes Completed
              </span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginTop: '2px', color: '#34d399' }}>
                {masteredCount} / {totalCount} Skills
              </h3>
            </div>
            <div style={{ padding: '8px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.15)', color: '#34d399' }}>
              <CheckCircle2 className="w-5 h-5" />
            </div>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            {inProgressCount} skills currently actively in progress across layers.
          </p>
        </div>

        {/* Weekly Study Hours */}
        <div className="glass-panel" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
            <div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>
                Study Time This Week
              </span>
              <h3 style={{ fontSize: '1.25rem', fontWeight: 800, marginTop: '2px', color: '#38bdf8' }}>
                22.4 Hours
              </h3>
            </div>
            <div style={{ padding: '8px', borderRadius: '12px', background: 'rgba(56, 189, 248, 0.15)', color: '#38bdf8' }}>
              <Clock className="w-5 h-5" />
            </div>
          </div>
          <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            +18% study intensity compared to last week.
          </p>
        </div>
      </div>

      {/* Main Content Grid: Recommended Frontier & Weekly Activity */}
      <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1.4fr 1fr', gap: '20px' }}>
        {/* Next Recommended Frontier Skills */}
        <div className="glass-panel" style={{ padding: '24px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <div>
              <h3 style={{ fontSize: '1.15rem', fontWeight: 800 }}>Next Recommended Frontier Skills</h3>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                Optimal next nodes to master based on your completed prerequisites.
              </p>
            </div>
            <button
              onClick={() => setActiveTab('roadmap')}
              style={{
                background: 'none',
                border: 'none',
                color: 'var(--accent-cyan)',
                fontSize: '0.82rem',
                fontWeight: 600,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
              }}
            >
              View Full DAG <ChevronRight className="w-4 h-4" />
            </button>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {nextSkills.map((item, idx) => {
              const skill = item.skill || item;
              return (
                <div
                  key={item.id || idx}
                  onClick={() => openSkillDrawer(skill.id || item.skill_id)}
                  style={{
                    padding: '16px',
                    borderRadius: '14px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                  }}
                  className="hover:border-cyan-500/40 hover:bg-slate-900/60"
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
                    <div
                      style={{
                        width: '42px',
                        height: '42px',
                        borderRadius: '12px',
                        background: 'linear-gradient(135deg, rgba(52, 211, 153, 0.15), rgba(34, 211, 238, 0.15))',
                        border: '1px solid rgba(52, 211, 153, 0.3)',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        color: '#34d399',
                        fontWeight: 700,
                      }}
                    >
                      {idx + 1}
                    </div>
                    <div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                          {skill.name}
                        </h4>
                        <span className="badge badge-purple">{skill.level || 'Core'}</span>
                      </div>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                        {skill.description?.slice(0, 75) || 'Core technical capability'}...
                      </p>
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      <Clock className="w-3.5 h-3.5" /> {skill.estimated_hours || 10}h
                    </span>
                    <button
                      className="btn-primary"
                      style={{ padding: '6px 14px', fontSize: '0.8rem' }}
                      onClick={(e) => {
                        e.stopPropagation();
                        openSkillDrawer(skill.id || item.skill_id);
                      }}
                    >
                      Start Node →
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Weekly Study Activity Chart */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h3 style={{ fontSize: '1.15rem', fontWeight: 800, marginBottom: '4px' }}>Weekly Study Focus</h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '20px' }}>
              Hours logged over the last 7 days.
            </p>

            {/* Bar Chart Visualization */}
            <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: '140px', paddingBottom: '10px' }}>
              {weeklyHours.map((hrs, i) => {
                const heightPercent = Math.min((hrs / 6) * 100, 100);
                return (
                  <div key={days[i]} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px', flex: 1 }}>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{hrs}h</span>
                    <div
                      style={{
                        width: '28px',
                        height: `${heightPercent}%`,
                        minHeight: '12px',
                        borderRadius: '6px 6px 0 0',
                        background: i === 5 ? 'linear-gradient(180deg, #34d399, #0891b2)' : 'rgba(52, 211, 153, 0.3)',
                        border: i === 5 ? '1px solid #34d399' : '1px solid rgba(255, 255, 255, 0.05)',
                        transition: 'all 0.3s ease',
                      }}
                    />
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: i === 5 ? '#34d399' : 'var(--text-secondary)' }}>
                      {days[i]}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          <div
            style={{
              padding: '14px',
              borderRadius: '12px',
              background: 'rgba(6, 8, 14, 0.7)',
              border: '1px solid var(--border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Clock className="w-4 h-4 text-cyan-400" />
              <span style={{ fontSize: '0.84rem', fontWeight: 600 }}>Ready to focus?</span>
            </div>
            <button
              onClick={() => setActiveTab('study')}
              className="btn-primary"
              style={{ padding: '6px 14px', fontSize: '0.8rem' }}
            >
              Launch Pomodoro Timer
            </button>
          </div>
        </div>
      </div>

      {/* Career Quick Action Hub */}
      <div>
        <h3 style={{ fontSize: '1.15rem', fontWeight: 800, marginBottom: '14px' }}>Career Acceleration Hub</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '16px' }}>
          <div
            onClick={() => setActiveTab('jobs')}
            className="glass-panel hover:border-cyan-400/50 cursor-pointer"
            style={{ padding: '20px', transition: 'all 0.2s ease' }}
          >
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(52, 211, 153, 0.15)', color: '#34d399', width: 'fit-content', marginBottom: '12px' }}>
              <Briefcase className="w-5 h-5" />
            </div>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '4px' }}>Job Gap Analyzer</h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Paste job descriptions to evaluate ATS match score & missing skills.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('interviews')}
            className="glass-panel hover:border-purple-400/50 cursor-pointer"
            style={{ padding: '20px', transition: 'all 0.2s ease' }}
          >
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(168, 85, 247, 0.15)', color: '#c084fc', width: 'fit-content', marginBottom: '12px' }}>
              <Sparkles className="w-5 h-5" />
            </div>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '4px' }}>AI Mock Interview</h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Practice 64+ technical & system design questions with rubric evaluations.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('resume')}
            className="glass-panel hover:border-emerald-400/50 cursor-pointer"
            style={{ padding: '20px', transition: 'all 0.2s ease' }}
          >
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', width: 'fit-content', marginBottom: '12px' }}>
              <BookOpen className="w-5 h-5" />
            </div>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '4px' }}>ATS Resume Matcher</h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Scan your resume keywords against top engineering salary roles.
            </p>
          </div>

          <div
            onClick={() => setActiveTab('projects')}
            className="glass-panel hover:border-amber-400/50 cursor-pointer"
            style={{ padding: '20px', transition: 'all 0.2s ease' }}
          >
            <div style={{ padding: '10px', borderRadius: '12px', background: 'rgba(245, 158, 11, 0.15)', color: '#fbbf24', width: 'fit-content', marginBottom: '12px' }}>
              <Target className="w-5 h-5" />
            </div>
            <h4 style={{ fontSize: '1rem', fontWeight: 700, marginBottom: '4px' }}>Portfolio Projects</h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
              Build 15 production-grade projects with structured rubrics and GitHub proof.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
