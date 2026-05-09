import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { PaymentFlow } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';

export function FlowsPage({ navigate }: { navigate: (target: NavTarget) => void }) {
  const [flows, setFlows] = useState<PaymentFlow[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    api.flows()
      .then((response) => setFlows(response.items || []))
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState label="Loading payment flows..." />;
  if (error) return <ErrorState error={error} />;
  if (flows.length === 0) return <EmptyState title="No payment flows" message="The backend returned no payment flows." />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Payment flow explorer</p>
        <h2>Payment flows</h2>
        <p>Review synthetic ISO 20022 and platform journeys with service, test, and risk evidence.</p>
      </header>

      <div className="list-grid">
        {flows.map((flow) => (
          <article className="content-card" key={flow.id}>
            <div className="card-heading-row">
              <h3>{flow.name}</h3>
              <EntityBadge label={flow.knowledge_health?.status} tone={flow.knowledge_health?.status === 'amber' ? 'amber' : 'green'} />
            </div>
            <p>{flow.business_purpose}</p>
            <div className="chip-row">
              <EntityBadge label={flow.message_type} tone="blue" />
              <EntityBadge label={flow.direction} />
              <EntityBadge label={`${flow.services?.length || 0} services`} />
              <EntityBadge label={`${flow.tests?.length || 0} tests`} />
            </div>
            {flow.knowledge_health?.watch_item && <p className="watch-item">{flow.knowledge_health.watch_item}</p>}
            <button className="secondary-action" onClick={() => navigate({ route: 'flow-detail', id: flow.id })}>Open flow detail</button>
          </article>
        ))}
      </div>
    </section>
  );
}
