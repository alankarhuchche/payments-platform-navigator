type EntityBadgeProps = {
  label?: string | number;
  tone?: 'neutral' | 'green' | 'amber' | 'red' | 'blue';
};

export function EntityBadge({ label, tone = 'neutral' }: EntityBadgeProps) {
  if (label === undefined || label === null || label === '') {
    return null;
  }

  return <span className={`badge badge-${tone}`}>{label}</span>;
}
