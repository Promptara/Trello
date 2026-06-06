// PROMPTARA — Storage & ID Helpers
import { STORAGE_KEY } from '../constants';

export const PromptaraStorage = {
  load() {
    try {
      const s = localStorage.getItem(STORAGE_KEY);
      if (s) return JSON.parse(s);
    } catch (_e) { /* ignore parse errors */ }
    return null;
  },
  save(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (_e) { /* ignore quota errors */ }
  },
  clear() {
    localStorage.removeItem(STORAGE_KEY);
  }
};

// TODO: Replace with server-generated IDs on API integration
export const genId = () => Math.random().toString(36).slice(2, 10);
