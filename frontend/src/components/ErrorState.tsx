type ErrorStateProps = {
  title?: string;
  error: unknown;
};

export function ErrorState({ title = 'Unable to load data', error }: ErrorStateProps) {
  const message = error instanceof Error ? error.message : 'An unexpected error occurred.';
  return (
    <div className="state-box state-error">
      <strong>{title}</strong>
      <p>{message}</p>
    </div>
  );
}
