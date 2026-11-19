import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from './App';
import * as healthApi from './api/health';

vi.mock('./api/health', () => ({
  fetchLiveness: vi.fn(),
  fetchDatabaseHealth: vi.fn(),
}));

const mockedLiveness = vi.mocked(healthApi.fetchLiveness);
const mockedDatabase = vi.mocked(healthApi.fetchDatabaseHealth);

beforeEach(() => {
  mockedLiveness.mockResolvedValue({ status: 'healthy' });
  mockedDatabase.mockResolvedValue({ status: 'healthy', database: 'connected' });
});

describe('App routing', () => {
  it('renders the status interface at the root route', async () => {
    render(<App />);
    expect(screen.getByText('Mini EMS')).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText('Database connected.')).toBeInTheDocument());
  });

  it('renders the status interface for an unknown route (catch-all)', () => {
    window.history.pushState({}, '', '/some/unknown/path');
    render(<App />);
    expect(screen.getByText('Mini EMS')).toBeInTheDocument();
    expect(screen.getByText('Frontend')).toBeInTheDocument();
  });
});
