import { configurationKey, configurationName, outcome, statusLabels } from '../reportData';
import type { AggregatedModelSummary, BenchmarkItem } from '../types';

interface Props {
  items: BenchmarkItem[];
  summaries: AggregatedModelSummary[];
  onInspect: (item: BenchmarkItem) => void;
}

export function ResultsMatrix({ items, summaries, onInspect }: Props) {
  const cases = new Map(items.map((item) => [item.case_id, item]));
  const byCase = new Map<string, Map<string, BenchmarkItem>>();
  for (const item of items) {
    if (!byCase.has(item.case_id)) byCase.set(item.case_id, new Map());
    byCase.get(item.case_id)?.set(configurationKey(item), item);
  }

  return (
    <section className="section">
      <div className="section-heading">
        <div><h2>Case outcomes</h2><p>Select a result to inspect the run.</p></div>
        <div className="status-legend">
          {Object.entries(statusLabels).map(([key, label]) => <span key={key} className={'status ' + key}>{label}</span>)}
        </div>
      </div>
      <div className="panel table-scroll matrix-scroll" role="region" aria-label="Case outcomes matrix" tabIndex={0}>
        <table className="matrix">
          <thead>
            <tr>
              <th scope="col">Benchmark case</th>
              {summaries.map((summary) => (
                <th scope="col" key={configurationKey(summary)}>
                  {configurationName(summary.model, summary.effort)}
                  <small>{summary.cli}{summary.effort ? ' · ' + summary.effort : ''}</small>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from(cases.values(), (benchmarkCase) => (
              <tr key={benchmarkCase.case_id}>
                <th scope="row">
                  <span>{benchmarkCase.case_title}</span>
                  <small>{benchmarkCase.category.replace(/_/g, ' ')}</small>
                </th>
                {summaries.map((summary) => {
                  const key = configurationKey(summary);
                  const item = byCase.get(benchmarkCase.case_id)?.get(key);
                  const status = item ? outcome(item) : null;
                  return (
                    <td key={key}>
                      {item && status ? (
                        <button type="button" className={'matrix-cell ' + status} onClick={() => onInspect(item)}
                          aria-label={statusLabels[status] + ' · ' + benchmarkCase.case_title + ' · ' + summary.model}>
                          {statusLabels[status]}
                        </button>
                      ) : <span className="matrix-cell missing">No result</span>}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
