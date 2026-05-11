import type {
  AskRequest,
  AskResponse,
  ChangeSafetyRequest,
  ChangeSafetyResponse,
  GlossaryTerm,
  HealthResponse,
  KnowledgeHealth,
  ListResponse,
  OnboardingPath,
  PaymentFlow,
  Service,
} from './types';

const configuredBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = configuredBaseUrl || (import.meta.env.DEV ? 'http://localhost:8080' : '');

function buildApiUrl(path: string): string {
  const normalizedPath = path.startsWith('/') ? path : `/${path}`;
  if (!API_BASE_URL) {
    return normalizedPath;
  }
  return `${API_BASE_URL.replace(/\/$/, '')}${normalizedPath}`;
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(buildApiUrl(path), {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;
    try {
      const payload = await response.json();
      message = payload?.error?.message || message;
    } catch {
      // Keep default message when the backend returns no JSON body.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>('/health'),
  services: () => request<ListResponse<Service>>('/api/services'),
  service: (serviceId: string) => request<Service>(`/api/services/${encodeURIComponent(serviceId)}`),
  flows: () => request<ListResponse<PaymentFlow>>('/api/flows'),
  flow: (flowId: string) => request<PaymentFlow>(`/api/flows/${encodeURIComponent(flowId)}`),
  glossary: () => request<ListResponse<GlossaryTerm>>('/api/glossary'),
  onboarding: (role: string, area: string) =>
    request<OnboardingPath>(
      `/api/onboarding?role=${encodeURIComponent(role)}&area=${encodeURIComponent(area)}`,
    ),
  knowledgeHealth: () => request<KnowledgeHealth>('/api/knowledge-health'),
  ask: (input: AskRequest | string) => {
    const payload = typeof input === 'string' ? { question: input } : input;
    return request<AskResponse>('/api/ask', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
  },
  changeSafety: (payload: ChangeSafetyRequest) =>
    request<ChangeSafetyResponse>('/api/change-safety-checklist', {
      method: 'POST',
      body: JSON.stringify(payload),
    }),
};

export { API_BASE_URL };
