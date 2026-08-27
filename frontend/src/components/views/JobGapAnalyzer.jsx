import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import {
  Briefcase,
  Sparkles,
  Search,
  CheckCircle,
  AlertCircle,
  Plus,
  ArrowRight,
  Building,
  MapPin,
  Clock,
  Layers,
  Zap,
} from 'lucide-react';
import { api } from '../../services/api';

const PRESET_JOBS = [
  {
    title: 'Senior AI/ML Engineer',
    company: 'Anthropic / OpenAI Ecosystem',
    location: 'San Francisco, CA / Remote',
    raw_text: `We are seeking a Senior AI/ML Engineer to train, fine-tune, and deploy state-of-the-art Large Language Models.
Requirements:
- 4+ years of production experience in Python, PyTorch, and Deep Learning.
- Deep expertise with Transformers, Attention Mechanisms, and Hugging Face.
- Hands-on experience with Vector Databases (Pinecone, Chroma), RAG architectures, and LangChain.
- Strong knowledge of MLOps pipelines (MLflow, Triton, Docker, Kubernetes).
- Familiarity with RLHF, LoRA/PEFT, model quantization, and CUDA optimization.
- Bachelor's or Master's degree in Computer Science or related STEM field.`,
  },
  {
    title: 'Staff Full Stack Developer',
    company: 'Stripe / Fintech Scale-up',
    location: 'New York, NY / Remote',
    raw_text: `Looking for a Staff Full Stack Developer to lead our next-generation payment interfaces and distributed microservices.
Requirements:
- 5+ years of software engineering experience with TypeScript, React, and Node.js.
- Strong expertise with Next.js, Server Components, and Tailwind CSS.
- Deep database mastery in PostgreSQL, indexing, query optimization, and Redis caching.
- Experience architecting RESTful and GraphQL APIs, Docker containers, and CI/CD pipelines.
- Solid understanding of WebSockets, system design, authentication protocols (OAuth2/JWT), and microservices.`,
  },
  {
    title: 'Cloud DevOps & Platform Engineer',
    company: 'Amazon Web Services / Cloud Native',
    location: 'Seattle, WA / Hybrid',
    raw_text: `Join our Cloud Platform Infrastructure team building resilient multi-region architectures.
Requirements:
- Proven experience with Linux systems, Bash scripting, and Python automation.
- Production mastery of Docker containerization and Kubernetes (EKS/GKE) orchestration.
- Infrastructure as Code (IaC) with Terraform, CloudFormation, and Ansible.
- Strong knowledge of AWS cloud architecture (VPC, IAM, ECS, S3, RDS).
- CI/CD automation with GitHub Actions, ArgoCD, and Helm.
- Observability and monitoring with Prometheus, Grafana, and OpenTelemetry.`,
  },
];

