import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { Service } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';

export function ServiceDetailPage({ serviceId, navigate }: { serviceId?: string; navigate: (target: NavTarget) => void }) {
  const [service, setService] = useState<Service | null>(null);
  const [loading, setLoading] = useState(Boolean(serviceId));
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    if (!serviceId) return;
    setLoading(true);
    api.service(serviceId).then(setService).catch(setError).finally(() => setLoading(false));
  }, [serviceId]);

  if (!serviceId) return <EmptyState title="No service selected" message="Open a service from the Services page." />;
  if (loading) return <LoadingState label="Loading service detail..." />;
  if (error) return <ErrorState error={error} />;
  if (!service) return <EmptyState title="Service not found" />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Service detail</p>
        <h2>{service.name}</h2>
        <p>{service.summary}</p>
        <div className="chip-row">
          <EntityBadge label={service.criticality} tone={service.criticality === 'tier-0' ? 'red' : 'amber'} />
          <EntityBadge label={service.type} />
          <EntityBadge label={service.domain} />
          <EntityBadge label={service.knowledge_health?.status} tone={service.knowledge_health?.status === 'amber' ? 'amber' : 'green'} />
        </div>
      </header>

      <section className="content-card">
        <h3>Ownership and operating context</h3>
        <dl className="compact-dl wide">
          <dt>Owner</dt><dd>{service.owned_by}</dd>
          <dt>Runtime</dt><dd>{service.runtime}</dd>
          <dt>Lifecycle</dt><dd>{service.lifecycle}</dd>
          <dt>Data classification</dt><dd>{service.data_classification}</dd>
        </dl>
      </section>

      <div className="two-column">
        <Evidence title="Payment flows" items={service.supports_flows} onClick={(id) => navigate({ route: 'flow-detail', id })} />
        <Evidence title="Upstream dependencies" items={service.upstream_services} onClick={(id) => navigate({ route: 'service-detail', id })} />
        <Evidence title="Downstream dependencies" items={service.downstream_services} onClick={(id) => navigate({ route: 'service-detail', id })} />
        <Evidence title="Events consumed" items={service.consumes_events} />
        <Evidence title="Events published" items={service.publishes_events} />
        <Evidence title="APIs" items={[...(service.provides_apis || []), ...(service.consumes_apis || [])]} />
        <Evidence title="Runbooks" items={service.runbooks} />
        <Evidence title="Related incidents" items={service.related_incidents} />
      </div>

      <section className="content-card">
        <h3>Known risks and change considerations</h3>
        {(service.risks || []).length === 0 ? <EmptyState title="No known risks linked" /> : (
          <div className="risk-list">
            {service.risks?.map((risk) => (
              <article key={risk.id}>
                <strong>{risk.title}</strong>
                <div className="chip-row">
                  {(risk.controls || []).map((control) => <span className="chip" key={control}>{control}</span>)}
                </div>
              </article>
            ))}
          </div>
        )}
      </section>
    </section>
  );
}

function Evidence({ title, items = [], onClick }: { title: string; items?: string[]; onClick?: (id: string) => void }) {
  return (
    <section className="content-card">
      <h3>{title}</h3>
      {items.length === 0 ? <EmptyState title="No evidence linked" /> : (
        <div className="chip-row">
          {items.map((item) => onClick ? (
            <button className="chip chip-button" key={item} onClick={() => onClick(item)}>{item}</button>
          ) : <span className="chip" key={item}>{item}</span>)}
        </div>
      )}
    </section>
  );
}
