import React, { useState, useMemo, useRef } from 'react';
import { useApp } from '../../context/AppContext';
import {
  ZoomIn,
  ZoomOut,
  RotateCcw,
  Maximize2,
  Filter,
  Search,
  Plus,
  CheckCircle2,
  Lock,
  Sparkles,
  Layers,
  Clock,
  Award,
  ChevronRight,
  TrendingUp,
  Flame,
} from 'lucide-react';

export const SkillDAGRoadmap = () => {
  const {
    currentCareer,
    roadmap,
    openSkillDrawer,
    setIsAddSkillModalOpen,
    user,
    setIsAuthModalOpen,
  } = useApp();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [zoomLevel, setZoomLevel] = useState(1);
  const [panOffset, setPanOffset] = useState({ x: 40, y: 30 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });

  const containerRef = useRef(null);

  const nodes = roadmap.nodes || [];
  const edges = roadmap.edges || [];

  // Group nodes by layer
  const layers = useMemo(() => {
    const map = {};
    nodes.forEach((node) => {
      const l = node.layer !== undefined ? node.layer : 0;
      if (!map[l]) map[l] = [];
      map[l].push(node);
    });
    return map;
  }, [nodes]);

  const layerIndices = useMemo(() => {
    return Object.keys(layers).map(Number).sort((a, b) => a - b);
  }, [layers]);

  // Node position map
  const nodeMap = useMemo(() => {
    const map = {};
    nodes.forEach((n) => {
      map[n.skill_id] = n;
    });
    return map;
  }, [nodes]);

  // Statistics
  const stats = useMemo(() => {
    let mastered = 0;
    let inProgress = 0;
    let totalHours = 0;
    nodes.forEach((n) => {
      if (n.user_status === 'completed') mastered++;
      else if (n.user_status === 'in_progress') inProgress++;
      totalHours += n.skill?.estimated_hours || 10;
    });
    const percent = nodes.length > 0 ? Math.round((mastered / nodes.length) * 100) : 0;
    return { mastered, inProgress, total: nodes.length, percent, totalHours };
  }, [nodes]);

  // Filtered nodes for search/category
  const filteredNodeIds = useMemo(() => {
    const set = new Set();
    nodes.forEach((n) => {
      const s = n.skill || {};
      const matchesSearch =
        !searchQuery ||
        s.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        s.description?.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesCat =
        selectedCategory === 'all' || s.category?.toLowerCase() === selectedCategory.toLowerCase();
      const matchesStatus =
        selectedStatus === 'all' ||
        (selectedStatus === 'completed' && n.user_status === 'completed') ||
        (selectedStatus === 'in_progress' && n.user_status === 'in_progress') ||
        (selectedStatus === 'not_started' && (!n.user_status || n.user_status === 'not_started'));

      if (matchesSearch && matchesCat && matchesStatus) {
        set.add(n.skill_id);
      }
    });
    return set;
  }, [nodes, searchQuery, selectedCategory, selectedStatus]);

  // Pan & Zoom handlers
  const handleMouseDown = (e) => {
    if (e.target.closest('.dag-node-interactive') || e.target.closest('button')) return;
    setIsDragging(true);
    setDragStart({ x: e.clientX - panOffset.x, y: e.clientY - panOffset.y });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPanOffset({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  // Touch support for mobile panning
  const handleTouchStart = (e) => {
    const t = e.touches[0];
    if (!t) return;
    if (e.target.closest('.dag-node-interactive') || e.target.closest('button')) return;
    setIsDragging(true);
    setDragStart({ x: t.clientX - panOffset.x, y: t.clientY - panOffset.y });
  };

  const handleTouchMove = (e) => {
    if (!isDragging) return;
    const t = e.touches[0];
    if (!t) return;
    e.preventDefault();
    setPanOffset({
      x: t.clientX - dragStart.x,
      y: t.clientY - dragStart.y,
    });
  };

  const handleTouchEnd = () => {
    setIsDragging(false);
  };

  const handleZoom = (delta) => {
    setZoomLevel((prev) => Math.min(Math.max(prev + delta, 0.5), 1.8));
  };

  const handleResetView = () => {
    setZoomLevel(1);
    setPanOffset({ x: 40, y: 30 });
  };

  const getLayerTitle = (index) => {
    const titles = [
      'Layer 1: Foundations & Core Tooling',
      'Layer 2: Core Engineering & Systems',
      'Layer 3: Advanced Architectures & Frameworks',
      'Layer 4: Mastery, Scale & Specialization',
      'Layer 5: Enterprise Production & Leadership',
    ];
    return titles[index] || `Layer ${index + 1}: Specialization`;
  };

  // Node coordinates calculation
  const LAYER_WIDTH = 290;
  const NODE_HEIGHT = 100;
  const NODE_SPACING_Y = 24;

  const nodeCoordinates = useMemo(() => {
    const coords = {};
    layerIndices.forEach((layerIdx, colIdx) => {
      const layerNodes = layers[layerIdx] || [];
      layerNodes.forEach((node, rowIdx) => {
        const x = colIdx * (LAYER_WIDTH + 80) + 60;
        const y = rowIdx * (NODE_HEIGHT + NODE_SPACING_Y) + 70;
        coords[node.skill_id] = { x, y, colIdx, rowIdx };
      });
    });
    return coords;
  }, [layerIndices, layers]);

  const maxCanvasWidth = Math.max(layerIndices.length * (LAYER_WIDTH + 80) + 200, 1200);
  const maxNodesInAnyLayer = Math.max(...Object.values(layers).map((l) => l.length), 4);
  const maxCanvasHeight = Math.max(maxNodesInAnyLayer * (NODE_HEIGHT + NODE_SPACING_Y) + 180, 750);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 84px)', gap: '16px' }}>
      {/* Top Toolbar & Filter Bar */}
      <div
        className="glass-panel"
        style={{
          padding: '16px 20px',
          display: 'flex',
          flexWrap: 'wrap',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '14px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em' }}>
                {currentCareer?.title || 'Skill DAG Roadmap'}
              </h2>
              <span className="badge badge-cyan">{stats.percent}% Mastered</span>
            </div>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              Directed Acyclic Graph (DAG) of prerequisite skills and mastery checkpoints.
            </p>
          </div>
        </div>

        {/* Stats Pills */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap' }}>
          <div
            style={{
              padding: '6px 14px',
              borderRadius: '10px',
              background: 'rgba(16, 185, 129, 0.1)',
              border: '1px solid rgba(16, 185, 129, 0.25)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '0.82rem',
              fontWeight: 600,
              color: '#34d399',
            }}
          >
            <CheckCircle2 className="w-4 h-4" /> {stats.mastered} Mastered
          </div>

          <div
            style={{
              padding: '6px 14px',
              borderRadius: '10px',
              background: 'rgba(245, 158, 11, 0.1)',
              border: '1px solid rgba(245, 158, 11, 0.25)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '0.82rem',
              fontWeight: 600,
              color: '#fbbf24',
            }}
          >
            <Flame className="w-4 h-4" /> {stats.inProgress} In Progress
          </div>

          <div
            style={{
              padding: '6px 14px',
              borderRadius: '10px',
              background: 'rgba(56, 189, 248, 0.08)',
              border: '1px solid rgba(56, 189, 248, 0.2)',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '0.82rem',
              fontWeight: 600,
              color: '#38bdf8',
            }}
          >
            <Clock className="w-4 h-4" /> {stats.totalHours} Hours Est.
          </div>

          <button
            onClick={() => setIsAddSkillModalOpen(true)}
            className="btn-primary"
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <Plus className="w-4 h-4" /> Add Custom Skill
          </button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '12px',
          flexWrap: 'wrap',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {/* Search box */}
          <div style={{ position: 'relative', width: '220px' }}>
            <input
              type="text"
              placeholder="Search DAG skills..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="custom-input"
              style={{ padding: '8px 12px 8px 34px', fontSize: '0.84rem', borderRadius: '10px' }}
            />
            <Search className="w-4 h-4 text-slate-400" style={{ position: 'absolute', left: '10px', top: '10px' }} />
          </div>

          {/* Status filters */}
          <div style={{ display: 'flex', background: 'rgba(15, 23, 42, 0.6)', padding: '3px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            {['all', 'completed', 'in_progress', 'not_started'].map((st) => (
              <button
                key={st}
                onClick={() => setSelectedStatus(st)}
                style={{
                  padding: '5px 12px',
                  borderRadius: '7px',
                  border: 'none',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: selectedStatus === st ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                  color: selectedStatus === st ? '#38bdf8' : 'var(--text-secondary)',
                }}
              >
                {st === 'all' ? 'All' : st === 'completed' ? 'Mastered' : st === 'in_progress' ? 'Active' : 'Unstarted'}
              </button>
            ))}
          </div>

          {/* Category filter */}
          <div style={{ display: 'flex', background: 'rgba(15, 23, 42, 0.6)', padding: '3px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
            {['all', 'technical', 'core', 'tools'].map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                style={{
                  padding: '5px 12px',
                  borderRadius: '7px',
                  border: 'none',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  background: selectedCategory === cat ? 'rgba(168, 85, 247, 0.2)' : 'transparent',
                  color: selectedCategory === cat ? '#c084fc' : 'var(--text-secondary)',
                }}
              >
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Zoom Controls */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(15, 23, 42, 0.7)', padding: '4px', borderRadius: '10px', border: '1px solid var(--border-subtle)' }}>
          <button
            onClick={() => handleZoom(0.15)}
            title="Zoom In"
            style={{
              padding: '6px',
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              borderRadius: '6px',
              display: 'flex',
            }}
          >
            <ZoomIn className="w-4 h-4" />
          </button>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', minWidth: '40px', textAlign: 'center' }}>
            {Math.round(zoomLevel * 100)}%
          </span>
          <button
            onClick={() => handleZoom(-0.15)}
            title="Zoom Out"
            style={{
              padding: '6px',
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              borderRadius: '6px',
              display: 'flex',
            }}
          >
            <ZoomOut className="w-4 h-4" />
          </button>
          <button
            onClick={handleResetView}
            title="Reset View"
            style={{
              padding: '6px',
              background: 'none',
              border: 'none',
              color: 'var(--text-secondary)',
              cursor: 'pointer',
              borderRadius: '6px',
              display: 'flex',
            }}
          >
            <RotateCcw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* DAG Interactive Canvas Viewport */}
      <div
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onTouchStart={handleTouchStart}
        onTouchMove={handleTouchMove}
        onTouchEnd={handleTouchEnd}
        className="glass-panel"
        style={{
          flex: 1,
          position: 'relative',
          overflow: 'hidden',
          cursor: isDragging ? 'grabbing' : 'grab',
          background: 'rgba(7, 10, 16, 0.9)',
          border: '1px solid rgba(56, 189, 248, 0.18)',
          boxShadow: 'inset 0 0 40px rgba(0, 0, 0, 0.8)',
        }}
      >
        {/* Visual Layer Column Headers */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            transform: `translate(${panOffset.x}px, 0px) scale(${zoomLevel})`,
            transformOrigin: '0 0',
            display: 'flex',
            pointerEvents: 'none',
            zIndex: 2,
          }}
        >
          {layerIndices.map((layerIdx, colIdx) => (
            <div
              key={layerIdx}
              style={{
                width: `${LAYER_WIDTH}px`,
                marginRight: '80px',
                marginLeft: colIdx === 0 ? '60px' : '0',
                paddingTop: '16px',
              }}
            >
              <div
                style={{
                  padding: '6px 12px',
                  borderRadius: '8px',
                  background: 'rgba(15, 23, 42, 0.85)',
                  border: '1px solid var(--border-subtle)',
                  fontSize: '0.76rem',
                  fontWeight: 700,
                  letterSpacing: '0.04em',
                  textTransform: 'uppercase',
                  color: colIdx === 0 ? '#38bdf8' : colIdx === 1 ? '#818cf8' : colIdx === 2 ? '#c084fc' : '#34d399',
                  textAlign: 'center',
                }}
              >
                {getLayerTitle(layerIdx)}
              </div>
            </div>
          ))}
        </div>

        {/* Transform Container for SVG + Nodes */}
        <div
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: `${maxCanvasWidth}px`,
            height: `${maxCanvasHeight}px`,
            transform: `translate(${panOffset.x}px, ${panOffset.y}px) scale(${zoomLevel})`,
            transformOrigin: '0 0',
            transition: isDragging ? 'none' : 'transform 0.05s ease-out',
          }}
        >
          {/* SVG Edges Layer */}
          <svg
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              pointerEvents: 'none',
              zIndex: 1,
            }}
          >
            <defs>
              <linearGradient id="edgeGradDefault" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.4" />
                <stop offset="100%" stopColor="#818cf8" stopOpacity="0.6" />
              </linearGradient>
              <linearGradient id="edgeGradActive" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0%" stopColor="#10b981" stopOpacity="0.7" />
                <stop offset="100%" stopColor="#38bdf8" stopOpacity="0.8" />
              </linearGradient>
            </defs>

            {edges.map((edge) => {
              const src = nodeCoordinates[edge.source_skill_id];
              const tgt = nodeCoordinates[edge.target_skill_id];
              if (!src || !tgt) return null;

              const x1 = src.x + LAYER_WIDTH;
              const y1 = src.y + NODE_HEIGHT / 2;
              const x2 = tgt.x;
              const y2 = tgt.y + NODE_HEIGHT / 2;

              const dx = (x2 - x1) / 2;
              const pathD = `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`;

              const srcNode = nodeMap[edge.source_skill_id];
              const isSourceMastered = srcNode?.user_status === 'completed';

              return (
                <g key={edge.id}>
                  {/* Glowing background line */}
                  <path
                    d={pathD}
                    fill="none"
                    stroke={isSourceMastered ? 'rgba(56, 189, 248, 0.4)' : 'rgba(255, 255, 255, 0.1)'}
                    strokeWidth={isSourceMastered ? '2.5' : '1.5'}
                  />
                  {/* Animated dash flow for active paths */}
                  {isSourceMastered && (
                    <path
                      d={pathD}
                      fill="none"
                      stroke="#38bdf8"
                      strokeWidth="2"
                      className="animate-flow"
                    />
                  )}
                </g>
              );
            })}
          </svg>

          {/* HTML Nodes Layer */}
          <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', zIndex: 3 }}>
            {nodes.map((node) => {
              const coords = nodeCoordinates[node.skill_id];
              if (!coords) return null;

              const skill = node.skill || {};
              const isMatch = filteredNodeIds.has(node.skill_id);
              const isMastered = node.user_status === 'completed';
              const isInProgress = node.user_status === 'in_progress';

              const borderCol = isMastered
                ? 'rgba(16, 185, 129, 0.6)'
                : isInProgress
                ? 'rgba(245, 158, 11, 0.6)'
                : 'rgba(255, 255, 255, 0.12)';

              const bgCol = isMastered
                ? 'rgba(6, 44, 30, 0.85)'
                : isInProgress
                ? 'rgba(45, 30, 8, 0.85)'
                : 'rgba(15, 23, 42, 0.85)';

              return (
                <div
                  key={node.id}
                  onClick={() => openSkillDrawer(node.skill_id)}
                  className={`dag-node dag-node-interactive ${
                    isMastered ? 'dag-node-completed' : isInProgress ? 'dag-node-progress' : ''
                  }`}
                  style={{
                    position: 'absolute',
                    left: `${coords.x}px`,
                    top: `${coords.y}px`,
                    width: `${LAYER_WIDTH}px`,
                    height: `${NODE_HEIGHT}px`,
                    borderRadius: '14px',
                    background: bgCol,
                    border: `1px solid ${borderCol}`,
                    padding: '12px 14px',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    opacity: isMatch ? 1 : 0.25,
                    backdropFilter: 'blur(10px)',
                    boxShadow: isMastered
                      ? '0 0 20px rgba(16, 185, 129, 0.2)'
                      : isInProgress
                      ? '0 0 20px rgba(245, 158, 11, 0.2)'
                      : '0 4px 15px rgba(0, 0, 0, 0.4)',
                    transition: 'all 0.2s cubic-bezier(0.16, 1, 0.3, 1)',
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: '8px' }}>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px' }}>
                        <span
                          style={{
                            fontSize: '0.68rem',
                            fontWeight: 700,
                            textTransform: 'uppercase',
                            color: skill.category === 'core' ? '#c084fc' : skill.category === 'tools' ? '#38bdf8' : '#818cf8',
                          }}
                        >
                          {skill.category || 'Skill'}
                        </span>
                        <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>•</span>
                        <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)' }}>
                          {skill.estimated_hours || 10}h
                        </span>
                      </div>
                      <h4
                        style={{
                          fontSize: '0.92rem',
                          fontWeight: 700,
                          color: 'var(--text-primary)',
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                        }}
                      >
                        {skill.name}
                      </h4>
                    </div>

                    <div>
                      {isMastered ? (
                        <div
                          style={{
                            padding: '4px',
                            borderRadius: '50%',
                            background: 'rgba(16, 185, 129, 0.2)',
                            color: '#34d399',
                            display: 'flex',
                          }}
                        >
                          <CheckCircle2 className="w-4 h-4" />
                        </div>
                      ) : isInProgress ? (
                        <div
                          style={{
                            padding: '4px',
                            borderRadius: '50%',
                            background: 'rgba(245, 158, 11, 0.2)',
                            color: '#fbbf24',
                            display: 'flex',
                          }}
                        >
                          <Flame className="w-4 h-4" />
                        </div>
                      ) : (
                        <div
                          style={{
                            padding: '4px',
                            borderRadius: '50%',
                            background: 'rgba(255, 255, 255, 0.05)',
                            color: '#64748b',
                            display: 'flex',
                          }}
                        >
                          <Lock className="w-3.5 h-3.5" />
                        </div>
                      )}
                    </div>
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', paddingTop: '6px', borderTop: '1px solid rgba(255, 255, 255, 0.06)' }}>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>
                      {skill.priority === 'required' ? '★ Core Required' : 'Recommended'}
                    </span>
                    <span
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        color: isMastered ? '#34d399' : isInProgress ? '#fbbf24' : '#38bdf8',
                      }}
                    >
                      {isMastered ? 'Mastered' : isInProgress ? 'In Progress' : 'Start →'}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};
