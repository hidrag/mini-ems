import { afterEach, describe, expect, it, vi } from 'vitest';
import { AxiosError, type AxiosResponse } from 'axios';
import { apiClient } from './client';
import { fetchDatabaseHealth, fetchLiveness } from './health';

afterEach(() => {
  vi.restoreAllMocks();
});

describe('fetchLiveness', () => {
  it('returns the liveness payload from /health', async () => {
    vi.spyOn(apiClient, 'get').mockResolvedValue({ data: { status: 'healthy' } });
    await expect(fetchLiveness()).resolves.toEqual({ status: 'healthy' });
    expect(apiClient.get).toHaveBeenCalledWith('/health');
  });
});

describe('fetchDatabaseHealth', () => {
  it('returns the connected payload on HTTP 200', async () => {
    vi.spyOn(apiClient, 'get').mockResolvedValue({
      data: { status: 'healthy', database: 'connected' },
    });
    await expect(fetchDatabaseHealth()).resolves.toEqual({
      status: 'healthy',
      database: 'connected',
    });
    expect(apiClient.get).toHaveBeenCalledWith('/health/database');
  });

  it('returns the unavailable body on HTTP 503 instead of throwing', async () => {
    const response = {
      status: 503,
      data: { status: 'unhealthy', database: 'unavailable' },
    } as AxiosResponse;
    const error = new AxiosError('Service Unavailable', 'ERR_BAD_RESPONSE', undefined, undefined, response);
    vi.spyOn(apiClient, 'get').mockRejectedValue(error);
    await expect(fetchDatabaseHealth()).resolves.toEqual({
      status: 'unhealthy',
      database: 'unavailable',
    });
  });

  it('rethrows non-503 errors', async () => {
    const response = { status: 500, data: {} } as AxiosResponse;
    const error = new AxiosError('Server Error', 'ERR_BAD_RESPONSE', undefined, undefined, response);
    vi.spyOn(apiClient, 'get').mockRejectedValue(error);
    await expect(fetchDatabaseHealth()).rejects.toBe(error);
  });
});
