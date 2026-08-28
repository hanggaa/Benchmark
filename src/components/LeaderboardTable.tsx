import React, { useState } from 'react';
import { AggregatedModelSummary, BenchmarkItem } from '../types';

interface LeaderboardTableProps {
  summaries: AggregatedModelSummary[];
  benchmarkItems: BenchmarkItem[];
  onOpenCase: (item: BenchmarkItem) => void;
}

type SortField = 'pass_rate' | 'efficiency_score' | 'avg_duration_seconds' | 'total_thinking_tokens' | 'total_cost_usd';

export const LeaderboardTable: React.FC<LeaderboardTableProps> = ({
  summaries,
  benchmarkItems,
  onOpenCase,
}) => {
  const [selectedCli, setSelectedCli] = useState<string>('all');
  const [sortField, setSortField] = useState<SortField>('pass_rate');
  const [sortAsc, setSortAsc] = useState<boolean>(false);
  const [expandedModel, setExpandedModel] = useState<string | null>(null);

  const clis = ['all', ...Array.from(new Set(summaries.map((s) => s.cli)))];

  const filteredSummaries = summaries
    .filter((s) => selectedCli === 'all' || s.cli.toLowerCase() === selectedCli.toLowerCase())
    .sort((a, b) => {
      if (sortField === 'pass_rate') {
        const diff = sortAsc ? a.pass_rate - b.pass_rate : b.pass_rate - a.pass_rate;
        if (diff !== 0) return diff;
        return b.efficiency_score - a.efficiency_score;
      }
      const valA = a[sortField] ?? 0;
      const valB = b[sortField] ?? 0;
      return sortAsc ? (valA > valB ? 1 : -1) : valA < valB ? 1 : -1;
    });

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(false);
    }
  };

  return (
    <section className="max-w-7xl mx-auto px-6 py-12 font-mono" id="leaderboard">
      
      {/* Section Header */}
      <div className="border border-substrate-borderStrong bg-substrate-card p-6 mb-1">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <div className="text-[11px] text-hazard-red font-bold uppercase tracking-widest mb-1">
              // TELEMETRY MATRIX // RECON DATA
            </div>
            <h2 className="text-2xl sm:text-3xl font-black uppercase text-phosphor-white font-sans">
              MODEL PERFORMANCE MATRIX
            </h2>
          </div>

          {/* Filter Bar */}
          <div className="flex flex-wrap items-center gap-1">
            <span className="text-[10px] uppercase text-phosphor-subtle mr-2">[HARNESS FILTER]:</span>
            {clis.map((cli) => (
              <button
                key={cli}
                onClick={() => setSelectedCli(cli)}
                className={`px-3 py-1 text-xs uppercase font-bold border transition-colors ${
                  selectedCli === cli
                    ? 'bg-hazard-red text-black border-hazard-red'
                    : 'bg-substrate-dark text-phosphor-dim border-substrate-border hover:border-phosphor-white hover:text-phosphor-white'
                }`}
              >
                [{cli.toUpperCase()}]
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Brutalist Data Matrix Table */}
      <div className="border border-substrate-borderStrong bg-substrate-card overflow-x-auto">
        <table className="w-full text-left text-xs font-mono text-phosphor-white">
          
          <thead className="bg-[#141416] border-b border-substrate-borderStrong text-[10px] text-phosphor-dim uppercase tracking-wider">
            <tr>
              <th className="py-3 px-4 font-bold text-phosphor-white">ID // UNIT DESIGNATION</th>
              <th className="py-3 px-4 font-bold text-phosphor-white">HARNESS</th>
              <th
                onClick={() => handleSort('pass_rate')}
                className="py-3 px-4 font-bold text-phosphor-white cursor-pointer hover:text-hazard-red transition-colors"
              >
                PASS@1 ACCURACY
              </th>
              <th
                onClick={() => handleSort('total_thinking_tokens')}
                className="py-3 px-4 font-bold text-phosphor-white cursor-pointer hover:text-hazard-red transition-colors"
              >
                THINKING TOKENS
              </th>
              <th
                onClick={() => handleSort('avg_duration_seconds')}
                className="py-3 px-4 font-bold text-phosphor-white cursor-pointer hover:text-hazard-red transition-colors"
              >
                LATENCY (S)
              </th>
              <th
                onClick={() => handleSort('total_cost_usd')}
                className="py-3 px-4 font-bold text-phosphor-white cursor-pointer hover:text-hazard-red transition-colors"
              >
                COST ($)
              </th>
              <th
                onClick={() => handleSort('efficiency_score')}
                className="py-3 px-4 font-bold text-phosphor-white cursor-pointer hover:text-hazard-red transition-colors text-right"
              >
                EFFICIENCY INDEX
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-substrate-border">
            {filteredSummaries.map((s, idx) => {
              const isExpanded = expandedModel === s.model;
              const modelRuns = benchmarkItems.filter((b) => b.model === s.model && b.cli === s.cli);

              return (
                <React.Fragment key={`${s.model}-${s.cli}-${idx}`}>
                  <tr
                    onClick={() => setExpandedModel(isExpanded ? null : s.model)}
                    className="cursor-pointer hover:bg-substrate-elevated transition-colors group"
                  >
                    {/* Model ID */}
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <span className="text-phosphor-subtle font-bold">
                          [{String(idx + 1).padStart(2, '0')}]
                        </span>
                        <div>
                          <div className="font-bold text-phosphor-white group-hover:text-hazard-red transition-colors uppercase">
                            {s.model}
                          </div>
                          <div className="text-[10px] text-phosphor-subtle uppercase">
                            {s.total_cases} SCENARIOS PROCESSED
                          </div>
                        </div>
                      </div>
                    </td>

                    {/* Harness */}
                    <td className="py-3 px-4 text-[11px] uppercase text-phosphor-dim">
                      [{s.cli}]
                    </td>

                    {/* Pass Rate */}
                    <td className="py-3 px-4">
                      <span className={`font-bold ${
                        s.pass_rate >= 90 ? 'text-telemetry-green' : s.pass_rate > 0 ? 'text-amber-400' : 'text-hazard-red'
                      }`}>
                        [{s.pass_rate}% // {s.passed_cases}/{s.total_cases}]
                      </span>
                    </td>

                    {/* Thinking Tokens */}
                    <td className="py-3 px-4 text-phosphor-dim">
                      {s.total_thinking_tokens.toLocaleString()} TOK
                    </td>

                    {/* Latency */}
                    <td className="py-3 px-4 text-phosphor-dim">
                      {s.avg_duration_seconds}S
                    </td>

                    {/* Cost */}
                    <td className="py-3 px-4 text-phosphor-white font-bold">
                      ${s.total_cost_usd.toFixed(5)}
                    </td>

                    {/* Efficiency Score */}
                    <td className="py-3 px-4 text-right font-black text-phosphor-white">
                      {s.efficiency_score.toLocaleString()}
                    </td>
                  </tr>

                  {/* Expanded Telemetry Drawer */}
                  {isExpanded && (
                    <tr className="bg-[#0D0D0E]">
                      <td colSpan={7} className="p-6 border-y border-substrate-borderStrong">
                        <div className="text-[11px] text-hazard-red font-bold uppercase mb-4">
                          /// DECLASSIFIED TELEMETRY DEBRIEF // UNIT: [{s.model}]
                        </div>
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
                          {modelRuns.map((run, rIdx) => (
                            <div
                              key={rIdx}
                              onClick={(e) => {
                                e.stopPropagation();
                                onOpenCase(run);
                              }}
                              className="border border-substrate-border bg-substrate-dark p-3 cursor-pointer hover:border-hazard-red transition-all"
                            >
                              <div className="flex items-center justify-between text-[10px] font-bold mb-1">
                                <span className={run.passed ? 'text-telemetry-green' : 'text-hazard-red'}>
                                  [{run.passed ? 'VERIFIED ✓' : 'FAILED ✗'}]
                                </span>
                                <span className="text-phosphor-subtle">{run.duration_seconds.toFixed(2)}S</span>
                              </div>
                              <div className="text-[11px] font-bold text-phosphor-white uppercase truncate">
                                {run.case_title}
                              </div>
                              <div className="flex justify-between text-[10px] text-phosphor-subtle mt-2 pt-2 border-t border-substrate-border">
                                <span>THINK: {run.token_usage.thinking_tokens.toLocaleString()}</span>
                                <span className="text-phosphor-white">${run.token_usage.estimated_cost_usd.toFixed(4)}</span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      </div>

    </section>
  );
};