export const JobGapAnalyzer = () => {
  const { user, openSkillDrawer, showToast, setIsAuthModalOpen } = useApp();
  const [jobTitle, setJobTitle] = useState(PRESET_JOBS[0].title);
  const [company, setCompany] = useState(PRESET_JOBS[0].company);
  const [location, setLocation] = useState(PRESET_JOBS[0].location);
  const [rawText, setRawText] = useState(PRESET_JOBS[0].raw_text);
  const [loading, setLoading] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!rawText.trim()) return;
    if (!user) {
      setIsAuthModalOpen(true);
      return;
    }
    setLoading(true);
    try {
      const res = await api.analyzeJob({
        title: jobTitle,
        company,
        location,
        raw_text: rawText,
        save: true,
      });
      setAnalysisResult(res);
      showToast(`Analysis complete! Match score: ${res.match_score}%`, 'success');
    } catch (err) {
      showToast(err.message || 'Job analysis failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  const loadPreset = (preset) => {
    setJobTitle(preset.title);
    setCompany(preset.company);
    setLocation(preset.location);
    setRawText(preset.raw_text);
    setAnalysisResult(null);
  };

  const matchedItems = analysisResult?.gap_items?.filter((g) => g.user_status === 'completed' || g.user_status === 'in_progress') || [];
  const missingItems = analysisResult?.gap_items?.filter((g) => g.user_status === 'not_started' || !g.user_status) || [];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-cyan">ATS Skill Gap AI</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Job Description Gap Analyzer
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '700px' }}>
          Paste any software engineering job description to instantly map required skills against your mastered DAG nodes. Identify gaps and bridge them with 1-click roadmap planning.
        </p>
      </div>

      {/* Preset Quick Loaders */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)' }}>Quick Presets:</span>
        {PRESET_JOBS.map((preset, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => loadPreset(preset)}
            style={{
              padding: '6px 14px',
              borderRadius: '10px',
              background: jobTitle === preset.title ? 'rgba(56, 189, 248, 0.2)' : 'rgba(255, 255, 255, 0.04)',
              border: jobTitle === preset.title ? '1px solid #38bdf8' : '1px solid var(--border-subtle)',
              color: jobTitle === preset.title ? '#38bdf8' : 'var(--text-secondary)',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.15s ease',
            }}
          >
            ⚡ {preset.title}
          </button>
        ))}
      </div>

      {/* Main Input & Analysis Layout */}
      <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Left: Input Form */}
        <form
          onSubmit={handleAnalyze}
          className="glass-panel"
          style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '16px' }}
        >
          <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Job Title
              </label>
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g. Senior Machine Learning Engineer"
                className="custom-input"
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Company Name
              </label>
              <input
                type="text"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                placeholder="e.g. Google, Anthropic, Stripe"
                className="custom-input"
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
              Job Description / Requirements *
            </label>
            <textarea
              required
              rows={10}
              value={rawText}
              onChange={(e) => setRawText(e.target.value)}
              placeholder="Paste the full job posting requirements and tech stack here..."
              className="custom-textarea"
              style={{ minHeight: '220px', fontFamily: 'var(--font-mono)', fontSize: '0.85rem' }}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: '100%', padding: '12px', fontSize: '0.95rem' }}
          >
            {loading ? 'Analyzing Tech Vocabulary & Skill Gaps...' : '🔍 Analyze Job Description Gaps'}
          </button>
        </form>

        {/* Right: Results Display */}
        <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
          {!analysisResult ? (
            <div
              style={{
                flex: 1,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center',
                padding: '40px 20px',
                color: 'var(--text-muted)',
              }}
            >
              <Briefcase className="w-12 h-12 mb-3 opacity-30 text-cyan-400" />
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>
                Awaiting Job Description
              </h3>
              <p style={{ fontSize: '0.85rem', maxWidth: '340px' }}>
                Paste a job posting and click analyze to see match percentage, mastered competencies, and missing skill gaps.
              </p>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {/* Score Header */}
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '16px 20px',
                  borderRadius: '16px',
                  background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(99, 102, 241, 0.1))',
                  border: '1px solid rgba(56, 189, 248, 0.3)',
                }}
              >
                <div>
                  <h3 style={{ fontSize: '1.2rem', fontWeight: 800 }}>{jobTitle}</h3>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '2px' }}>
                    <Building className="w-3.5 h-3.5" /> {company}
                  </div>
                </div>

                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '1.8rem', fontWeight: 900, color: analysisResult.match_score > 70 ? '#34d399' : '#fbbf24' }}>
                    {analysisResult.match_score}%
                  </div>
                  <span style={{ fontSize: '0.72rem', textTransform: 'uppercase', fontWeight: 700, color: 'var(--text-muted)' }}>
                    Match Score
                  </span>
                </div>
              </div>

              {/* Matched Skills (Green) */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#34d399', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                  <CheckCircle className="w-4 h-4" /> Matched Skills ({matchedItems.length})
                </h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {matchedItems.length === 0 ? (
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>No direct matches yet.</span>
                  ) : (
                    matchedItems.map((item, idx) => (
                      <span
                        key={idx}
                        className="badge badge-emerald"
                        style={{ padding: '5px 12px', fontSize: '0.8rem', cursor: 'pointer' }}
                        onClick={() => item.matched_skill_id && openSkillDrawer(item.matched_skill_id)}
                      >
                        ✓ {item.display_name}
                      </span>
                    ))
                  )}
                </div>
              </div>

              {/* Missing Skills Gap (Orange/Red) */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: '#fbbf24', display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '8px' }}>
                  <AlertCircle className="w-4 h-4" /> Missing Skill Gaps ({missingItems.length})
                </h4>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                  {missingItems.length === 0 ? (
                    <span style={{ fontSize: '0.8rem', color: '#34d399' }}>100% Skill coverage achieved!</span>
                  ) : (
                    missingItems.map((item, idx) => (
                      <button
                        key={idx}
                        onClick={() => item.matched_skill_id && openSkillDrawer(item.matched_skill_id)}
                        className="badge badge-amber"
                        style={{ padding: '6px 12px', fontSize: '0.8rem', cursor: 'pointer', border: '1px solid rgba(245, 158, 11, 0.4)' }}
                      >
                        + {item.display_name} ({item.estimated_hours || 10}h)
                      </button>
                    ))
                  )}
                </div>
              </div>

              {/* Parsed Meta (Experience & Education) */}
              {analysisResult.parsed_meta && (
                <div
                  style={{
                    padding: '14px',
                    borderRadius: '12px',
                    background: 'rgba(255, 255, 255, 0.03)',
                    border: '1px solid var(--border-subtle)',
                    fontSize: '0.82rem',
                    color: 'var(--text-secondary)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '6px',
                  }}
                >
                  {analysisResult.parsed_meta.years_experience && (
                    <div><strong>Required Experience:</strong> {analysisResult.parsed_meta.years_experience} years</div>
                  )}
                  {analysisResult.parsed_meta.education && (
                    <div><strong>Education:</strong> {analysisResult.parsed_meta.education}</div>
                  )}
                  {analysisResult.parsed_meta.soft_skills && analysisResult.parsed_meta.soft_skills.length > 0 && (
                    <div><strong>Soft Skills:</strong> {analysisResult.parsed_meta.soft_skills.join(', ')}</div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
