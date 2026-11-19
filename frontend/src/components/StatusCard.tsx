export type CardState = 'loading' | 'success' | 'error' | 'unavailable';

interface StatusCardProps {
  title: string;
  state: CardState;
  detail?: string;
  onRetry?: () => void;
}

const STATE_STYLES: Record<CardState, { badge: string; label: string }> = {
  loading: { badge: 'bg-slate-200 text-slate-700', label: 'Checking...' },
  success: { badge: 'bg-emerald-100 text-emerald-800', label: 'Healthy' },
  error: { badge: 'bg-rose-100 text-rose-800', label: 'Error' },
  unavailable: { badge: 'bg-amber-100 text-amber-800', label: 'Unavailable' },
};

export function StatusCard({ title, state, detail, onRetry }: StatusCardProps) {
  const { badge, label } = STATE_STYLES[state];
  const showRetry = (state === 'error' || state === 'unavailable') && Boolean(onRetry);
  return (
    <section
      className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm"
      aria-label={title}
    >
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-sm font-semibold text-slate-900">{title}</h2>
        <span className={`rounded-full px-3 py-1 text-xs font-medium ${badge}`} role="status">
          {label}
        </span>
      </div>
      {detail ? <p className="mt-3 text-sm text-slate-600">{detail}</p> : null}
      {showRetry ? (
        <button
          type="button"
          onClick={onRetry}
          className="mt-4 rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-700"
        >
          Retry
        </button>
      ) : null}
    </section>
  );
}
