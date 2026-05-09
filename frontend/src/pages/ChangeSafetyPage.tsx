import { useEffect, useState } from 'react';
import { api } from '../api/client';
import type { ChangeSafetyResponse, Service } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';

const changeTypes = [
  'validation rule change',
  'event schema change',
  'API contract change',
  'routing rule change',
  'infrastructure change',
  'runbook update',
];

export function ChangeSafetyPage() {
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState('');
  const [changeType, setChangeType] = useState(changeTypes[0]);
  const [description, setDescription] = useState('');
  const [result, setResult] = useState<ChangeSafetyResponse | null>(null);
  const [loadingServices, setLoadingServices] = useState(true);
  const [loadingChecklist, setLoadingChecklist] = useState(false);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    api.services()
      .then((response) => {
        setServices(response.items || []);
        setSelectedService(response.items?.[0]?.id || '');
      })
      .catch(setError)
      .finally(() => setLoadingServices(false));
  }, []);

  const generate = () => {
    setLoadingChecklist(true);
    setError(null);
    api.changeSafety({ service_id: selectedService, change_type: changeType, description })
      .then(setResult)
      .catch(setError)
      .finally(() => setLoadingChecklist(false));
  };

  if (loadingServices) return <LoadingState label="Loading service catalogue..." />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Change safety checklist</p>
        <h2>Prepare a safer synthetic platform change</h2>
        <p>Generate deterministic impact, evidence, runbook, rollback, and operational checks from the backend data model.</p>
      </header>

      {error != null && <ErrorState error={error} />}
      {services.length === 0 ? <EmptyState title="No services available" /> : (
        <section className="content-card">
          <div className="form-grid">
            <label>
              Service
              <select value={selectedService} onChange={(event) => setSelectedService(event.target.value)}>
                {services.map((service) => <option value={service.id} key={service.id}>{service.name}</option>)}
              </select>
            </label>
            <label>
              Change type
              <select value={changeType} onChange={(event) => setChangeType(event.target.value)}>
                {changeTypes.map((item) => <option key={item}>{item}</option>)}
              </select>
            </label>
          </div>
          <label>
            Optional description
            <textarea value={description} onChange={(event) => setDescription(event.target.value)} rows={3} />
          </label>
          <button className="primary-action" onClick={generate} disabled={!selectedService || loadingChecklist}>Generate checklist</button>
        </section>
      )}

      {loadingChecklist && <LoadingState label="Generating checklist..." />}
      {result && (
        <section className="content-card">
          <div className="card-heading-row">
            <h3>{result.service?.name || 'Generated checklist'}</h3>
            <EntityBadge label={result.risk_level} tone={result.risk_level === 'high' ? 'red' : result.risk_level === 'medium' ? 'amber' : 'green'} />
          </div>
          <p>{result.summary}</p>
          <ChecklistSection title="Impacted flows" items={result.impacted_flows} />
          <ChecklistSection title="Impacted services" items={result.impacted_services} />
          <ChecklistSection title="Impacted events" items={result.impacted_events} />
          <ChecklistSection title="Impacted APIs" items={result.impacted_apis} />
          <ChecklistSection title="Runbooks to review" items={result.runbooks_to_review} />
          <ChecklistSection title="Tests to run" items={result.tests_to_run} />
          <ChecklistSection title="Related incidents" items={result.related_incidents} />
          <ChecklistSection title="Known risks" items={(result.known_risks || []).map((risk) => `${risk.id}: ${risk.title}`)} />
          <ChecklistSection title="Documentation updates" items={result.documentation_updates} />
          <ChecklistSection title="Operational checks" items={result.operational_checks} />
          <ChecklistSection title="Rollback considerations" items={result.rollback_considerations} />
        </section>
      )}
    </section>
  );
}

function ChecklistSection({ title, items = [] }: { title: string; items?: string[] }) {
  return (
    <div className="answer-section">
      <h4>{title}</h4>
      {items.length === 0 ? <span className="subtle">No items returned.</span> : (
        <ul className="clean-list">
          {items.map((item) => <li key={item}>{item}</li>)}
        </ul>
      )}
    </div>
  );
}
