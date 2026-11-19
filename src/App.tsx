/// <reference types="vite/client" />

import { useEffect, useMemo, useRef, useState } from 'react';
import type { ChangeEvent } from 'react';
import { ArrowDownRight, ArrowUpRight, BarChart3 } from 'lucide-react';
import { aggregateBenchmarks } from './benchmarkSummary';
import { BenchmarkResults } from './components/BenchmarkResults';
import { ResultsMatrix } from './components/ResultsMatrix';
import { CaseInspectorModal } from './components/CaseInspectorModal';
import { readLocalReport } from './reportData';
import type { BenchmarkItem } from './types';
import fullData from './data/benchmark-data.json';
import coreData from './data/benchmark-data-core10-v1.json';

const repository = 'https://github.com/hanggaa/Benchmark';
const suites = [
  { id: 'full', label: 'Full suite', rows: fullData as BenchmarkItem[] },
  { id: 'core10-v1', label: 'Core 10 (v1)', rows: coreData as BenchmarkItem[] },
] as const;

const pages = [
  { id: 'leaderboard', route: '#/', label: 'Leaderboard' },
  { id: 'data', route: '#/data', label: 'Data' },
  { id: 'run', route: '#/run', label: 'Run' },
] as const;

const command = [
  'python3 -m benchmarks.runner \\',
  '  --suite core10-v1 \\',
  '  --models "Gemini 4 Neon (High), Gemini 4 Hydrogen (High), Gemini 4 Argon (High)" \\',
  '  --timeout 600',
].join('\n');

function getPage() {
  return pages.find((page) => page.route === window.location.hash)?.id ?? 'leaderboard';
}

