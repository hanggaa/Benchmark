import type { BenchmarkItem } from './types';

export function configurationKey(item: { model: string; cli: string; effort?: string | null }): string {
  return JSON.stringify([item.model, item.cli, item.effort || null]);
}

export function configurationName(model: string, effort?: string | null): string {
  const suffix = effort ? ' (' + effort.toLowerCase() + ')' : '';
  return suffix && model.toLowerCase().endsWith(suffix) ? model.slice(0, -suffix.length) : model;
}

export function outcome(item: BenchmarkItem): 'pass' | 'fail' | 'error' {
  return item.error_message ? 'error' : item.passed ? 'pass' : 'fail';
}

export const statusLabels = { pass: 'Pass', fail: 'Fail', error: 'CLI error' };

export const cost = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD',
  minimumFractionDigits: 2,
  maximumFractionDigits: 4,
});

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function isNonnegativeNumber(value: unknown): value is number {
  return typeof value === 'number' && Number.isFinite(value) && value >= 0;
}

function isBenchmarkItem(value: unknown): value is BenchmarkItem {
  if (!isRecord(value)) return false;
  const requiredText = ['case_id', 'case_title', 'category', 'model', 'cli'];
  const optionalText = ['effort', 'error_message', 'evaluator_logs', 'raw_response'];
  const usage = value.token_usage;
  return requiredText.every((key) => typeof value[key] === 'string' && value[key] !== '')
    && optionalText.every((key) => value[key] == null || typeof value[key] === 'string')
    && typeof value.passed === 'boolean'
    && isNonnegativeNumber(value.duration_seconds)
    && isNonnegativeNumber(value.timestamp)
    && (value.metadata === undefined || isRecord(value.metadata))
    && isRecord(usage)
    && ['input_tokens', 'output_tokens', 'thinking_tokens', 'cache_read_tokens', 'total_tokens', 'estimated_cost_usd']
      .every((key) => isNonnegativeNumber(usage[key]));
}

export function readLocalReport(input: unknown) {
  const checkpoint = isRecord(input) && isRecord(input.metadata) ? input : null;
  const rows: unknown = checkpoint ? checkpoint.results : input;
  if (!Array.isArray(rows) || rows.length === 0 || !rows.every(isBenchmarkItem)) {
    throw new Error('Choose a benchmark JSON report or a checkpoint with saved results.');
  }

  const metadata = checkpoint?.metadata ?? rows[0].metadata;
  const runId = isRecord(metadata) && typeof metadata.run_id === 'string' ? metadata.run_id : null;
  const expected = checkpoint?.expected_keys;
  const keys = new Set(rows.map((item) => JSON.stringify([configurationKey(item), item.case_id])));
  if (keys.size !== rows.length || (!checkpoint && rows.some((item) => (item.metadata?.run_id ?? null) !== runId))) {
    throw new Error('Choose one run with a single result per case and model configuration.');
  }
  if (checkpoint && (!Array.isArray(expected) || expected.length < rows.length)) {
    throw new Error('The checkpoint does not have a valid execution plan.');
  }
  return {
    rows,
    runId,
    startedAt: isRecord(metadata) && typeof metadata.started_at_utc === 'string' ? metadata.started_at_utc : null,
    planned: Array.isArray(expected) ? expected.length : rows.length,
    reevaluated: rows.filter((item) => isRecord(item.metadata?.offline_reevaluation)).length,
  };
}
