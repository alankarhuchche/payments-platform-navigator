export type ListResponse<T> = {
  metadata?: Record<string, unknown>;
  count: number;
  items: T[];
};

export type HealthResponse = {
  status: string;
  service: string;
  data_classification: string;
  data_files_loaded: string[];
};

export type KnowledgeHealthRef = {
  score?: number;
  status?: string;
  coverage?: string;
  watch_item?: string;
  last_reviewed?: string;
  dimensions?: Record<string, number>;
};

export type Risk = {
  id: string;
  title: string;
  controls?: string[];
};

export type Service = {
  id: string;
  name: string;
  type?: string;
  domain?: string;
  lifecycle?: string;
  summary?: string;
  owned_by?: string;
  criticality?: string;
  runtime?: string;
  data_classification?: string;
  upstream_services?: string[];
  downstream_services?: string[];
  supports_flows?: string[];
  publishes_events?: string[];
  consumes_events?: string[];
  provides_apis?: string[];
  consumes_apis?: string[];
  runbooks?: string[];
  risks?: Risk[];
  related_incidents?: string[];
  related_changes?: string[];
  tests?: string[];
  knowledge_health?: KnowledgeHealthRef;
};

export type FlowStep = {
  step: number;
  service: string;
  action: string;
};

export type PaymentFlow = {
  id: string;
  name: string;
  message_type?: string;
  direction?: string;
  business_purpose?: string;
  entry_service?: string;
  services?: string[];
  events?: string[];
  apis?: string[];
  runbooks?: string[];
  tests?: string[];
  risks?: string[];
  happy_path?: FlowStep[];
  synthetic_example?: Record<string, string>;
  knowledge_health?: KnowledgeHealthRef;
};

export type GlossaryTerm = {
  term: string;
  definition: string;
  category?: string;
  related_services?: string[];
  related_flows?: string[];
};

export type OnboardingModule = {
  id: string;
  title: string;
  resources?: string[];
  completion_signal?: string;
};

export type OnboardingPath = {
  id: string;
  role: string;
  goal?: string;
  area?: string;
  area_matched_services?: string[];
  recommended_starting_services?: string[];
  primary_flows?: string[];
  modules?: OnboardingModule[];
};

export type DashboardTile = {
  id: string;
  title: string;
  value: number;
  unit: string;
  status: string;
};

export type KnowledgeHealth = {
  metadata?: Record<string, unknown>;
  executive_summary?: {
    overall_score?: number;
    trend?: string;
    services_green?: number;
    services_amber?: number;
    services_red?: number;
    top_risks?: string[];
    recommended_actions?: string[];
  };
  dashboard_tiles?: DashboardTile[];
  service_health?: Array<{
    id?: string;
    service_id: string;
    score?: number;
    status?: string;
    last_reviewed?: string;
    owner?: string;
    dimensions?: Record<string, number>;
  }>;
  flow_health?: Array<{
    flow_id: string;
    score?: number;
    status?: string;
    coverage?: string;
    watch_item?: string;
  }>;
};

export type AskResponse = {
  answer_summary: string;
  matched_entities?: Record<string, string[]>;
  relevant_services?: string[];
  relevant_flows?: string[];
  relevant_runbooks?: string[];
  relevant_risks?: Risk[];
  suggested_next_steps?: string[];
  confidence?: number;
  source_files?: string[];
};

export type ChangeSafetyRequest = {
  service_id: string;
  change_type: string;
  description?: string;
};

export type ChangeSafetyResponse = {
  service?: {
    id: string;
    name: string;
    criticality?: string;
    owned_by?: string;
  };
  change_type: string;
  impacted_flows?: string[];
  impacted_services?: string[];
  impacted_events?: string[];
  impacted_apis?: string[];
  runbooks_to_review?: string[];
  tests_to_run?: string[];
  related_incidents?: string[];
  known_risks?: Risk[];
  known_test_gaps?: Array<Record<string, unknown>>;
  documentation_updates?: string[];
  operational_checks?: string[];
  rollback_considerations?: string[];
  risk_level?: string;
  summary?: string;
};
