import React, { useState } from 'react';
import { useApp } from '../../context/AppContext';
import { X, Plus, Sparkles, Layers, Clock, BookOpen } from 'lucide-react';
import { api } from '../../services/api';

export const AddSkillModal = () => {
  const { isAddSkillModalOpen, setIsAddSkillModalOpen, currentCareer, roadmap, loadRoadmap, showToast } = useApp();
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [whyImportant, setWhyImportant] = useState('');
  const [level, setLevel] = useState('fundamental');
  const [category, setCategory] = useState('technical');
  const [priority, setPriority] = useState('recommended');
  const [estimatedHours, setEstimatedHours] = useState(12);
  const [selectedPrereqs, setSelectedPrereqs] = useState([]);
  const [loading, setLoading] = useState(false);

  if (!isAddSkillModalOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;
    setLoading(true);
    try {
      await api.createCustomSkill({
        career_path_id: currentCareer?.id,
        name: name.trim(),
        description: description.trim(),
        why_important: whyImportant.trim(),
        level,
        category,
        priority,
        estimated_hours: Number(estimatedHours),
        prerequisites: selectedPrereqs,
      });

      showToast(`Custom skill "${name}" added to your roadmap!`, 'success');
      if (currentCareer) {
        await loadRoadmap(currentCareer.id);
      }
      setIsAddSkillModalOpen(false);
      setName('');
      setDescription('');
      setSelectedPrereqs([]);
    } catch (err) {
      showToast(err.message || 'Failed to add custom skill', 'error');
    } finally {
      setLoading(false);
    }
  };

  const togglePrereq = (skillId) => {
    setSelectedPrereqs((prev) =>
      prev.includes(skillId) ? prev.filter((id) => id !== skillId) : [...prev, skillId]
    );
  };

  return (
    <div className="modal-backdrop">
      <div
        className="glass-panel-elevated"
        style={{
          width: '100%',
          maxWidth: '560px',
          maxHeight: '90vh',
          overflowY: 'auto',
          padding: '30px',
          position: 'relative',
          background: 'rgba(13, 17, 26, 0.96)',
        }}
      >
        <button
          onClick={() => setIsAddSkillModalOpen(false)}
          style={{
            position: 'absolute',
            top: '20px',
            right: '20px',
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

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '20px' }}>
          <div
            style={{
              padding: '10px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.2), rgba(99, 102, 241, 0.2))',
              border: '1px solid rgba(56, 189, 248, 0.3)',
            }}
          >
            <Plus className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700 }}>Add Custom Skill to Roadmap</h2>
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.84rem' }}>
              Expand your DAG with new tools, frameworks, or niche topics.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
              Skill Name *
            </label>
            <input
              type="text"
              required
              placeholder="e.g. LangChain, Kubernetes Operators, CUDA..."
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="custom-input"
            />
          </div>

          <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Level
              </label>
              <select
                value={level}
                onChange={(e) => setLevel(e.target.value)}
                className="custom-input"
                style={{ cursor: 'pointer' }}
              >
                <option value="fundamental">Fundamental</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="mastery">Mastery</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="custom-input"
                style={{ cursor: 'pointer' }}
              >
                <option value="technical">Technical</option>
                <option value="core">Core Architecture</option>
                <option value="tools">Tools & DevOps</option>
                <option value="math">Mathematics & Logic</option>
                <option value="soft">Soft Skills</option>
              </select>
            </div>
          </div>

          <div className="resp-collapse" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Priority
              </label>
              <select
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="custom-input"
                style={{ cursor: 'pointer' }}
              >
                <option value="required">Required / Core</option>
                <option value="recommended">Recommended</option>
                <option value="optional">Optional / Niche</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
                Estimated Study Hours
              </label>
              <input
                type="number"
                min="1"
                max="200"
                value={estimatedHours}
                onChange={(e) => setEstimatedHours(e.target.value)}
                className="custom-input"
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
              Description & Objectives
            </label>
            <textarea
              placeholder="What will you learn and build with this skill?"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="custom-textarea"
              style={{ minHeight: '70px' }}
            />
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '6px', fontWeight: 500 }}>
              Prerequisites (Select skills that must be mastered first)
            </label>
            <div
              style={{
                maxHeight: '140px',
                overflowY: 'auto',
                padding: '8px',
                borderRadius: '12px',
                background: 'rgba(15, 23, 42, 0.6)',
                border: '1px solid var(--border-subtle)',
                display: 'flex',
                flexWrap: 'wrap',
                gap: '6px',
              }}
            >
              {(roadmap.nodes || []).map((node) => {
                const s = node.skill || {};
                const isSelected = selectedPrereqs.includes(s.id);
                return (
                  <button
                    key={node.id}
                    type="button"
                    onClick={() => togglePrereq(s.id)}
                    style={{
                      padding: '4px 10px',
                      borderRadius: '8px',
                      fontSize: '0.78rem',
                      fontWeight: 500,
                      cursor: 'pointer',
                      border: isSelected ? '1px solid #38bdf8' : '1px solid var(--border-subtle)',
                      background: isSelected ? 'rgba(56, 189, 248, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                      color: isSelected ? '#38bdf8' : 'var(--text-secondary)',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    {isSelected ? '✓ ' : '+ '}
                    {s.name}
                  </button>
                );
              })}
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn-primary"
            style={{ width: '100%', padding: '12px', marginTop: '6px' }}
          >
            {loading ? 'Adding Node to DAG...' : '✨ Insert Node into Roadmap DAG'}
          </button>
        </form>
      </div>
    </div>
  );
};
