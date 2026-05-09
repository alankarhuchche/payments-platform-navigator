import type { ReactNode } from 'react';
import { API_BASE_URL } from '../api/client';

export type RouteKey =
  | 'home'
  | 'onboarding'
  | 'flows'
  | 'flow-detail'
  | 'services'
  | 'service-detail'
  | 'ask'
  | 'change-safety'
  | 'knowledge-health'
  | 'glossary';

export type NavTarget = {
  route: RouteKey;
  id?: string;
  role?: string;
  area?: string;
};

type LayoutProps = {
  children: ReactNode;
  currentRoute: RouteKey;
  navigate: (target: NavTarget) => void;
};

const navItems: Array<{ route: RouteKey; label: string }> = [
  { route: 'home', label: 'Home' },
  { route: 'onboarding', label: 'Onboarding' },
  { route: 'flows', label: 'Payment Flows' },
  { route: 'services', label: 'Services' },
  { route: 'ask', label: 'Ask' },
  { route: 'change-safety', label: 'Change Safety' },
  { route: 'knowledge-health', label: 'Knowledge Health' },
  { route: 'glossary', label: 'Glossary' },
];

export function Layout({ children, currentRoute, navigate }: LayoutProps) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">PPN</div>
          <div>
            <h1>Payments Platform Navigator</h1>
            <p>Synthetic payments engineering knowledge</p>
          </div>
        </div>

        <nav className="main-nav" aria-label="Primary navigation">
          {navItems.map((item) => (
            <button
              key={item.route}
              className={currentRoute === item.route ? 'nav-link active' : 'nav-link'}
              onClick={() => navigate({ route: item.route })}
            >
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-note">
          <strong>Backend</strong>
          <span>{API_BASE_URL}</span>
        </div>
      </aside>

      <main className="main-content">
        <div className="top-strip">
          <span>Synthetic data only</span>
          <span>No external AI dependency</span>
          <span>Cloud Run MVP</span>
        </div>
        {children}
      </main>
    </div>
  );
}
