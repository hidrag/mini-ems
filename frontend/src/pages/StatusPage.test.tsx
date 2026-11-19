import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import * as healthApi from '../api/health';
import { StatusPage } from './StatusPage';

vi.mock('../api/health', () => ({
  fetchLiveness: vi.fn(),
  fetchDatabaseHealth: vi.fn(),
}));

const mockedLiveness = vi.mocked(healthApi.fetchLiveness);
const mockedDatabase = vi.mocked(healthApi.fetchDatabaseHealth);

function renderPage() {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false, refetchOnWindowFocus: false, gcTime: Infinity },
    },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <StatusPage />
    </QueryClientProvider>,
  );
}

beforeEach(() => {
  vi.clearAllMocks();
});

describe('StatusPage', () => {
  it('renders the application identity and frontend status', async () => {
    mockedLiveness.mockResolvedValue({ status: 'healthy' });
    mockedDatabase.mockResolvedValue({ status: 'healthy', database: 'connected' });
    renderPage();
    expect(screen.getByText('Mini EMS')).toBeInTheDocument();
    expect(screen.getByText('Frontend')).toBeInTheDocument();
    await waitFor(() => expect(screen.getAllByText('Healthy').length).toBeGreaterThanOrEqual(2));
  });

  it('shows loading states while checks are pending', () => {
    mockedLiveness.mockReturnValue(new Promise(() => {}));
    mockedDatabase.mockReturnValue(new Promise(() => {}));
    renderPage();
    expect(screen.getAllByText('Checking...').length).toBe(2);
  });

  it('shows backend and database success states', async () => {
    mockedLiveness.mockResolvedValue({ status: 'healthy' });
    mockedDatabase.mockResolvedValue({ status: 'healthy', database: 'connected' });
    renderPage();
    await waitFor(() => {
      expect(screen.getByText('API is responding.')).toBeInTheDocument();
      expect(screen.getByText('Database connected.')).toBeInTheDocument();
    });
  });

  it('shows the database unavailable state for a 503 reading', async () => {
    mockedLiveness.mockResolvedValue({ status: 'healthy' });
    mockedDatabase.mockResolvedValue({ status: 'unhealthy', database: 'unavailable' });
    renderPage();
    await waitFor(() => {
      expect(screen.getByText('Database is unavailable.')).toBeInTheDocument();
      expect(screen.getByText('Unavailable')).toBeInTheDocument();
    });
  });

  it('shows an error state and a retry control when liveness fails', async () => {
    mockedLiveness.mockRejectedValue(new Error('network down'));
    mockedDatabase.mockResolvedValue({ status: 'healthy', database: 'connected' });
    renderPage();
    await waitFor(() => expect(screen.getByText('Could not reach the API.')).toBeInTheDocument());
    expect(screen.getAllByRole('button', { name: 'Retry' }).length).toBeGreaterThanOrEqual(1);
  });

  it('retries a failed check and recovers to success', async () => {
    mockedLiveness
      .mockRejectedValueOnce(new Error('network down'))
      .mockResolvedValue({ status: 'healthy' });
    mockedDatabase.mockResolvedValue({ status: 'healthy', database: 'connected' });
    renderPage();
    await waitFor(() => expect(screen.getByText('Could not reach the API.')).toBeInTheDocument());
    const retry = screen.getAllByRole('button', { name: 'Retry' })[0];
    await userEvent.click(retry);
    await waitFor(() => expect(screen.getByText('API is responding.')).toBeInTheDocument());
  });
});
