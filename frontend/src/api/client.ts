import axios from 'axios';

const FALLBACK_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Normalize the configured API base URL so the `/api/v1` prefix appears
 * exactly once. Accepts a base that already includes `/api/v1` or one that
 * does not; never appends the prefix twice.
 */
export function resolveBaseUrl(raw: string | undefined): string {
  const value = raw && raw.trim() ? raw.trim() : FALLBACK_BASE_URL;
  let url = value.replace(/\/+$/, '');
  if (!url.endsWith('/api/v1')) {
    url += '/api/v1';
  }
  return url;
}

export const apiBaseUrl = resolveBaseUrl(import.meta.env.VITE_API_BASE_URL);

export const apiClient = axios.create({
  baseURL: apiBaseUrl,
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});
