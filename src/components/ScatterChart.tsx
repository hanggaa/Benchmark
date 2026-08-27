import React from 'react';
import { AggregatedModelSummary } from '../types';

interface ScatterChartProps {
  summaries: AggregatedModelSummary[];
}

export const ScatterChart: React.FC<ScatterChartProps> = ({ summaries }) => {
  if (!summaries || summaries.length === 0) return null;

  const maxCost = Math.max(...summaries.map((s) => s.total_cost_usd), 0.1);

  return (
    <section className="max-w-7xl mx-auto px-6 py-12 font-mono" id="telemetry">
      <div className="border border-substrate-borderStrong bg-substrate-card p-6 sm:p-8">
        
        {/* Header */}
        <div className="flex flex-wrap items-end justify-between gap-4 border-b border-substrate-border pb-4 mb-6">
          <div>
            <div className="text-[11px] text-hazard-red font-bold uppercase tracking-widest mb-1">
              // TELEMETRY RECON 02 // EFFICIENCY OSCILLOSCOPE
            </div>
            <h3 className="text-2xl sm:text-3xl font-black uppercase text-phosphor-white font-sans">
              COST VS ACCURACY EFFICIENCY LANDSCAPE
            </h3>
          </div>
          <div className="text-[10px] text-phosphor-subtle uppercase">
            [ PARAMETER: MINIMUM BURNOUT / MAXIMUM PASS ]
          </div>
        </div>

        {/* Tactical Telemetry Gauges Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {summaries.map((s, idx) => {
            const passPct = s.pass_rate;
            const costRatio = Math.min((s.total_cost_usd / maxCost) * 100, 100);

            return (
              <div
                key={idx}
                className="border border-substrate-border bg-substrate-dark p-4 sm:p-5"
              >
                <div className="flex items-center justify-between pb-3 mb-3 border-b border-substrate-border">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-phosphor-white uppercase">
                      {s.model}
                    </span>
                    <span className="text-[10px] bg-substrate-elevated px-1.5 py-0.5 border border-substrate-border text-phosphor-dim uppercase">
                      {s.cli}
                    </span>
                  </div>
                  <span className="text-xs font-bold text-hazard-red">
                    SCORE: {s.efficiency_score.toLocaleString()}
                  </span>
                </div>

                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between text-[10px] uppercase text-phosphor-subtle mb-1">
                      <span>PASS@1 VERIFICATION:</span>
                      <span className="text-phosphor-white font-bold">{passPct}% ({s.passed_cases}/{s.total_cases})</span>
                    </div>
                    <div className="h-2 w-full bg-[#18181B] border border-substrate-border">
                      <div
                        className="h-full bg-telemetry-green transition-all duration-500"
                        style={{ width: `${passPct}%` }}
                      />
                    </div>
                  </div>

                  <div>
                    <div className="flex justify-between text-[10px] uppercase text-phosphor-subtle mb-1">
                      <span>RELATIVE EXPENDITURE BURNOUT:</span>
                      <span className="text-phosphor-white font-bold">${s.total_cost_usd.toFixed(5)}</span>
                    </div>
                    <div className="h-2 w-full bg-[#18181B] border border-substrate-border">
                      <div
                        className="h-full bg-hazard-red transition-all duration-500"
                        style={{ width: `${costRatio}%` }}
                      />
                    </div>
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-substrate-border flex items-center justify-between text-[10px] text-phosphor-dim uppercase">
                  <span>THINKING: {s.total_thinking_tokens.toLocaleString()} TOK</span>
                  <span>AVG LATENCY: {s.avg_duration_seconds}S</span>
                </div>
              </div>
            );
          })}
        </div>

      </div>
    </section>
  );
};
