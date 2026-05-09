import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { KnowledgeHealth } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';
import { NavTarget } from '../components/Layout';
import { StatCard } from '../components/StatCard';

export function KnowledgeHealthPage({ navigate }: { navigate: (target: NavTarget) => void }) {
  const [data, setData] = useState<KnowledgeHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    api.knowledgeHealth().then(setData).catch(setError).finally(() => setLoading(false));
  }, []);

  if (loading) return <LoadingState label="Loading knowledge-health dashboard..." />;
  if (error) return <ErrorState error={error} />;
  if (!data) return <EmptyState title="No knowledge-health data" />;

  const summary = data.executive_summary;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Executive dashboard</p>
        <h2>Knowledge health</h2>
        <p>Leadership view of ownership, readiness, documentation, dependency clarity, and test evidence.</p>
      </header>

      <div className="stat-grid">
        <StatCard title="Overall score" value={summary?.overall_score} detail={summary?.trend} status="green" />
        <StatCard title="Service ownership coverage" value={summary?.services_green} detail="green services" status="green" />
        <StatCard title="Critical warnings" value={summary?.services_amber} detail="amber services" status="amber" />
        <StatCard title="Stale documentation count" value={summary?.services_red || 0} detail="red services" status="green" />
      </div>

      <div className="stat-grid">
        {(data.dashboard_tiles || []).map((tile) => (
          <StatCard key={tile.id} title={tile.title} value={`${tile.value} ${tile.unit}`} status={tile.status} />
        ))}
      </div>

      <div className="two-column">
        <section className="content-card">
          <h3>Top risks</h3>
          <ul className="clean-list">
            {(summary?.top_risks || []).map((item) => <li key={item}>{item}</li>)}
          </ul>
        </section>
        <section className="content-card">
          <h3>Leadership interpretation</h3>
          <ul className="clean-list">
            {(summary?.recommended_actions || []).map((item) => <li key={item}>{item}</li>)}
            <li>Architecture decision record coverage should be reviewed when major flow or API changes are made.</li>
            <li>Missing dependency mappings should be prioritised for tier-0 and tier-1 services.</li>
          </ul>
        </section>
      </div>

      <section className="content-card">
        <h3>Service health</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Service</th>
                <th>Owner</th>
                <th>Score</th>
                <th>Status</th>
                <th>Reviewed</th>
              </tr>
            </thead>
            <tbody>
              {(data.service_health || []).map((item) => (
                <tr key={item.service_id}>
                  <td><button className="link-button" onClick={() => navigate({ route: 'service-detail', id: item.service_id })}>{item.service_id}</button></td>
                  <td>{item.owner}</td>
                  <td>{item.score}</td>
                  <td><EntityBadge label={item.status} tone={item.status === 'amber' ? 'amber' : 'green'} /></td>
                  <td>{item.last_reviewed}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="content-card">
        <h3>Flow coverage</h3>
        <div className="list-grid compact">
          {(data.flow_health || []).map((item) => (
            <article key={item.flow_id} className="mini-card">
              <button className="link-button" onClick={() => navigate({ route: 'flow-detail', id: item.flow_id })}>{item.flow_id}</button>
              <div className="chip-row">
                <EntityBadge label={item.score} />
                <EntityBadge label={item.status} tone={item.status === 'amber' ? 'amber' : 'green'} />
                <EntityBadge label={item.coverage} />
              </div>
              <p>{item.watch_item}</p>
            </article>
          ))}
        </div>
      </section>
    </section>
  );
}
