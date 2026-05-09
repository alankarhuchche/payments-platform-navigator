import { useState } from 'react';
import { api } from '../api/client';
import type { AskResponse } from '../api/types';
import { EmptyState } from '../components/EmptyState';
import { EntityBadge } from '../components/EntityBadge';
import { ErrorState } from '../components/ErrorState';
import { LoadingState } from '../components/LoadingState';

const examples = [
  'What should I check before changing Payment Validation Service?',
  'What happens when a pacs.008 payment fails sanctions screening?',
  'Which services are involved in outbound SWIFT pacs.008?',
  'What should a new support engineer learn first?',
];

export function AskPage() {
  const [question, setQuestion] = useState(examples[0]);
  const [answer, setAnswer] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<unknown>(null);

  const submit = () => {
    setLoading(true);
    setError(null);
    api.ask(question).then(setAnswer).catch(setError).finally(() => setLoading(false));
  };

  return (
    <section className="page-stack">
      <header className="page-header">
        <p className="eyebrow">Ask the Platform</p>
        <h2>Rule-based platform answers</h2>
        <p>Ask questions that can be answered from structured synthetic services, flows, runbooks, incidents, changes, tests, and glossary data.</p>
      </header>

      <section className="content-card">
        <label>
          Question
          <textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={4} />
        </label>
        <div className="example-row">
          {examples.map((item) => (
            <button key={item} onClick={() => setQuestion(item)}>{item}</button>
          ))}
        </div>
        <button className="primary-action" onClick={submit} disabled={loading || question.trim().length < 3}>
          Ask
        </button>
      </section>

      {loading && <LoadingState label="Generating structured answer..." />}
      {error != null && <ErrorState error={error} />}
      {!loading && !error && !answer && <EmptyState title="No answer yet" message="Choose an example question or ask about a service, flow, runbook, or change." />}
      {answer && (
        <section className="content-card answer-card">
          <div className="card-heading-row">
            <h3>Structured answer</h3>
            <EntityBadge label={`confidence ${Math.round((answer.confidence || 0) * 100)}%`} tone={(answer.confidence || 0) > 0.6 ? 'green' : 'amber'} />
          </div>
          <p className="answer-summary">{answer.answer_summary}</p>
          <AnswerList title="Matched entities" items={Object.entries(answer.matched_entities || {}).flatMap(([key, values]) => values.map((value) => `${key}: ${value}`))} />
          <AnswerList title="Relevant services" items={answer.relevant_services} />
          <AnswerList title="Relevant flows" items={answer.relevant_flows} />
          <AnswerList title="Relevant runbooks" items={answer.relevant_runbooks} />
          <AnswerList title="Risks" items={(answer.relevant_risks || []).map((risk) => `${risk.id}: ${risk.title}`)} />
          <AnswerList title="Next steps" items={answer.suggested_next_steps} />
          <AnswerList title="Source files" items={answer.source_files} />
        </section>
      )}
    </section>
  );
}

function AnswerList({ title, items = [] }: { title: string; items?: string[] }) {
  return (
    <div className="answer-section">
      <h4>{title}</h4>
      {items.length === 0 ? <span className="subtle">No linked evidence returned.</span> : (
        <div className="chip-row">
          {items.map((item) => <span className="chip" key={item}>{item}</span>)}
        </div>
      )}
    </div>
  );
}