export function App() {
  const [page, setPage] = useState(getPage);
  const [suite, setSuite] = useState('full');
  const [selectedCase, setSelectedCase] = useState<BenchmarkItem | null>(null);
  const [localReport, setLocalReport] = useState<ReturnType<typeof readLocalReport> | null>(null);
  const [uploadError, setUploadError] = useState('');
  const [copyStatus, setCopyStatus] = useState('');
  const uploadVersion = useRef(0);

  useEffect(() => {
    const handleHashChange = () => {
      setPage(getPage());
      setSelectedCase(null);
      window.scrollTo(0, 0);
    };
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const preview = import.meta.env.DEV && suite === 'local' ? localReport : null;
  const publishedSuite = suites.find((entry) => entry.id === suite) ?? suites[0];
  const items = preview?.rows ?? publishedSuite.rows;
  const summaries = useMemo(() => aggregateBenchmarks(items), [items]);
  const firstItem = items[0];
  const dateValue = preview?.startedAt ?? firstItem?.metadata?.started_at_utc;
  const date = typeof dateValue === 'string' ? new Date(dateValue) : null;
  const formattedDate = date && Number.isFinite(date.getTime())
    ? new Intl.DateTimeFormat('en-GB', { day: 'numeric', month: 'short', year: 'numeric', timeZone: 'UTC' }).format(date)
    : '—';
  const caseCount = new Set(items.map((item) => item.case_id)).size;

  async function loadReport(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    event.target.value = '';
    if (!file) return;
    const version = ++uploadVersion.current;
    try {
      const report = readLocalReport(JSON.parse(await file.text()));
      if (version !== uploadVersion.current) return;
      setLocalReport(report);
      setSelectedCase(null);
      setSuite('local');
      setUploadError('');
    } catch (error) {
      if (version === uploadVersion.current) {
        setUploadError(error instanceof SyntaxError ? 'This file contains invalid JSON.' :
          error instanceof Error ? error.message : 'The report could not be opened.');
      }
    }
  }

  async function copyCommand() {
    try {
      await navigator.clipboard.writeText(command);
      setCopyStatus('Copied');
    } catch {
      setCopyStatus('Select the command to copy it.');
    }
  }

  return (
    <>
      <header className="site-header">
        <div className="shell header-inner">
          <a className="brand" href="#/"><span className="brand-mark"><BarChart3 size={17} aria-hidden="true" /></span> Benchmark</a>
          <nav aria-label="Primary">
            {pages.map(({ id, route, label }) => (
              <a key={id} href={route} aria-current={page === id ? 'page' : undefined}>{label}</a>
            ))}
            <a className="source-link" href={repository} aria-label="GitHub repository"><ArrowUpRight size={17} aria-hidden="true" /></a>
          </nav>
        </div>
      </header>

      <main className="shell">
        {page === 'run' ? (
          <>
            <section className="page-intro">
              <div>
                <h1>Run a benchmark.</h1>
                <p>Compare the same model configurations across a fixed set of coding tasks.</p>
              </div>
            </section>
            <section className="section">
              <div className="section-heading"><div><h2>Run Core 10</h2><p>Three Gemini High configurations. Ten cases per model.</p></div>
                <button type="button" className="button" onClick={copyCommand}>Copy command</button>
              </div>
              <pre className="panel command">{command}</pre>
              <p role="status">{copyStatus}</p>
              <p>Run from the repository root with your CLI configured. Add <code>--dry-run</code> to check the execution plan. The runner saves a report and a checkpoint under <code>benchmarks/reports</code>.</p>
              <a className="text-link" href={repository + '/blob/main/benchmarks/README.md'}>Runner documentation <ArrowUpRight size={15} aria-hidden="true" /></a>
            </section>
          </>
        ) : (
          <>
            <section className="page-intro">
              <div>
                <h1>{page === 'data' ? 'Explore the results.' : 'LLM coding benchmark.'}</h1>
                <p>{page === 'data' ? 'Trace every case outcome to its evaluation log and token usage.' :
                  'Compare how coding agents perform across reproducible tasks, with cost and evidence for every result.'}</p>
                <a className="text-link" href={page === 'data' ? '#/' : '#/data'}>
                  {page === 'data' ? 'Back to leaderboard' : 'Explore the results'} <ArrowDownRight size={16} aria-hidden="true" />
                </a>
              </div>
              <dl className="run-stats">
                <div><dt>Cases recorded</dt><dd>{caseCount}</dd></div>
                <div><dt>Configurations</dt><dd>{summaries.length}</dd></div>
                <div><dt>Run date (UTC)</dt><dd>{formattedDate}</dd></div>
              </dl>
            </section>
            <div className="suite-bar">
              <div className="suite-control">
                <label htmlFor="benchmark-suite">Suite</label>
                <select id="benchmark-suite" value={suite} onChange={(event) => {
                  setSuite(event.target.value);
                  setSelectedCase(null);
                }}>
                  {suites.map((entry) => <option key={entry.id} value={entry.id}>{entry.label}</option>)}
                  {import.meta.env.DEV && localReport && <option value="local">Local preview</option>}
                </select>
              </div>
              {import.meta.env.DEV && (
                <label className="button file-control">
                  Open local report
                  <input aria-label="Open local report" type="file" accept=".json,application/json" onChange={loadReport} />
                </label>
              )}
            </div>
            {import.meta.env.DEV && uploadError && <p className="upload-error" role="alert">{uploadError}</p>}
            {preview && (
              <p className="preview-banner" role="status">
                <strong>Local preview</strong> · Run <code>{preview.runId ?? 'unrecorded'}</code> · {items.length}/{preview.planned} results
                {preview.reevaluated > 0 && ' · ' + preview.reevaluated + ' results reevaluated offline'}
              </p>
            )}
            {items.length === 0 ? (
              <section className="panel empty-state"><h2>Results pending</h2><p>This suite has no published results yet.</p></section>
            ) : page === 'data' ? (
              <ResultsMatrix items={items} summaries={summaries} onInspect={setSelectedCase} />
            ) : (
              <BenchmarkResults key={suite + (preview?.runId ?? '')} summaries={summaries} />
            )}
          </>
        )}

        <section className="methodology">
          <h2>Reading the results</h2>
          <dl>
            <div><dt>First attempt</dt><dd>Cases passed on the initial try divided by cases with recorded results. Older reports may lack attempt history.</dd></div>
            <div><dt>Scored accuracy</dt><dd>Cases passed divided by cases evaluated. CLI errors do not enter the denominator.</dd></div>
            <div><dt>Recorded cost</dt><dd>Estimated API-equivalent USD per recorded case. Retry costs from earlier attempts and subscription charges are outside this estimate.</dd></div>
          </dl>
        </section>
      </main>

      <footer className="site-footer">
        <div className="shell footer-inner"><span>Personal LLM Benchmark</span>
          <a href={repository}>Source code <ArrowUpRight size={14} aria-hidden="true" /></a></div>
      </footer>
      {selectedCase && <CaseInspectorModal item={selectedCase} onClose={() => setSelectedCase(null)} />}
    </>
  );
}

export default App;
