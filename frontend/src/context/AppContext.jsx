import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { api } from '../services/api';
import confetti from 'canvas-confetti';

const AppContext = createContext();

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }) => {
  const [theme] = useState('dark');
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [careers, setCareers] = useState([]);
  const [currentCareer, setCurrentCareer] = useState(null);
  const [roadmap, setRoadmap] = useState({ nodes: [], edges: [] });
  const [dashboardData, setDashboardData] = useState(null);
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [selectedSkillId, setSelectedSkillId] = useState(null);
  const [isSkillDrawerOpen, setIsSkillDrawerOpen] = useState(false);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isNotificationDrawerOpen, setIsNotificationDrawerOpen] = useState(false);
  const [isAddSkillModalOpen, setIsAddSkillModalOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [toastMessage, setToastMessage] = useState(null);
  const idleTimerRef = useRef(null);
  const refreshTimerRef = useRef(null);
  const userRef = useRef(null);
  const logoutRef = useRef(null);
  const showToastRef = useRef(null);

  const showToast = (message, type = 'info') => {
    setToastMessage({ message, type, id: Date.now() });
    setTimeout(() => {
      setToastMessage((prev) => (prev?.message === message ? null : prev));
    }, 4000);
  };
  showToastRef.current = showToast;

  const triggerConfetti = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#34d399', '#22d3ee', '#a78bfa', '#fbbf24', '#f472b6'],
    });
  };

  // Fetch initial careers
  const loadCareers = useCallback(async () => {
    try {
      const data = await api.getCareers();
      setCareers(data);
      return data;
    } catch (err) {
      console.warn('Failed to load careers from API', err);
      return [];
    }
  }, []);

  // Fetch roadmap for a career
  const loadRoadmap = useCallback(async (careerId) => {
    if (!careerId) return;
    try {
      const data = await api.getRoadmap(careerId);
      setRoadmap(data);
      if (data.career_path) {
        setCurrentCareer(data.career_path);
      }
    } catch (err) {
      console.warn('Failed to load roadmap', err);
    }
  }, []);

  // Fetch dashboard stats
  const loadDashboard = useCallback(async () => {
    if (!user) return;
    try {
      const data = await api.getDashboard();
      setDashboardData(data);
    } catch (err) {
      console.warn('Failed to load dashboard', err);
    }
  }, [user]);

  // Fetch notifications
  const loadNotifications = useCallback(async () => {
    if (!user) return;
    try {
      const list = await api.getNotifications();
      setNotifications(list);
      const countRes = await api.getUnreadCount();
      setUnreadCount(countRes.count || 0);
    } catch (err) {
      console.warn('Failed to load notifications', err);
    }
  }, [user]);

  // Refresh current user profile from the authenticated session.
  const refreshUser = useCallback(async (userData) => {
    if (userData) {
      userRef.current = userData;
      setUser(userData);
      return userData;
    }
    try {
      const data = await api.getMe();
      userRef.current = data;
      setUser(data);
      return data;
    } catch (err) {
      userRef.current = null;
      setUser(null);
      return null;
    }
  }, []);

  // Attempt to mint a fresh access token from the refresh cookie.
  const refreshSession = useCallback(async () => {
    try {
      const userData = await api.refresh();
      userRef.current = userData;
      setUser(userData);
      return userData;
    } catch (err) {
      userRef.current = null;
      setUser(null);
      return null;
    }
  }, []);

  // Login handler — `remember` gates whether the refresh token persists on disk.
  // The raw password is NEVER stored; the backend keeps it only as a bcrypt hash.
  const login = async (email, password, remember) => {
    try {
      const res = await api.login({ email, password, remember });
      userRef.current = res;
      setUser(res);
      showToast(`Welcome back, ${res.full_name || res.username}!`, 'success');
      setIsAuthModalOpen(false);
      restoreActiveSession(res);
      return res;
    } catch (err) {
      throw err;
    }
  };

  // Register handler — automatically starts an authenticated session.
  const register = async (userData) => {
    try {
      const res = await api.register(userData);
      userRef.current = res;
      setUser(res);
      showToast(`Account created! Welcome, ${res.full_name}!`, 'success');
      setIsAuthModalOpen(false);
      restoreActiveSession(res);
      return res;
    } catch (err) {
      throw err;
    }
  };

  // End the session: clear backend cookies then local state.
  const logout = async () => {
    userRef.current = null;
    await api.logout();
    setUser(null);
    setDashboardData(null);
    setNotifications([]);
    setUnreadCount(0);
    stopSessionTimers();
    showToast('Signed out successfully', 'info');
  };
  logoutRef.current = logout;

  // On successful auth, (re)hydrate career/dashboard state and arm session timers.
  const restoreActiveSession = useCallback((activeUser) => {
    const targetCareer =
      careers.find((c) => c.id === activeUser.selected_career_id) || careers[0];
    if (targetCareer) {
      setCurrentCareer(targetCareer);
      loadRoadmap(targetCareer.id);
    }
    loadDashboard();
    loadNotifications();
    startSessionTimers();
  }, [careers, loadRoadmap, loadDashboard, loadNotifications]);

  // ---------------------------------------------------------------------------
  // Session timeout & token refresh
  // ---------------------------------------------------------------------------

  // Access tokens are short-lived; silently refresh shortly before they expire.
  const startRefreshLoop = useCallback(() => {
    clearInterval(refreshTimerRef.current);
    const REFRESH_INTERVAL_MS = 20 * 60 * 1000; // 20 min (< 30 min access TTL)
    refreshTimerRef.current = setInterval(async () => {
      await refreshSession();
    }, REFRESH_INTERVAL_MS);
  }, [refreshSession]);

  // Idle timeout: after 30 minutes of inactivity the user is signed out.
  // Stable (uses refs) so its identity never changes and it does not trigger
  // the bootstrap effect to re-run on every user change.
  const resetIdleTimer = useCallback(() => {
    if (!userRef.current) return;
    clearTimeout(idleTimerRef.current);
    idleTimerRef.current = setTimeout(() => {
      logoutRef.current && logoutRef.current();
      showToastRef.current && showToastRef.current('Session expired due to inactivity', 'info');
    }, 30 * 60 * 1000);
  }, []);

  const stopSessionTimers = useCallback(() => {
    clearInterval(refreshTimerRef.current);
    clearTimeout(idleTimerRef.current);
  }, []);

  const startSessionTimers = useCallback(() => {
    startRefreshLoop();
    resetIdleTimer();
  }, [startRefreshLoop, resetIdleTimer]);

  // Track user activity to keep the idle timer honest.
  const onUserActivity = useCallback(() => {
    resetIdleTimer();
  }, [resetIdleTimer]);

  useEffect(() => {
    if (!user) return undefined;
    startSessionTimers();
    window.addEventListener('mousemove', onUserActivity);
    window.addEventListener('keydown', onUserActivity);
    window.addEventListener('click', onUserActivity);
    window.addEventListener('scroll', onUserActivity);
    return () => {
      stopSessionTimers();
      window.removeEventListener('mousemove', onUserActivity);
      window.removeEventListener('keydown', onUserActivity);
      window.removeEventListener('click', onUserActivity);
      window.removeEventListener('scroll', onUserActivity);
    };
  }, [user, startSessionTimers, stopSessionTimers, onUserActivity]);

  // Switch target career
  const selectCareer = async (career) => {
    setCurrentCareer(career);
    loadRoadmap(career.id);
    if (user) {
      try {
        await api.updateMe({ selected_career_id: career.id });
        await refreshUser();
        await loadDashboard();
        showToast(`Target career changed to ${career.title}`, 'success');
      } catch (err) {
        console.warn('Failed to update target career on backend', err);
      }
    }
  };

  // Update skill progress & status
  const updateSkillProgress = async (skillId, { status, progress, notes, github_url, confidence }) => {
    try {
      const res = await api.updateSkillProgress(skillId, {
        status,
        progress: progress !== undefined ? progress : (status === 'completed' ? 100 : status === 'in_progress' ? 50 : 0),
        notes,
        github_url,
        confidence,
      });

      if (status === 'completed') {
        triggerConfetti();
        showToast('Skill Mastered! +50 XP Earned', 'success');
      } else {
        showToast('Skill progress updated', 'info');
      }

      // Refresh roadmap & dashboard & user
      if (currentCareer) {
        loadRoadmap(currentCareer.id);
      }
      refreshUser();
      loadDashboard();
      loadNotifications();
      return res;
    } catch (err) {
      showToast(err.message || 'Failed to update skill', 'error');
      throw err;
    }
  };

  // Open skill detail drawer
  const openSkillDrawer = (skillId) => {
    setSelectedSkillId(skillId);
    setIsSkillDrawerOpen(true);
  };

  const closeSkillDrawer = () => {
    setIsSkillDrawerOpen(false);
    setSelectedSkillId(null);
  };

  // Initial App bootstrap: load careers, then restore any persisted session.
  // A persisted session is detected server-side via the refresh cookie; if the
  // access cookie has expired we transparently mint a new one via /refresh.
  // Runs EXACTLY once on mount (guarded), so it can never self-trigger a loop.
  const bootstrappedRef = useRef(false);
  useEffect(() => {
    if (bootstrappedRef.current) return;
    bootstrappedRef.current = true;

    const initApp = async () => {
      setLoading(true);
      const loadedCareers = await loadCareers();

      let currentUser = null;
      try {
        currentUser = await api.getMe();
      } catch (err) {
        // Access token expired/missing — try to refresh from the refresh cookie.
        if (err.status === 401) {
          currentUser = await refreshSession();
        }
      }
      if (currentUser) {
        setUser(currentUser);
        startSessionTimers();
      }

      const activeCareerId = currentUser?.selected_career_id || (loadedCareers[0]?.id || 1);
      const targetCareer = loadedCareers.find((c) => c.id === activeCareerId) || loadedCareers[0];
      if (targetCareer) {
        setCurrentCareer(targetCareer);
        await loadRoadmap(targetCareer.id);
      }

      setLoading(false);
    };

    initApp();
  }, []);

  // Sync dashboard and notifications when the user changes. Career changes are
  // already handled by loadRoadmap on select/bootstrap, so we deliberately do
  // NOT depend on currentCareer here — this avoids re-fetch churn when the
  // career object identity changes.
  useEffect(() => {
    if (user) {
      loadDashboard();
      loadNotifications();
    }
  }, [user, loadDashboard, loadNotifications]);

  const value = {
    theme,
    activeTab,
    setActiveTab,
    user,
    careers,
    currentCareer,
    roadmap,
    dashboardData,
    notifications,
    unreadCount,
    selectedSkillId,
    isSkillDrawerOpen,
    isAuthModalOpen,
    isNotificationDrawerOpen,
    isAddSkillModalOpen,
    loading,
    toastMessage,
    sidebarOpen,
    setSidebarOpen,
    login,
    register,
    logout,
    refreshSession,
    selectCareer,
    loadRoadmap,
    loadDashboard,
    updateSkillProgress,
    openSkillDrawer,
    closeSkillDrawer,
    setIsAuthModalOpen,
    setIsNotificationDrawerOpen,
    setIsAddSkillModalOpen,
    showToast,
    triggerConfetti,
    loadNotifications,
    refreshUser,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
};
