const AUTH_KEY = 'promptara_auth';

export const AuthStore = {
  /**
   * Save auth data (like token, user info) to local storage
   * @param {Object} data 
   */
  setAuth(data) {
    try {
      localStorage.setItem(AUTH_KEY, JSON.stringify(data));
    } catch (e) {
      console.error('Failed to save auth to local storage', e);
    }
  },

  /**
   * Get auth data from local storage
   * @returns {Object|null}
   */
  getAuth() {
    try {
      const auth = localStorage.getItem(AUTH_KEY);
      if (auth) {
        return JSON.parse(auth);
      }
    } catch (e) {
      console.error('Failed to parse auth from local storage', e);
    }
    return null;
  },

  /**
   * Get auth token specifically
   * @returns {string|null}
   */
  getToken() {
    const auth = this.getAuth();
    return auth?.token || null;
  },

  /**
   * Clear auth data (for logout)
   */
  clearAuth() {
    try {
      localStorage.removeItem(AUTH_KEY);
    } catch (e) {
      console.error('Failed to remove auth from local storage', e);
    }
  }
};

export default AuthStore;
