import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { HealthResponse, KnowledgeHealth } from '../api/types';
import { NavTarget } from '../components/Layout';
import { StatCard } from '../components/StatCard';
import { ErrorState } from '../components/ErrorState';

const roles = ['Backend engineer', 'Test engineer', 'Production support engineer', 'Engineering lead', 'Solution architect'];
const areas = ['SWIFT Gateway', 'Payment Validation', 'Sanctions Screening', 'Routing', 'Investigations'];

type HomePageProps = {
  role: string;
  area: string;
  navigate: (target: NavTarget) => void;
};

export function HomePage({ role, area, navigate }: HomePageProps) {
  const [selectedRole, setSelectedRole] = useState(role);
  const [selectedArea, setSelectedArea] = useState(area);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [knowledge, setKnowledge] = useState<KnowledgeHealth | null>(null);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    Promise.all([api.health(), api.knowledgeHealth()])
      .then(([healthResponse, knowledgeResponse]) => {
        setHealth(healthResponse);
        setKnowledge(knowledgeResponse);
      })
      .catch(setError);
  }, []);

  return (
    <section className="page-stack">
      <div className="hero-panel">
        <div>
          <p className="eyebrow">Public portfolio reference implementation</p>
          <h2>Payments engineering knowledge, connected for safer onboarding and change.</h2>
          <p>
            Navigate synthetic payment flows, service dependencies, operational runbooks, incident learnings,
            and change-safety evidence through a deterministic platform experience.
          </p>
        </div>
        <div className="hero-status">
          <span>API status</span>
          <strong>{health?.status || 'checking'}</strong>
          <small>{health?.data_classification || 'synthetic'} data</small>
        </div>
      </div>

      {error != null && <ErrorState error={error} title="Backend health check failed" />}

      <div className="form-grid">
        <label>
          Role
          <select value={selectedRole} onChange={(event) => setSelectedRole(event.target.value)}>
            {roles.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
        <label>
          Area
          <select value={selectedArea} onChange={(event) => setSelectedArea(event.target.value)}>
            {areas.map((item) => (
              <option key={item}>{item}</option>
            ))}
          </select>
        </label>
        <button className="primary-action" onClick={() => navigate({ route: 'onboarding', role: selectedRole, area: selectedArea })}>
          Open onboarding plan
        </button>
      </div>

      <div className="stat-grid">
        <StatCard title="Knowledge health" value={knowledge?.executive_summary?.overall_score} detail={knowledge?.executive_summary?.trend} status="green" />
        <StatCard title="Green services" value={knowledge?.executive_summary?.services_green} detail="ownership and evidence" status="green" />
        <StatCard title="Amber services" value={knowledge?.executive_summary?.services_amber} detail="needs attention" status="amber" />
        <StatCard title="Backend files" value={health?.data_files_loaded?.length} detail="synthetic sources loaded" status={health?.status} />
      </div>

      <div className="card-grid">
        {[
          ['onboarding', 'Role-based onboarding', '30-day path from role to platform confidence.'],
          ['flows', 'Payment flows', 'Explore pacs.008, pacs.009, status, sanctions, and repair journeys.'],
          ['services', 'Service dependencies', 'Inspect ownership, criticality, APIs, events, and dependencies.'],
          ['ask', 'Ask the Platform', 'Deterministic answers grounded in structured synthetic data.'],
          ['change-safety', 'Change safety', 'Generate impact, test, runbook, rollback, and evidence checks.'],
          ['knowledge-health', 'Knowledge health', 'Executive view of documentation, ownership, and readiness.'],
          ['glossary', 'Glossary', 'Payments, ISO 20022, resilience, and platform terms.'],
        ].map(([routeKey, title, detail]) => (
          <button key={routeKey} className="nav-card" onClick={() => navigate({ route: routeKey as NavTarget['route'], role: selectedRole, area: selectedArea })}>
            <strong>{title}</strong>
            <span>{detail}</span>
          </button>
        ))}
      </div>
    </section>
  );
}
