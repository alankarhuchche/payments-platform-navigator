import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { PaymentFlow } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';

export function FlowDetailPage({ flowId, navigate }: { flowId?: string; navigate: (target: NavTarget) => void }) {
  const [flow, setFlow] = useState<PaymentFlow | null>(null);
  const [loading, setLoading] = useState(Boolean(flowId));
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    if (!flowId) return;
    setLoading(true);
    api.flow(flowId).then(setFlow).catch(setError).finally(() => setLoading(false));
  }, [flowId]);

  if (!flowId) return <EmptyState title="No flow selected" message="Open a flow from the Payment Flows page." />;
  if (loading) return <LoadingState label="Loading flow detail..." />;
  if (error) return <ErrorState error={error} />;
  if (!flow) return <EmptyState title="Flow not found" />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Flow detail</p>
        <h2>{flow.name}</h2>
        <p>{flow.business_purpose}</p>
        <div className="chip-row">
          <EntityBadge label={flow.message_type} tone="blue" />
          <EntityBadge label={flow.direction} />
          <EntityBadge label={flow.knowledge_health?.status} tone={flow.knowledge_health?.status === 'amber' ? 'amber' : 'green'} />
        </div>
      </header>

      <section className="content-card">
        <h3>Ordered steps</h3>
        {(flow.happy_path || []).length === 0 ? <EmptyState title="No ordered steps configured" /> : (
          <div className="timeline">
            {flow.happy_path?.map((step) => (
              <article className="timeline-item" key={`${step.step}-${step.service}`}>
                <span className="timeline-index">{step.step}</span>
                <div>
                  <button className="link-button" onClick={() => navigate({ route: 'service-detail', id: step.service })}>{step.service}</button>
                  <p>{step.action}</p>
                </div>
              </article>
            ))}
          </div>
        )}
      </section>

      <div className="two-column">
        <Evidence title="Services involved" items={flow.services} onClick={(id) => navigate({ route: 'service-detail', id })} />
        <Evidence title="Events" items={flow.events} />
        <Evidence title="APIs" items={flow.apis} />
        <Evidence title="Risks" items={flow.risks} />
        <Evidence title="Runbooks" items={flow.runbooks} />
        <Evidence title="Tests" items={flow.tests} />
      </div>
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
