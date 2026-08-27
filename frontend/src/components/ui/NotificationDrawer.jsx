import React from 'react';
import { useApp } from '../../context/AppContext';
import { X, Bell, CheckCircle2, Award, Zap, BookOpen, ExternalLink } from 'lucide-react';
import { api } from '../../services/api';

export const NotificationDrawer = () => {
  const {
    isNotificationDrawerOpen,
    setIsNotificationDrawerOpen,
    notifications,
    unreadCount,
    loadNotifications,
    setActiveTab,
    showToast,
  } = useApp();

  if (!isNotificationDrawerOpen) return null;

  const handleMarkAllRead = async () => {
    try {
      await api.markAllNotificationsRead();
      loadNotifications();
      showToast('All notifications marked as read', 'info');
    } catch (e) {
      // ignore
    }
  };

  const handleNotificationClick = async (notif) => {
    try {
      await api.markNotificationRead(notif.id);
      loadNotifications();
    } catch (e) {
      // ignore
    }

    if (notif.link) {
      if (notif.link.includes('roadmap')) setActiveTab('roadmap');
      else if (notif.link.includes('careers')) setActiveTab('careers');
      else if (notif.link.includes('jobs')) setActiveTab('jobs');
      else if (notif.link.includes('interviews')) setActiveTab('interviews');
      else if (notif.link.includes('projects')) setActiveTab('projects');
      setIsNotificationDrawerOpen(false);
    }
  };

  const getIcon = (type) => {
    switch (type) {
      case 'achievement':
        return <Award className="w-5 h-5 text-amber-400" />;
      case 'streak':
        return <Zap className="w-5 h-5 text-rose-400" />;
      case 'study':
        return <BookOpen className="w-5 h-5 text-cyan-400" />;
      default:
        return <Bell className="w-5 h-5 text-indigo-400" />;
    }
  };

  return (
    <div className="modal-backdrop" style={{ justifyContent: 'flex-end', padding: 0 }}>
      <div
        className="glass-panel"
        style={{
          width: '100%',
          maxWidth: '420px',
          height: '100%',
          padding: '24px',
          background: 'rgba(10, 14, 22, 0.95)',
          borderLeft: '1px solid var(--border-subtle)',
          borderRadius: '0',
          display: 'flex',
          flexDirection: 'column',
          boxShadow: '-10px 0 30px rgba(0, 0, 0, 0.7)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Bell className="w-5 h-5 text-cyan-400" />
            <h3 style={{ fontSize: '1.2rem', fontWeight: 700 }}>Notifications</h3>
            {unreadCount > 0 && (
              <span className="badge badge-rose">{unreadCount} new</span>
            )}
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {unreadCount > 0 && (
              <button
                onClick={handleMarkAllRead}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--accent-cyan)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Mark all read
              </button>
            )}
            <button
              onClick={() => setIsNotificationDrawerOpen(false)}
              style={{
                background: 'rgba(255, 255, 255, 0.06)',
                border: 'none',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                padding: '6px',
                borderRadius: '50%',
                display: 'flex',
              }}
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {notifications.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '60px 20px', color: 'var(--text-muted)' }}>
              <Bell className="w-10 h-10 mx-auto mb-3 opacity-30" />
              <p>No notifications yet</p>
              <span style={{ fontSize: '0.8rem' }}>Milestones and alerts will appear here</span>
            </div>
          ) : (
            notifications.map((n) => (
              <div
                key={n.id}
                onClick={() => handleNotificationClick(n)}
                style={{
                  padding: '14px',
                  borderRadius: '12px',
                  background: n.is_read ? 'rgba(255, 255, 255, 0.03)' : 'rgba(56, 189, 248, 0.08)',
                  border: n.is_read ? '1px solid var(--border-subtle)' : '1px solid rgba(56, 189, 248, 0.3)',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  display: 'flex',
                  gap: '12px',
                }}
              >
                <div style={{ marginTop: '2px' }}>{getIcon(n.type)}</div>
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <h4 style={{ fontSize: '0.9rem', fontWeight: 600, color: 'var(--text-primary)', marginBottom: '4px' }}>
                      {n.title}
                    </h4>
                    {!n.is_read && (
                      <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#38bdf8' }} />
                    )}
                  </div>
                  <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                    {n.body}
                  </p>
                  {n.created_at && (
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '6px', display: 'block' }}>
                      {new Date(n.created_at).toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                    </span>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
