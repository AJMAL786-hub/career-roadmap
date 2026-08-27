// API Client for CareerPath AI Backend
//
// Authentication uses HTTP-only SameSite=Lax cookies (set by the backend),
// so the SPA never touches the raw tokens. Every request sends
// `credentials: 'include'` to attach the cookie. A short-lived access cookie
// authenticates requests; a long-lived refresh cookie (only persisted when the
// user opts in via "Remember me") mints new access tokens on refresh.

const API_BASE = '/api/v1';

class ApiService {
  constructor() {
    this._refreshPromise = null;
  }

  _defaultHeaders() {
    return { 'Content-Type': 'application/json' };
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const config = {
      ...options,
      credentials: 'include',
      headers: {
        ...(options.multipart ? {} : this._defaultHeaders()),
        ...(options.headers || {}),
      },
    };

    let res;
    try {
      res = await fetch(url, config);
    } catch (err) {
      // Network-level failure (backend down, CORS, etc.)
      throw new Error('Network error — could not reach the server');
    }

    // Support both empty (204-style/object) and JSON responses.
    let body = null;
    const contentType = res.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
      body = await res.json().catch(() => null);
    }

    if (!res.ok) {
      const detail = (body && body.detail) || `Request failed with status ${res.status}`;
      const error = new Error(detail);
      error.status = res.status;
      throw error;
    }
    return body;
  }

  // ---- Auth (cookie-based) ----
  // login/register return the User object (the JWT lives in HTTP-only cookies).

  async register(data) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async login(data) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // Mint a fresh access token from the refresh cookie. Returns the User object.
  async refresh() {
    return this.request('/auth/refresh', { method: 'POST' });
  }

  // Invalidate the session by clearing the auth cookies.
  async logout() {
    return this.request('/auth/logout', { method: 'POST' }).catch(() => null);
  }

  async getMe() {
    return this.request('/auth/me');
  }

  async updateMe(data) {
    return this.request('/auth/me', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // ---- Careers ----
  async getCareers() {
    return this.request('/careers');
  }

  async getCareer(id) {
    return this.request(`/careers/${id}`);
  }

  async getRoadmap(careerId) {
    return this.request(`/careers/${careerId}/roadmap`);
  }

  // ---- Skills ----
  async getSkillDetail(skillId) {
    return this.request(`/skills/${skillId}`);
  }

  async updateSkillProgress(skillId, data) {
    return this.request(`/skills/${skillId}/progress`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async createCustomSkill(data) {
    return this.request('/skills/custom', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async addEvidence(skillId, data) {
    return this.request(`/skills/${skillId}/evidence`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getEvidence(skillId) {
    return this.request(`/skills/${skillId}/evidence`);
  }

  // ---- Dashboard ----
  async getDashboard() {
    return this.request('/dashboard');
  }

  // ---- Jobs & Gap Analyzer ----
  async analyzeJob(data) {
    return this.request('/jobs/analyze', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getSavedJobs() {
    return this.request('/jobs/saved');
  }

  // ---- Study Sessions ----
  async logStudySession(data) {
    return this.request('/study-sessions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async getStudySessions(limit = 50) {
    return this.request(`/study-sessions?limit=${limit}`);
  }

  async getStudyStats() {
    return this.request('/study-sessions/stats');
  }

  // ---- Interview Questions ----
  async getInterviewQuestions(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/interviews/questions${query ? '?' + query : ''}`);
  }

  async updateInterviewProgress(questionId, data) {
    return this.request(`/interviews/progress/${questionId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async createMockInterview(data) {
    return this.request('/interviews/mock', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // ---- Resume ----
  async getResumeProfile() {
    return this.request('/resume/profile');
  }

  async updateResumeProfile(data) {
    return this.request('/resume/profile', {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  async analyzeResume(data) {
    return this.request('/resume/analyze', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  async uploadResume(file) {
    const formData = new FormData();
    formData.append('file', file);
    return this.request('/resume/upload', {
      method: 'POST',
      body: formData,
      multipart: true,
    });
  }

  async getResumeHistory(limit = 30) {
    return this.request(`/resume/history?limit=${limit}`);
  }

  // ---- Projects ----
  async getProjects(careerId = null, difficulty = null) {
    const params = new URLSearchParams();
    if (careerId) params.append('career_id', careerId);
    if (difficulty) params.append('difficulty', difficulty);
    const query = params.toString();
    return this.request(`/projects${query ? '?' + query : ''}`);
  }

  async startProject(projectId) {
    return this.request(`/projects/${projectId}/start`, {
      method: 'POST',
    });
  }

  async updateProject(projectId, data) {
    return this.request(`/projects/${projectId}/progress`, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // ---- Resources ----
  async getResources(params = {}) {
    const query = new URLSearchParams(params).toString();
    return this.request(`/resources${query ? '?' + query : ''}`);
  }

  // ---- Market Intelligence ----
  async getMarket(careerSlug) {
    return this.request(`/market/${careerSlug}`);
  }

  // ---- Notifications & Profile ----
  async getNotifications(unreadOnly = false) {
    return this.request(`/notifications?unread_only=${unreadOnly}`);
  }

  async getUnreadCount() {
    return this.request('/notifications/unread-count');
  }

  async markAllNotificationsRead() {
    return this.request('/notifications/read-all', { method: 'PUT' });
  }

  async markNotificationRead(id) {
    return this.request(`/notifications/${id}/read`, { method: 'PUT' });
  }

  async getProfile() {
    return this.request('/profile');
  }
}

export const api = new ApiService();
