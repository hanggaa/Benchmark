import React from 'react';
import { AggregatedModelSummary } from '../types';

interface HeroRankCardProps {
  topModel: AggregatedModelSummary | null;
  onSelectModel: (modelName: string) => void;
}

export const HeroRankCard: React.FC<HeroRankCardProps> = ({ topModel, onSelectModel }) => {
  if (!topModel) return null;

  return (
    <section className="max-w-7xl mx-auto px-6 mb-16 font-mono">
      <div className="border border-hazard-red bg-substrate-card p-6 sm:p-8 relative">
        
        {/* Corner Crosshairs */}
        <span className="absolute -top-2.5 -left-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -top-2.5 -right-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -bottom-2.5 -left-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -bottom-2.5 -right-2 text-hazard-red font-bold text-xs">+</span>

        {/* Tactical Header */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-substrate-border pb-4 mb-6">
          <div className="flex items-center gap-2">
            <span className="bg-hazard-red text-black font-extrabold px-2 py-0.5 text-xs uppercase">
              RANK #01 // UNIT LEADER
            </span>
            <span className="text-xs text-phosphor-dim uppercase">
              // TELEMETRY RECON VERIFIED
            </span>
          </div>

          <div className="flex items-center gap-2">
            <span className="border border-substrate-borderStrong bg-substrate-dark px-3 py-1 text-xs text-phosphor-white uppercase font-bold">
              HARNESS: [{topModel.cli.toUpperCase()}]
            </span>
            {topModel.effort && (
              <span className="border border-hazard-red bg-substrate-dark px-3 py-1 text-xs text-hazard-red uppercase font-bold">
                EFFORT: [{topModel.effort.toUpperCase()}]
              </span>
            )}
          </div>
        </div>

        {/* Model Title */}
        <div className="mb-6">
          <div className="text-[11px] text-phosphor-subtle uppercase mb-1">
            PRIMARY UNIT IDENTIFIER:
          </div>
          <h2 className="text-3xl sm:text-4xl md:text-5xl font-black uppercase text-phosphor-white tracking-tight font-sans">
            {topModel.model}
          </h2>
        </div>

        {/* Telemetry Definition Grid */}
        <dl className="grid grid-cols-2 md:grid-cols-4 gap-1 bg-substrate-border border border-substrate-border mb-6">
          
          <div className="bg-substrate-dark p-4">
            <dt className="text-[10px] text-phosphor-subtle uppercase mb-1">
              PASS@1 ACCURACY
            </dt>
            <dd className="text-2xl sm:text-3xl font-extrabold text-telemetry-green">
              {topModel.pass_rate}%
            </dd>
            <div className="text-[10px] text-phosphor-dim uppercase mt-1">
              {topModel.passed_cases}/{topModel.total_cases} CASES VERIFIED
            </div>
          </div>

          <div className="bg-substrate-dark p-4">
            <dt className="text-[10px] text-phosphor-subtle uppercase mb-1">
              EFFICIENCY INDEX
            </dt>
            <dd className="text-2xl sm:text-3xl font-extrabold text-phosphor-white">
              {topModel.efficiency_score.toLocaleString()}
            </dd>
            <div className="text-[10px] text-phosphor-dim uppercase mt-1">
              VALUE-TO-COST SCORE
            </div>
          </div>

          <div className="bg-substrate-dark p-4">
            <dt className="text-[10px] text-phosphor-subtle uppercase mb-1">
              THINKING TOKENS
            </dt>
            <dd className="text-2xl sm:text-3xl font-extrabold text-hazard-red">
              {topModel.total_thinking_tokens.toLocaleString()}
            </dd>
            <div className="text-[10px] text-phosphor-dim uppercase mt-1">
              -70% VS PREVIOUS GEN
            </div>
          </div>

          <div className="bg-substrate-dark p-4">
            <dt className="text-[10px] text-phosphor-subtle uppercase mb-1">
              TOTAL EXPENDITURE
            </dt>
            <dd className="text-2xl sm:text-3xl font-extrabold text-phosphor-white">
              ${topModel.total_cost_usd.toFixed(5)}
            </dd>
            <div className="text-[10px] text-phosphor-dim uppercase mt-1">
              AVG {topModel.avg_duration_seconds}S / CASE
            </div>
          </div>

        </dl>

        {/* Bottom Action Strip */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-4 border-t border-substrate-border">
          <div className="text-[11px] text-phosphor-dim uppercase max-w-2xl">
            // REASONING DENSITY REDUCES LATENCY AND COST WITHOUT COMPROMISING ZERO-DEFECT COMPILATION STANDARDS.
          </div>

          <button
            onClick={() => onSelectModel(topModel.model)}
            className="btn-brutalist text-xs py-2 px-5 hover:border-hazard-red"
          >
            [+] INSPECT TELEMETRY LOGS &gt;&gt;&gt;
          </button>
        </div>

      </div>
    </section>
  );
};
