import { useEffect, useRef } from 'react';
import { X } from 'lucide-react';
import { cost, outcome, statusLabels } from '../reportData';
import type { BenchmarkItem } from '../types';

export function CaseInspectorModal({ item, onClose }: { item: BenchmarkItem; onClose: () => void }) {
  const dialog = useRef<HTMLDialogElement>(null);
  useEffect(() => {
    const element = dialog.current;
    if (!element || element.open) return;
    const trigger = document.activeElement;
    element.showModal();
    return () => {
      element.close();
      if (trigger instanceof HTMLElement) trigger.focus();
    };
  }, []);

  const status = outcome(item);
  const tokens = item.token_usage;
  const failureKind = item.metadata?.error_kind;
  const formatTokens = (count: number) => count.toLocaleString('en-US');
  const label = failureKind === 'workspace_policy_violation' ? 'Workspace policy violation'
    : failureKind === 'workspace_regression_failure' ? 'Workspace regression failure' : statusLabels[status];

  return (
    <dialog ref={dialog} className="case-dialog" aria-labelledby="case-title" onCancel={(event) => {
      event.preventDefault();
      onClose();
    }}>
      <header>
        <span className={'status ' + status}>{label}</span>
        <button type="button" className="button close-button" onClick={onClose} aria-label="Close case details" autoFocus>
          <X size={19} aria-hidden="true" />
        </button>
      </header>
      <h2 id="case-title">{item.case_title}</h2>
      <p>{item.model} · {item.cli}{item.effort ? ' · ' + item.effort : ''}</p>
      <dl className="inspector-stats">
        <div><dt>Duration</dt><dd>{item.duration_seconds.toFixed(2)} s</dd></div>
        <div><dt>Est. API cost</dt><dd>{cost.format(tokens.estimated_cost_usd)}{!tokens.telemetry_complete && ' (partial)'}</dd></div>
        <div><dt>Input</dt><dd>{formatTokens(tokens.input_tokens)}</dd></div>
        <div><dt>Output</dt><dd>{formatTokens(tokens.output_tokens)}</dd></div>
        <div><dt>Thinking</dt><dd>{formatTokens(tokens.thinking_tokens)}</dd></div>
        <div><dt>Cache read</dt><dd>{formatTokens(tokens.cache_read_tokens)}</dd></div>
      </dl>
      <h3>{item.error_message ? 'CLI error' : 'Evaluator log'}</h3>
      <pre>{item.error_message || item.evaluator_logs || 'No log recorded.'}</pre>
      {Boolean(item.metadata?.offline_reevaluation) && <p>Reevaluated offline using the saved response.</p>}
      {item.raw_response && <details><summary>Model response</summary><pre>{item.raw_response}</pre></details>}
    </dialog>
  );
}
