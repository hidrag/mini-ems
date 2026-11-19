import { useQuery } from '@tanstack/react-query';
import { fetchDatabaseHealth, fetchLiveness } from '../api/health';

export function useLiveness() {
  return useQuery({
    queryKey: ['health', 'liveness'],
    queryFn: fetchLiveness,
  });
}

export function useDatabaseHealth() {
  return useQuery({
    queryKey: ['health', 'database'],
    queryFn: fetchDatabaseHealth,
  });
}
