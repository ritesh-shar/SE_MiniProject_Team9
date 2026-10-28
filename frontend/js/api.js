/**
 * BBMS Frontend API Helper
 *
 * Handles HTTP requests, JWT token storage, and authentication headers.
 */

const API_BASE = '/api';

const auth = {
  getAccessToken() {
    return localStorage.getItem('bbms_access_token');
  },

  getRefreshToken() {
    return localStorage.getItem('bbms_refresh_token');
  },

  getUser() {
    const raw = localStorage.getItem('bbms_user');
    return raw ? JSON.parse(raw) : null;
  },

  setAuth(accessToken, refreshToken, user) {
    if (accessToken) localStorage.setItem('bbms_access_token', accessToken);
    if (refreshToken) localStorage.setItem('bbms_refresh_token', refreshToken);
    if (user) localStorage.setItem('bbms_user', JSON.stringify(user));
  },

  clear() {
    localStorage.removeItem('bbms_access_token');
    localStorage.removeItem('bbms_refresh_token');
    localStorage.removeItem('bbms_user');
  },

  isAuthenticated() {
    return !!this.getAccessToken();
  },

  parseJwt(token) {
    try {
      const base64Url = token.split('.')[1];
      const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
      const jsonPayload = decodeURIComponent(
        atob(base64)
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join('')
      );
      return JSON.parse(jsonPayload);
    } catch (e) {
      return null;
    }
  },
};

/**
 * Standardized fetch wrapper that automatically attaches JWT token.
 */
async function apiFetch(endpoint, options = {}) {
  const url = endpoint.startsWith('http') ? endpoint : `${API_BASE}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  // Public endpoints: do not attach Authorization header for register and login
  const isPublicAuth =
    endpoint.includes('/auth/register') ||
    endpoint.includes('/auth/login') ||
    url.includes('/api/auth/register') ||
    url.includes('/api/auth/login');

  const token = auth.getAccessToken();
  if (token && !isPublicAuth) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  // If any API call returns 401, clear stored token and redirect to login page
  if (response.status === 401) {
    auth.clear();
    if (typeof window !== 'undefined' && window.location) {
      if (!endpoint.includes('/auth/login')) {
        window.location.href = 'index.html';
      }
    }
  }

  let data = null;
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    data = await response.json();
  } else {
    data = await response.text();
  }

  if (!response.ok) {
    const errorMsg =
      (data && data.error) ||
      (data && data.detail) ||
      `Request failed with status ${response.status}`;
    const code = (data && data.code) || 'API_ERROR';
    const err = new Error(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg);
    err.status = response.status;
    err.code = code;
    err.data = data;
    throw err;
  }

  return data;
}
