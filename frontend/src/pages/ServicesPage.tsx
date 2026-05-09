import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Service } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';

export function ServicesPage({ navigate }: { navigate: (target: NavTarget) => void }) {
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    api.services()
      .then((response) => setServices(response.items || []))
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState label="Loading services..." />;
  if (error) return <ErrorState error={error} />;
  if (services.length === 0) return <EmptyState title="No services" message="The backend returned no services." />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Service dependency map</p>
        <h2>Services</h2>
        <p>Inspect ownership, criticality, flow support, and direct dependency context.</p>
      </header>

      <div className="list-grid">
        {services.map((service) => (
          <article className="content-card" key={service.id}>
            <div className="card-heading-row">
              <h3>{service.name}</h3>
              <EntityBadge label={service.criticality} tone={service.criticality === 'tier-0' ? 'red' : service.criticality === 'tier-1' ? 'amber' : 'neutral'} />
            </div>
            <p>{service.summary}</p>
            <dl className="compact-dl">
              <dt>Owner</dt>
              <dd>{service.owned_by || 'Unassigned'}</dd>
              <dt>Depends on</dt>
              <dd>{(service.upstream_services || []).join(', ') || 'No upstream services'}</dd>
              <dt>Downstream</dt>
              <dd>{(service.downstream_services || []).join(', ') || 'No downstream services'}</dd>
            </dl>
            <div className="chip-row">
              <EntityBadge label={`${service.supports_flows?.length || 0} flows`} />
              <EntityBadge label={service.knowledge_health?.status} tone={service.knowledge_health?.status === 'amber' ? 'amber' : 'green'} />
            </div>
            <button className="secondary-action" onClick={() => navigate({ route: 'service-detail', id: service.id })}>Open service detail</button>
          </article>
        ))}
      </div>
    </section>
  );
}
