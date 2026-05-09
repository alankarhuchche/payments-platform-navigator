import { useEffect, useMemo, useState } from 'react';
import { Layout, NavTarget, RouteKey } from './components/Layout';
import { HomePage } from './pages/HomePage';
import { OnboardingPage } from './pages/OnboardingPage';
import { FlowsPage } from './pages/FlowsPage';
import { FlowDetailPage } from './pages/FlowDetailPage';
import { ServicesPage } from './pages/ServicesPage';
import { ServiceDetailPage } from './pages/ServiceDetailPage';
import { AskPage } from './pages/AskPage';
import { ChangeSafetyPage } from './pages/ChangeSafetyPage';
import { KnowledgeHealthPage } from './pages/KnowledgeHealthPage';
import { GlossaryPage } from './pages/GlossaryPage';

type AppRoute = NavTarget;

const defaultRoute: AppRoute = {
  route: 'home',
  role: 'Backend engineer',
  area: 'Payment Validation',
};

function parseHash(): AppRoute {
  const raw = window.location.hash.replace(/^#\/?/, '');
  if (!raw) return defaultRoute;
  const [path, queryString] = raw.split('?');
  const params = new URLSearchParams(queryString || '');
  const route = (path || 'home') as RouteKey;
  return {
    route,
    id: params.get('id') || undefined,
    role: params.get('role') || defaultRoute.role,
    area: params.get('area') || defaultRoute.area,
  };
}

function toHash(target: AppRoute) {
  const params = new URLSearchParams();
  if (target.id) params.set('id', target.id);
  if (target.role) params.set('role', target.role);
  if (target.area) params.set('area', target.area);
  const suffix = params.toString() ? `?${params.toString()}` : '';
  return `#/${target.route}${suffix}`;
}

export default function App() {
  const [route, setRoute] = useState<AppRoute>(() => parseHash());

  useEffect(() => {
    const onHashChange = () => setRoute(parseHash());
    window.addEventListener('hashchange', onHashChange);
    return () => window.removeEventListener('hashchange', onHashChange);
  }, []);

  const navigate = (target: NavTarget) => {
    const next = {
      ...defaultRoute,
      ...route,
      ...target,
    };
    window.location.hash = toHash(next);
    setRoute(next);
  };

  const page = useMemo(() => {
    switch (route.route) {
      case 'onboarding':
        return <OnboardingPage role={route.role || defaultRoute.role!} area={route.area || defaultRoute.area!} navigate={navigate} />;
      case 'flows':
        return <FlowsPage navigate={navigate} />;
      case 'flow-detail':
        return <FlowDetailPage flowId={route.id} navigate={navigate} />;
      case 'services':
        return <ServicesPage navigate={navigate} />;
      case 'service-detail':
        return <ServiceDetailPage serviceId={route.id} navigate={navigate} />;
      case 'ask':
        return <AskPage />;
      case 'change-safety':
        return <ChangeSafetyPage />;
      case 'knowledge-health':
        return <KnowledgeHealthPage navigate={navigate} />;
      case 'glossary':
        return <GlossaryPage />;
      case 'home':
      default:
        return <HomePage role={route.role || defaultRoute.role!} area={route.area || defaultRoute.area!} navigate={navigate} />;
    }
  }, [route]);

  return (
    <Layout currentRoute={route.route} navigate={navigate}>
      {page}
    </Layout>
  );
}
