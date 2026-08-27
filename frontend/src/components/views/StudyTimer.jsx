import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Play,
  Pause,
  RotateCcw,
  SkipForward,
  Clock,
  Sparkles,
  Flame,
  Award,
  BookOpen,
  CheckCircle,
  Save,
} from 'lucide-react';
import { api } from '../../services/api';

const MODES = {
  focus: { label: 'Focus Session', minutes: 25, color: '#38bdf8' },
  shortBreak: { label: 'Short Break', minutes: 5, color: '#34d399' },
  longBreak: { label: 'Long Break', minutes: 15, color: '#c084fc' },
};

export const StudyTimer = () => {
  const { roadmap, user, showToast, triggerConfetti, setIsAuthModalOpen, refreshUser } = useApp();
  const [currentMode, setCurrentMode] = useState('focus');
  const [timeLeft, setTimeLeft] = useState(MODES.focus.minutes * 60);
  const [isRunning, setIsRunning] = useState(false);
  const [selectedSkillId, setSelectedSkillId] = useState('');
  const [sessionNotes, setSessionNotes] = useState('');
  const [sessions, setSessions] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const totalSeconds = MODES[currentMode].minutes * 60;
  const progressPercent = ((totalSeconds - timeLeft) / totalSeconds) * 100;

  // Load past study sessions
  useEffect(() => {
    if (!user) return;
    const fetchHistory = async () => {
      setLoadingHistory(true);
      try {
        const list = await api.getStudySessions(10);
        setSessions(list);
      } catch (e) {
        // fallback
      } finally {
        setLoadingHistory(false);
      }
    };
    fetchHistory();
  }, [user]);

  // Timer countdown effect
  useEffect(() => {
    let interval = null;
    if (isRunning && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((prev) => prev - 1);
      }, 1000);
    } else if (timeLeft === 0 && isRunning) {
      setIsRunning(false);
      handleSessionComplete();
    }
    return () => clearInterval(interval);
  }, [isRunning, timeLeft]);

  const switchMode = (modeKey) => {
    setCurrentMode(modeKey);
    setTimeLeft(MODES[modeKey].minutes * 60);
    setIsRunning(false);
  };

  const handleSessionComplete = async () => {
    triggerConfetti();
    showToast(`🎉 ${MODES[currentMode].label} Complete! Great focus session.`, 'success');

    if (currentMode === 'focus' && user) {
      try {
        await api.logStudySession({
          skill_id: selectedSkillId ? Number(selectedSkillId) : null,
          duration_minutes: MODES.focus.minutes,
          notes: sessionNotes || 'Focused Pomodoro Study Session',
        });
        showToast('Study session recorded! +25 XP & streak maintained', 'success');
        refreshUser();
        const updated = await api.getStudySessions(10);
        setSessions(updated);
      } catch (e) {
        // ignore
      }
    }
  };

  const handleManualLog = async (e) => {
    e.preventDefault();
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    try {
      await api.logStudySession({
        skill_id: selectedSkillId ? Number(selectedSkillId) : null,
        duration_minutes: MODES[currentMode].minutes,
        notes: sessionNotes || 'Focused deep work session',
      });
      triggerConfetti();
      showToast('Logged study session to your profile! +XP awarded', 'success');
      refreshUser();
      const updated = await api.getStudySessions(10);
      setSessions(updated);
      setSessionNotes('');
    } catch (err) {
      showToast(err.message || 'Failed to log session', 'error');
    }
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const nodes = roadmap.nodes || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-cyan">Deep Work Hub</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Pomodoro Study Timer & Focus Sessions
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '700px' }}>
          Train with timed Pomodoro cycles to build deep technical focus, retain complex concepts, and earn continuous daily streak rewards.
        </p>
      </div>

      {/* Main Grid Layout */}
      <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '24px' }}>
        {/* Left: Pomodoro Timer Visualizer */}
        <div
          className="glass-panel-elevated"
          style={{
            padding: '36px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '24px',
            background: 'linear-gradient(135deg, rgba(13, 17, 26, 0.95) 0%, rgba(20, 24, 38, 0.95) 100%)',
          }}
        >
          {/* Mode Selector Tabs */}
          <div
            style={{
              display: 'flex',
              background: 'rgba(15, 23, 42, 0.8)',
              padding: '4px',
              borderRadius: '14px',
              border: '1px solid var(--border-subtle)',
            }}
          >
            {Object.entries(MODES).map(([key, mode]) => (
              <button
                key={key}
                type="button"
                onClick={() => switchMode(key)}
                style={{
                  padding: '8px 18px',
                  borderRadius: '10px',
                  border: 'none',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: currentMode === key ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  color: currentMode === key ? '#38bdf8' : 'var(--text-secondary)',
                  transition: 'all 0.2s ease',
                }}
              >
                {mode.label}
              </button>
            ))}
          </div>

          {/* Big Radial Timer Display */}
          <div style={{ position: 'relative', width: '220px', height: '220px' }}>
            <svg style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
              <circle
                cx="110"
                cy="110"
                r="95"
                stroke="rgba(255, 255, 255, 0.06)"
                strokeWidth="12"
                fill="none"
              />
              <circle
                cx="110"
                cy="110"
                r="95"
                stroke={MODES[currentMode].color}
                strokeWidth="12"
                strokeDasharray={597}
                strokeDashoffset={597 - (597 * progressPercent) / 100}
                strokeLinecap="round"
                fill="none"
                style={{ transition: 'stroke-dashoffset 0.5s ease' }}
              />
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
              <span
                style={{
                  fontSize: '3rem',
                  fontWeight: 900,
                  fontFamily: 'var(--font-mono)',
                  letterSpacing: '-0.03em',
                  color: 'var(--text-primary)',
                }}
              >
                {formatTime(timeLeft)}
              </span>
              <span
                style={{
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  textTransform: 'uppercase',
                  color: isRunning ? MODES[currentMode].color : 'var(--text-muted)',
                  marginTop: '2px',
                }}
              >
                {isRunning ? 'Session Active' : 'Paused'}
              </span>
            </div>
          </div>

          {/* Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '14px' }}>
            <button
              type="button"
              onClick={() => {
                setTimeLeft(MODES[currentMode].minutes * 60);
                setIsRunning(false);
              }}
              className="btn-secondary"
              title="Reset Timer"
              style={{ padding: '12px', borderRadius: '50%' }}
            >
              <RotateCcw className="w-5 h-5" />
            </button>

            <button
              type="button"
              onClick={() => setIsRunning(!isRunning)}
              className="btn-primary"
              style={{ padding: '14px 32px', fontSize: '1.05rem', minWidth: '160px' }}
            >
              {isRunning ? (
                <>
                  <Pause className="w-5 h-5" /> Pause
                </>
              ) : (
                <>
                  <Play className="w-5 h-5" /> Start Focus
                </>
              )}
            </button>

            <button
              type="button"
              onClick={() => setTimeLeft(0)}
              className="btn-secondary"
              title="Skip to End"
              style={{ padding: '12px', borderRadius: '50%' }}
            >
              <SkipForward className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Right: Skill Linking & History Logger */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {/* Target Skill Attachment */}
          <form
            onSubmit={handleManualLog}
            className="glass-panel"
            style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '14px' }}
          >
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700 }}>Link Session to Skill DAG Node</h3>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                Active Target Skill
              </label>
              <select
                value={selectedSkillId}
                onChange={(e) => setSelectedSkillId(e.target.value)}
                className="custom-input"
                style={{ cursor: 'pointer' }}
              >
                <option value="">-- Select Skill Being Studied --</option>
                {nodes.map((node) => (
                  <option key={node.skill_id} value={node.skill_id}>
                    {node.skill?.name || `Skill #${node.skill_id}`}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-secondary)', marginBottom: '4px' }}>
                Study Session Notes
              </label>
              <textarea
                rows={3}
                placeholder="What did you build or learn during this focus session?"
                value={sessionNotes}
                onChange={(e) => setSessionNotes(e.target.value)}
                className="custom-textarea"
                style={{ minHeight: '70px', fontSize: '0.85rem' }}
              />
            </div>

            <button
              type="submit"
              className="btn-emerald"
              style={{ width: '100%', padding: '10px', fontSize: '0.88rem' }}
            >
              <Save className="w-4 h-4" /> Log {MODES[currentMode].minutes} Min Focus Session (+XP)
            </button>
          </form>

          {/* Recent History */}
          <div className="glass-panel" style={{ padding: '20px', flex: 1, overflowY: 'auto', maxHeight: '280px' }}>
            <h4 style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: '12px' }}>Recent Focus Sessions</h4>
            {sessions.length === 0 ? (
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', textAlign: 'center', padding: '20px 0' }}>
                No focus sessions logged yet. Complete a Pomodoro cycle to see it recorded here!
              </p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {sessions.map((s) => (
                  <div
                    key={s.id}
                    style={{
                      padding: '10px 14px',
                      borderRadius: '10px',
                      background: 'rgba(255, 255, 255, 0.03)',
                      border: '1px solid var(--border-subtle)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                    }}
                  >
                    <div>
                      <div style={{ fontSize: '0.86rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                        {s.notes || 'Deep Focus Session'}
                      </div>
                      <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                        {new Date(s.session_date).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                    <span className="badge badge-cyan">{s.duration_minutes} mins</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
