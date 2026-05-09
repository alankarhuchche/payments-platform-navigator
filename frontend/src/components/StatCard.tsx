import { EntityBadge } from './EntityBadge';

type StatCardProps = {
  title: string;
  value?: string | number;
  detail?: string;
  status?: string;
};

export function StatCard({ title, value, detail, status }: StatCardProps) {
  return (
    <article className="stat-card">
      <div className="stat-card-title">{title}</div>
      <div className="stat-card-value">{value ?? 'Unavailable'}</div>
      <div className="stat-card-footer">
        {detail && <span>{detail}</span>}
        {status && <EntityBadge label={status} tone={statusTone(status)} />}
      </div>
    </article>
  );
}

function statusTone(status: string): 'green' | 'amber' | 'red' | 'neutral' {
  const lowered = status.toLowerCase();
  if (lowered.includes('green') || lowered.includes('ok')) return 'green';
  if (lowered.includes('amber') || lowered.includes('medium')) return 'amber';
  if (lowered.includes('red') || lowered.includes('high')) return 'red';
  return 'neutral';
}
