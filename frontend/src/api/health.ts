import axios from 'axios';
import { apiClient } from './client';

export interface LivenessResponse {
  status: string;
}

export interface DatabaseHealthResponse {
  status: string;
  database: string;
}

/** Application liveness (GET /api/v1/health); independent of PostgreSQL. */
export async function fetchLiveness(): Promise<LivenessResponse> {
  const { data } = await apiClient.get<LivenessResponse>('/health');
  return data;
}

/**
 * Database readiness (GET /api/v1/health/database).
 * HTTP 503 is a valid "unavailable" reading, not a transport error: its body
 * is returned so the UI can show the unavailable state. Other failures throw.
 */
export async function fetchDatabaseHealth(): Promise<DatabaseHealthResponse> {
  try {
    const { data } = await apiClient.get<DatabaseHealthResponse>('/health/database');
    return data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 503) {
      return error.response.data as DatabaseHealthResponse;
    }
    throw error;
  }
}
