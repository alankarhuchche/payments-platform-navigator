import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { OnboardingPath } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';

type Props = {
  role: string;
  area: string;
  navigate: (target: NavTarget) => void;
};

export function OnboardingPage({ role, area, navigate }: Props) {
  const [data, setData] = useState<OnboardingPath | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    setLoading(true);
    api.onboarding(role, area)
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, [role, area]);

  if (loading) return <LoadingState label="Loading onboarding path..." />;
  if (error) return <ErrorState error={error} />;
  if (!data) return <EmptyState title="No onboarding path" message="No onboarding data is available for this role." />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Role-based onboarding</p>
        <h2>{data.role}</h2>
        <p>{data.goal}</p>
        <span className="subtle">Selected area: {area}</span>
      </header>

      <div className="two-column">
        <EvidencePanel title="Key services" items={data.recommended_starting_services} onClick={(id) => navigate({ route: 'service-detail', id })} />
        <EvidencePanel title="Key flows" items={data.primary_flows} onClick={(id) => navigate({ route: 'flow-detail', id })} />
      </div>

      <section className="content-card">
        <h3>30-day phased journey</h3>
        <div className="timeline">
          {(data.modules || []).map((module, index) => (
            <article className="timeline-item" key={module.id}>
              <span className="timeline-index">Day {index * 10 + 1}-{(index + 1) * 10}</span>
              <div>
                <h4>{module.title}</h4>
                <p>{module.completion_signal}</p>
                <div className="chip-row">
                  {(module.resources || []).map((item) => (
                    <span className="chip" key={item}>{item}</span>
                  ))}
                </div>
              </div>
            </article>
          ))}
        </div>
      </section>

      <div className="two-column">
        <section className="content-card">
          <h3>Suggested first contribution</h3>
          <p>
            Prepare a low-risk change brief using the relevant service detail, linked flow, runbooks, and
            test evidence. Then generate a change-safety checklist before implementation.
          </p>
        </section>
        <section className="content-card">
          <h3>Knowledge checks</h3>
          <ul className="clean-list">
            <li>Can explain the payment journey and status events.</li>
            <li>Can identify affected APIs, events, tests, and runbooks.</li>
            <li>Can prepare rollback and monitoring notes for a change.</li>
          </ul>
        </section>
      </div>
    </section>
  );
}

function EvidencePanel({ title, items = [], onClick }: { title: string; items?: string[]; onClick: (id: string) => void }) {
  return (
    <section className="content-card">
      <h3>{title}</h3>
      {items.length === 0 ? <EmptyState title="No items configured" /> : (
        <div className="evidence-list">
          {items.map((item) => (
            <button key={item} onClick={() => onClick(item)}>{item}</button>
          ))}
        </div>
      )}
    </section>
  );
}
