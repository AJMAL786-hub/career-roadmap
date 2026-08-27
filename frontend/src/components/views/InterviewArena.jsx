import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Sparkles,
  HelpCircle,
  CheckCircle,
  Clock,
  Play,
  RotateCcw,
  Eye,
  Award,
  ChevronRight,
  Code,
  Lightbulb,
  Search,
  Star,
} from 'lucide-react';
import { api } from '../../services/api';

const CATEGORIES = [
  { id: 'all', label: 'All Categories' },
  { id: 'ml', label: 'Machine Learning & AI' },
  { id: 'system_design', label: 'System Design' },
  { id: 'programming', label: 'Programming & Logic' },
  { id: 'dsa', label: 'Algorithms & DSA' },
  { id: 'cloud', label: 'Cloud & Infrastructure' },
  { id: 'devops', label: 'DevOps & CI/CD' },
  { id: 'cybersecurity', label: 'Security & Auth' },
  { id: 'behavioral', label: 'Behavioral & Leadership' },
];

export const InterviewArena = () => {
  const { currentCareer, user, showToast, setIsAuthModalOpen, triggerConfetti } = useApp();
  const [questions, setQuestions] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [activeQuestion, setActiveQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [showModelAnswer, setShowModelAnswer] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const [timerSeconds, setTimerSeconds] = useState(300);
  const [isTimerRunning, setIsTimerRunning] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchQuestions = async () => {
      setLoading(true);
      try {
        const params = {};
        if (selectedCategory !== 'all') params.category = selectedCategory;
        if (selectedDifficulty !== 'all') params.difficulty = selectedDifficulty;
        if (currentCareer) params.career_id = currentCareer.id;
        const list = await api.getInterviewQuestions(params);
        setQuestions(list);
        if (list.length > 0 && !activeQuestion) {
          setActiveQuestion(list[0]);
        }
      } catch (err) {
        console.warn('Failed to load interview questions', err);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, [selectedCategory, selectedDifficulty, currentCareer]);

  // Timer countdown
  useEffect(() => {
    let interval = null;
    if (isTimerRunning && timerSeconds > 0) {
      interval = setInterval(() => {
        setTimerSeconds((prev) => prev - 1);
      }, 1000);
    } else if (timerSeconds === 0 && isTimerRunning) {
      setIsTimerRunning(false);
      showToast('Time is up! Review your response below.', 'info');
    }
    return () => clearInterval(interval);
  }, [isTimerRunning, timerSeconds]);

  const handleSelectQuestion = (q) => {
    setActiveQuestion(q);
    setUserAnswer('');
    setShowModelAnswer(false);
    setShowHint(false);
    setTimerSeconds(300);
    setIsTimerRunning(false);
  };

  const handleMasterQuestion = async () => {
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    if (!activeQuestion) return;

    try {
      await api.updateInterviewProgress(activeQuestion.id, {
        mastered: true,
        confidence: 5,
      });
      triggerConfetti();
      showToast('Interview Question Mastered! +25 XP', 'success');
      setActiveQuestion((prev) => ({ ...prev, mastered: true }));
    } catch (e) {
      showToast('Mastery progress updated', 'info');
    }
  };

  const formatTime = (secs) => {
    const m = Math.floor(secs / 60);
    const s = secs % 60;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
  };

  const filteredQuestions = questions.filter((q) =>
    !searchQuery ||
    q.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    q.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-purple">AI Interview Simulation</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Technical Interview Practice Arena
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '700px' }}>
          Master 64+ technical, system design, and algorithmic interview questions curated for {currentCareer?.title || 'Tech Careers'}. Test yourself under timed conditions with model rubrics.
        </p>
      </div>

      {/* Category Pills & Search */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', paddingBottom: '4px', maxWidth: '80%' }}>
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              style={{
                padding: '6px 14px',
                borderRadius: '10px',
                border: selectedCategory === cat.id ? '1px solid #c084fc' : '1px solid var(--border-subtle)',
                background: selectedCategory === cat.id ? 'rgba(168, 85, 247, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                color: selectedCategory === cat.id ? '#c084fc' : 'var(--text-secondary)',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer',
                whiteSpace: 'nowrap',
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>

        <div style={{ position: 'relative', width: '220px' }}>
          <input
            type="text"
            placeholder="Search questions..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="custom-input"
            style={{ padding: '8px 12px 8px 34px', fontSize: '0.84rem' }}
          />
          <Search className="w-4 h-4 text-slate-400" style={{ position: 'absolute', left: '10px', top: '10px' }} />
        </div>
      </div>

      {/* Two Column Layout: List on Left, Active Question on Right */}
      <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1.2fr 2fr', gap: '24px' }}>
        {/* Left: Questions List */}
        <div
          className="glass-panel"
          style={{
            padding: '16px',
            maxHeight: '680px',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '4px 8px', color: 'var(--text-muted)', fontSize: '0.78rem', fontWeight: 600 }}>
            <span>QUESTIONS ({filteredQuestions.length})</span>
            <span>DIFFICULTY</span>
          </div>

          {filteredQuestions.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '40px 10px', color: 'var(--text-muted)' }}>
              No questions found for this category.
            </div>
          ) : (
            filteredQuestions.map((q) => {
              const isSelected = activeQuestion?.id === q.id;
              return (
                <div
                  key={q.id}
                  onClick={() => handleSelectQuestion(q)}
                  style={{
                    padding: '14px',
                    borderRadius: '12px',
                    background: isSelected ? 'rgba(168, 85, 247, 0.12)' : 'rgba(255, 255, 255, 0.02)',
                    border: isSelected ? '1px solid #c084fc' : '1px solid var(--border-subtle)',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                  className="hover:border-purple-400/40"
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '8px' }}>
                    <h4 style={{ fontSize: '0.88rem', fontWeight: 600, color: 'var(--text-primary)', lineHeight: 1.4 }}>
                      {q.question}
                    </h4>
                    <span className={`badge ${q.difficulty === 'advanced' ? 'badge-rose' : q.difficulty === 'intermediate' ? 'badge-amber' : 'badge-cyan'}`}>
                      {q.difficulty}
                    </span>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: '8px' }}>
                    <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)', textTransform: 'capitalize' }}>
                      {q.category?.replace('_', ' ')}
                    </span>
                    {q.mastered && (
                      <span style={{ fontSize: '0.74rem', color: '#34d399', display: 'flex', alignItems: 'center', gap: '3px' }}>
                        <CheckCircle className="w-3.5 h-3.5" /> Mastered
                      </span>
                    )}
                  </div>
                </div>
              );
            })
          )}
        </div>

        {/* Right: Active Question Arena */}
        <div className="glass-panel" style={{ padding: '28px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          {activeQuestion ? (
            <>
              {/* Question Header */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                    <span className="badge badge-purple">{activeQuestion.category?.replace('_', ' ')}</span>
                    <span className="badge badge-cyan">{activeQuestion.difficulty}</span>
                    {activeQuestion.company && (
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        Frequently asked at <strong>{activeQuestion.company}</strong>
                      </span>
                    )}
                  </div>
                  <h2 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', lineHeight: 1.4 }}>
                    {activeQuestion.question}
                  </h2>
                </div>

                {/* Timer Controls */}
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '8px',
                    padding: '8px 14px',
                    borderRadius: '12px',
                    background: isTimerRunning ? 'rgba(244, 63, 94, 0.15)' : 'rgba(255, 255, 255, 0.05)',
                    border: isTimerRunning ? '1px solid rgba(244, 63, 94, 0.4)' : '1px solid var(--border-subtle)',
                  }}
                >
                  <Clock className={`w-4 h-4 ${isTimerRunning ? 'text-rose-400 animate-pulse' : 'text-slate-400'}`} />
                  <span style={{ fontSize: '1rem', fontWeight: 700, fontFamily: 'var(--font-mono)' }}>
                    {formatTime(timerSeconds)}
                  </span>
                  <button
                    type="button"
                    onClick={() => setIsTimerRunning(!isTimerRunning)}
                    style={{
                      background: 'none',
                      border: 'none',
                      color: isTimerRunning ? '#fb7185' : '#38bdf8',
                      cursor: 'pointer',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                    }}
                  >
                    {isTimerRunning ? 'PAUSE' : 'START'}
                  </button>
                </div>
              </div>

              {/* Your Answer Area */}
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 600 }}>
                  Your Structured Response / Code Solution
                </label>
                <textarea
                  rows={6}
                  placeholder="Structure your thought process: 1. Core Principles, 2. Trade-offs, 3. Implementation/Code, 4. Edge Cases..."
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  className="custom-textarea"
                  style={{ minHeight: '140px', fontFamily: 'var(--font-mono)', fontSize: '0.88rem' }}
                />
              </div>

              {/* Action Toolbar */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '10px' }}>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    type="button"
                    onClick={() => setShowHint(!showHint)}
                    className="btn-secondary"
                    style={{ fontSize: '0.82rem', padding: '8px 14px' }}
                  >
                    <Lightbulb className="w-4 h-4 text-amber-400" />
                    {showHint ? 'Hide Hint' : 'Get Hint'}
                  </button>

                  <button
                    type="button"
                    onClick={() => setShowModelAnswer(!showModelAnswer)}
                    className="btn-secondary"
                    style={{ fontSize: '0.82rem', padding: '8px 14px' }}
                  >
                    <Eye className="w-4 h-4 text-cyan-400" />
                    {showModelAnswer ? 'Hide Solution' : 'Reveal Model Answer'}
                  </button>
                </div>

                <button
                  type="button"
                  onClick={handleMasterQuestion}
                  className="btn-emerald"
                  style={{ fontSize: '0.85rem', padding: '8px 18px' }}
                >
                  <Award className="w-4 h-4" /> Mark Mastered (+25 XP)
                </button>
              </div>

              {/* Hint Box */}
              {showHint && (
                <div
                  style={{
                    padding: '14px',
                    borderRadius: '12px',
                    background: 'rgba(245, 158, 11, 0.08)',
                    border: '1px solid rgba(245, 158, 11, 0.3)',
                    color: '#fbbf24',
                    fontSize: '0.85rem',
                  }}
                >
                  💡 <strong>Interviewer Hint:</strong> Focus on scalability, algorithmic complexity, and error-handling in production systems.
                </div>
              )}

              {/* Official Model Answer & Rubric */}
              {showModelAnswer && (
                <div
                  style={{
                    padding: '18px',
                    borderRadius: '14px',
                    background: 'rgba(15, 23, 42, 0.85)',
                    border: '1px solid rgba(56, 189, 248, 0.3)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#38bdf8', fontWeight: 700, fontSize: '0.88rem', marginBottom: '10px' }}>
                    <Sparkles className="w-4 h-4" /> Comprehensive Model Solution & Rubric
                  </div>
                  <div
                    style={{
                      fontSize: '0.9rem',
                      color: 'var(--text-primary)',
                      lineHeight: 1.6,
                      whiteSpace: 'pre-wrap',
                      fontFamily: 'var(--font-mono)',
                    }}
                  >
                    {activeQuestion.answer || 'Standard industry answer applying SOLID and distributed systems principles.'}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              Select an interview question from the left to start practicing.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
