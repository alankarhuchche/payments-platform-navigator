type LoadingStateProps = {
  label?: string;
};

export function LoadingState({ label = 'Loading platform knowledge...' }: LoadingStateProps) {
  return (
    <div className="state-box">
      <span className="loading-dot" />
      {label}
    </div>
  );
}
