import { useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';
import type { GlossaryTerm } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';

export function GlossaryPage() {
  const [terms, setTerms] = useState<GlossaryTerm[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<unknown>(null);

  useEffect(() => {
    api.glossary()
      .then((response) => setTerms(response.items || []))
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(() => {
    const lowered = query.toLowerCase();
    return terms.filter((term) => term.term.toLowerCase().includes(lowered) || term.definition.toLowerCase().includes(lowered));
  }, [terms, query]);

  if (loading) return <LoadingState label="Loading glossary..." />;
  if (error) return <ErrorState error={error} />;

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Glossary</p>
        <h2>Payments and platform terms</h2>
        <p>Search synthetic ISO 20022, operational resilience, platform, and change-safety language.</p>
      </header>

      <section className="content-card">
        <label>
          Search glossary
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="pacs.008, replay, four-eyes, Cloud Run" />
        </label>
      </section>

      {filtered.length === 0 ? <EmptyState title="No glossary terms match this search" /> : (
        <div className="list-grid">
          {filtered.map((term) => (
            <article className="content-card" key={term.term}>
              <div className="card-heading-row">
                <h3>{term.term}</h3>
                {term.category && <span className="badge badge-neutral">{term.category}</span>}
              </div>
              <p>{term.definition}</p>
              {(term.related_services || term.related_flows) && (
                <div className="chip-row">
                  {(term.related_services || []).map((item) => <span className="chip" key={item}>{item}</span>)}
                  {(term.related_flows || []).map((item) => <span className="chip" key={item}>{item}</span>)}
                </div>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
