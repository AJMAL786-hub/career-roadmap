import React, { useState, useEffect } from 'react';
import { useApp } from '../../context/AppContext';
import {
  BookOpen,
  Video,
  FileText,
  Bookmark,
  ExternalLink,
  Search,
  Sparkles,
  Filter,
  CheckCircle,
} from 'lucide-react';
import { api } from '../../services/api';

const TYPES = [
  { id: 'all', label: 'All Resources' },
  { id: 'docs', label: 'Documentation' },
  { id: 'video', label: 'Video Courses' },
  { id: 'course', label: 'Interactive Courses' },
  { id: 'book', label: 'Books' },
  { id: 'tutorial', label: 'Tutorials' },
];

export const ResourcesView = () => {
  const { currentCareer } = useApp();
  const [resources, setResources] = useState([]);
  const [selectedType, setSelectedType] = useState('all');
  const [isFreeFilter, setIsFreeFilter] = useState('all'); // 'all' | 'free' | 'paid'
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchResources = async () => {
      setLoading(true);
      try {
        const params = {};
        if (selectedType !== 'all') params.resource_type = selectedType;
        if (isFreeFilter === 'free') params.is_free = true;
        if (isFreeFilter === 'paid') params.is_free = false;
        if (currentCareer) params.career_id = currentCareer.id;
        const list = await api.getResources(params);
        setResources(list);
      } catch (e) {
        console.warn('Failed to load resources', e);
      } finally {
        setLoading(false);
      }
    };
    fetchResources();
  }, [currentCareer, selectedType, isFreeFilter]);

  const filtered = resources.filter((r) =>
    !searchQuery ||
    r.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.platform?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    r.description?.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const getIcon = (type) => {
    switch (type) {
      case 'video':
        return <Video className="w-5 h-5 text-rose-400" />;
      case 'book':
        return <Bookmark className="w-5 h-5 text-amber-400" />;
      case 'docs':
      case 'tutorial':
        return <FileText className="w-5 h-5 text-cyan-400" />;
      default:
        return <BookOpen className="w-5 h-5 text-indigo-400" />;
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingBottom: '40px' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
          <span className="badge badge-cyan">Curated Directory</span>
        </div>
        <h1 style={{ fontSize: '1.9rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
          Learning Resources & Deep Dives
        </h1>
        <p style={{ color: 'var(--text-secondary)', fontSize: '0.95rem', maxWidth: '700px' }}>
          High-yield books, official documentation, interactive courses, and video walkthroughs aligned with {currentCareer?.title || 'Tech Engineering'}.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '12px', flexWrap: 'wrap' }}>
        <div style={{ display: 'flex', gap: '6px', overflowX: 'auto', paddingBottom: '4px' }}>
          {TYPES.map((t) => (
            <button
              key={t.id}
              onClick={() => setSelectedType(t.id)}
              style={{
                padding: '6px 14px',
                borderRadius: '10px',
                border: selectedType === t.id ? '1px solid #38bdf8' : '1px solid var(--border-subtle)',
                background: selectedType === t.id ? 'rgba(56, 189, 248, 0.2)' : 'rgba(255, 255, 255, 0.03)',
                color: selectedType === t.id ? '#38bdf8' : 'var(--text-secondary)',
                fontSize: '0.8rem',
                fontWeight: 600,
                cursor: 'pointer',
                whiteSpace: 'nowrap',
              }}
            >
              {t.label}
            </button>
          ))}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ display: 'flex', background: 'rgba(15, 23, 42, 0.6)', padding: '3px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            {['all', 'free', 'paid'].map((f) => (
              <button
                key={f}
                onClick={() => setIsFreeFilter(f)}
                style={{
                  padding: '5px 12px',
                  borderRadius: '7px',
                  border: 'none',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: isFreeFilter === f ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  color: isFreeFilter === f ? '#38bdf8' : 'var(--text-secondary)',
                  textTransform: 'capitalize',
                }}
              >
                {f}
              </button>
            ))}
          </div>

          <div style={{ position: 'relative', width: '220px' }}>
            <input
              type="text"
              placeholder="Search resources..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="custom-input"
              style={{ padding: '8px 12px 8px 34px', fontSize: '0.84rem' }}
            />
            <Search className="w-4 h-4 text-slate-400" style={{ position: 'absolute', left: '10px', top: '10px' }} />
          </div>
        </div>
      </div>

      {/* Resources Cards Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
        {filtered.length === 0 ? (
          <div style={{ gridColumn: '1 / -1', textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
            No resources match the selected filters.
          </div>
        ) : (
          filtered.map((res) => (
            <a
              key={res.id}
              href={res.url}
              target="_blank"
              rel="noopener noreferrer"
              className="glass-panel hover:border-cyan-400/40"
              style={{
                padding: '20px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '14px',
                textDecoration: 'none',
                transition: 'all 0.2s ease',
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
                  <div style={{ padding: '8px', borderRadius: '10px', background: 'rgba(255, 255, 255, 0.05)' }}>
                    {getIcon(res.resource_type)}
                  </div>
                  <span className={`badge ${res.is_free ? 'badge-emerald' : 'badge-amber'}`}>
                    {res.is_free ? 'Free Resource' : 'Paid / Book'}
                  </span>
                </div>

                <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '4px' }}>
                  {res.title}
                </h3>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                  {res.description || 'Comprehensive learning guide for production software engineers.'}
                </p>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '10px', borderTop: '1px solid var(--border-subtle)', fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                <span style={{ fontWeight: 600, color: 'var(--text-secondary)' }}>{res.platform || 'Documentation'}</span>
                <span style={{ color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '4px', fontWeight: 600 }}>
                  Open Link <ExternalLink className="w-3.5 h-3.5" />
                </span>
              </div>
            </a>
          ))
        )}
      </div>
    </div>
  );
};
