import { describe, expect, it } from 'vitest';
import { resolveBaseUrl } from './client';

describe('resolveBaseUrl', () => {
  it('keeps a base that already includes /api/v1', () => {
    expect(resolveBaseUrl('http://localhost:8000/api/v1')).toBe('http://localhost:8000/api/v1');
  });

  it('appends /api/v1 once when missing', () => {
    expect(resolveBaseUrl('http://localhost:8000')).toBe('http://localhost:8000/api/v1');
  });

  it('strips trailing slashes before normalizing', () => {
    expect(resolveBaseUrl('http://localhost:8000/api/v1/')).toBe('http://localhost:8000/api/v1');
    expect(resolveBaseUrl('http://localhost:8000///')).toBe('http://localhost:8000/api/v1');
  });

  it('never doubles the /api/v1 prefix', () => {
    const url = resolveBaseUrl('http://localhost:8000/api/v1');
    expect(url.split('/api/v1').length - 1).toBe(1);
  });

  it('falls back when undefined, empty or whitespace', () => {
    expect(resolveBaseUrl(undefined)).toBe('http://localhost:8000/api/v1');
    expect(resolveBaseUrl('')).toBe('http://localhost:8000/api/v1');
    expect(resolveBaseUrl('   ')).toBe('http://localhost:8000/api/v1');
  });
});
