import { StatusCard, type CardState } from '../components/StatusCard';
import { useDatabaseHealth, useLiveness } from '../hooks/useHealth';

export function StatusPage() {
  const liveness = useLiveness();
  const database = useDatabaseHealth();

  const livenessState: CardState = liveness.isPending
    ? 'loading'
    : liveness.isError
      ? 'error'
      : liveness.data?.status === 'healthy'
        ? 'success'
        : 'error';

  const databaseState: CardState = database.isPending
    ? 'loading'
    : database.isError
      ? 'error'
      : database.data?.status === 'healthy'
        ? 'success'
        : 'unavailable';

  const livenessDetail =
    livenessState === 'loading'
      ? 'Checking API liveness...'
      : livenessState === 'success'
        ? 'API is responding.'
        : 'Could not reach the API.';

  const databaseDetail =
    databaseState === 'loading'
      ? 'Checking database readiness...'
      : databaseState === 'success'
        ? 'Database connected.'
        : databaseState === 'unavailable'
          ? 'Database is unavailable.'
          : 'Could not check the database.';

  return (
    <div className="mx-auto max-w-3xl px-4 py-10">
      <header className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900">Mini EMS</h1>
        <p className="mt-1 text-sm text-slate-600">
          Industrial Energy Monitoring &amp; Management System - foundation status
        </p>
      </header>
      <div className="grid gap-4 sm:grid-cols-2">
        <StatusCard title="Frontend" state="success" detail="React application is running." />
        <StatusCard
          title="Backend API"
          state={livenessState}
          detail={livenessDetail}
          onRetry={() => {
            void liveness.refetch();
          }}
        />
        <StatusCard
          title="PostgreSQL"
          state={databaseState}
          detail={databaseDetail}
          onRetry={() => {
            void database.refetch();
          }}
        />
      </div>
    </div>
  );
}
