import { useState } from 'react';
import { configurationKey, configurationName, cost } from '../reportData';
import type { AggregatedModelSummary } from '../types';

const colors = ['#9ae0c2', '#afb4ff', '#ffcb87', '#eaa4ce', '#94cdec', '#d9e79e'];
const fmt = (value: number) => Number(value.toFixed(1)) + '%';
const firstRate = (row: AggregatedModelSummary) =>
  row.first_attempt_passes === null ? null : row.first_attempt_passes / row.attempted_cases * 100;
const avgCost = (row: AggregatedModelSummary) => row.total_cost_usd / row.attempted_cases;

export function BenchmarkResults({ summaries }: { summaries: AggregatedModelSummary[] }) {
  const firstRecorded = summaries.some((summary) => firstRate(summary) !== null);
  const [metric, setMetric] = useState<'first' | 'scored'>(firstRecorded ? 'first' : 'scored');
  const [active, setActive] = useState<string | null>(null);
  const score = (row: AggregatedModelSummary) =>
    metric === 'first' ? firstRate(row) : row.total_cases ? row.pass_rate : null;

  const maxCost = Math.max(0.01, ...summaries.map(avgCost));
  const stepSize = 10 ** Math.floor(Math.log10(maxCost));
  const costLimit = Math.ceil(maxCost / stepSize) * stepSize;
  const chartItems = summaries.flatMap((row, i) => {
    const value = score(row);
    return value === null ? [] : [{ row, value, color: colors[i % colors.length] }];
  });
  const sorted = [...summaries].sort((a, b) =>
    (score(b) ?? -1) - (score(a) ?? -1) || avgCost(a) - avgCost(b)
  );
  const selected = chartItems.find(({ row }) => configurationKey(row) === active);

  return (
    <>
      <section className="section">
        <div className="section-heading">
          <div><h2>Performance vs. cost</h2><p>Each point is a model, CLI, and effort configuration.</p></div>
          <div className="segmented" aria-label="Chart metric">
            <button type="button" aria-pressed={metric === 'first'} disabled={!firstRecorded}
              onClick={() => setMetric('first')}>First attempt</button>
            <button type="button" aria-pressed={metric === 'scored'}
              onClick={() => setMetric('scored')}>Scored accuracy</button>
          </div>
        </div>
        <div className="panel chart-panel">
          <p className="chart-title">{metric === 'first' ? 'First-attempt success' : 'Scored accuracy'}</p>
          <div className="chart">
            <div className="y-axis" aria-hidden="true">
              {[100, 75, 50, 25, 0].map((n) => <span key={n}>{n}%</span>)}
            </div>
            <div className="plot">
              {chartItems.map(({ row, value, color }) => {
                const key = configurationKey(row);
                return (
                  <button type="button" key={key} className="point" aria-pressed={active === key}
                    style={{ left: avgCost(row) / costLimit * 100 + '%', bottom: value + '%', backgroundColor: color }}
                    aria-label={row.model + ', ' + row.cli + ', ' + fmt(value) + ', ' + cost.format(avgCost(row))}
                    onClick={() => setActive(key)} />
                );
              })}
              {chartItems.length === 0 && <span className="chart-empty">No scores available for this metric</span>}
            </div>
            <div className="x-axis" aria-hidden="true">
              {[0, 1, 2, 3, 4].map((i) => <span key={i}>{cost.format(costLimit * i / 4)}</span>)}
            </div>
          </div>
          <p className="axis-caption">Avg. recorded API-equivalent cost per case</p>
          <div className="chart-legend" aria-label="Model configurations">
            {chartItems.map(({ row, color }) => {
              const key = configurationKey(row);
              return (
                <button type="button" key={key} onClick={() => setActive(key)} aria-pressed={active === key}>
                  <span className="legend-dot" style={{ background: color }} aria-hidden="true" />
                  {configurationName(row.model, row.effort)} <small>{row.cli}{row.effort ? ' · ' + row.effort : ''}</small>
                </button>
              );
            })}
          </div>
          {selected && (
            <p className="chart-selection" role="status">
              {selected.row.model} · {fmt(selected.value)} · {cost.format(avgCost(selected.row))} per case
              {!selected.row.telemetry_complete && ' · partial telemetry'}
            </p>
          )}
        </div>
      </section>
      <section className="section ranking">
        <div className="section-heading"><div><h2>Model rankings</h2><p>Ranked by the selected score.</p></div></div>
        <div className="panel table-scroll" role="region" aria-label="Model rankings" tabIndex={0}>
          <table className="rank-table">
            <thead><tr><th scope="col">Configuration</th><th scope="col">First attempt</th>
              <th scope="col">Scored accuracy</th><th scope="col">CLI errors</th><th scope="col">Avg. cost</th></tr></thead>
            <tbody>
              {sorted.map((row) => (
                <tr key={configurationKey(row)}>
                  <th scope="row">{configurationName(row.model, row.effort)}
                    <small>{row.cli}{row.effort ? ' · ' + row.effort : ''}</small></th>
                  <td>{row.first_attempt_passes === null ? '—' : row.first_attempt_passes + '/' + row.attempted_cases}</td>
                  <td>{row.total_cases ? fmt(row.pass_rate) : '—'}<small>{row.passed_cases}/{row.total_cases} scored</small></td>
                  <td>{row.cli_error_cases}</td>
                  <td>{cost.format(avgCost(row))}{!row.telemetry_complete && <small>Partial</small>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </>
  );
}
