export interface TokenUsage {
  input_tokens: number;
  output_tokens: number;
  thinking_tokens: number;
  cache_read_tokens: number;
  total_tokens: number;
  estimated_cost_usd: number;
}

export interface BenchmarkItem {
  case_id: string;
  case_title: string;
  category: 'logic' | 'bugfix' | 'research' | 'tool_use' | string;
  model: string;
  cli: string;
  passed: boolean;
  duration_seconds: number;
  token_usage: TokenUsage;
  raw_response?: string;
  error_message?: string | null;
  evaluator_logs?: string;
  effort?: string | null;
  timestamp: number;
}

export interface AggregatedModelSummary {
  model: string;
  cli: string;
  effort?: string | null;
  total_cases: number;
  passed_cases: number;
  pass_rate: number;
  avg_duration_seconds: number;
  total_input_tokens: number;
  total_output_tokens: number;
  total_thinking_tokens: number;
  total_cost_usd: number;
  efficiency_score: number;
  category_pass_rates: Record<string, { passed: number; total: number; rate: number }>;
}
