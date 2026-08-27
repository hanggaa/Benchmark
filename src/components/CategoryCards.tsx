import React from 'react';

export const CategoryCards: React.FC = () => {
  const modules = [
    {
      code: 'MOD-01',
      title: 'LOGIC & CONCURRENCY ENGINE',
      cases: '04 SCENARIOS',
      desc: 'Thread-safe LRU Cache with TTL eviction, Topological DAG Cycle Detection, Sliding Window Rate Limiter, and Async Priority Worker Pool with graceful drain.',
      standard: 'ZERO RACE CONDITIONS'
    },
    {
      code: 'MOD-02',
      title: 'SECURITY & VULNERABILITY INTERCEPT',
      cases: '02 SCENARIOS',
      desc: 'Eliminating JWT none-algorithm exploits and boundary expiration flaws, plus linearizing Catastrophic ReDoS Backtracking under 50,000-character evil payloads.',
      standard: 'O(N) LINEAR GUARANTEE'
    },
    {
      code: 'MOD-03',
      title: 'ARCHITECTURE & DEEP RESEARCH',
      cases: '02 SCENARIOS',
      desc: 'Automated Product Requirement Document (PRD) generation strictly following mandatory machine-readable Handoff Context blocks, and 10M Vector DB comparison matrices.',
      standard: 'STRICT SCHEMA ADHERENCE'
    },
    {
      code: 'MOD-04',
      title: 'SURGICAL CODE DIFF REFACTOR',
      cases: '01 SCENARIO',
      desc: 'Refactoring connection pools with self-healing auto-recovery while guaranteeing 100% method signature parity and zero docstring corruption.',
      standard: 'MINIMAL CODE CHURN'
    },
  ];

  return (
    <section className="max-w-7xl mx-auto px-6 py-12 font-mono" id="modules">
      <div className="border border-substrate-borderStrong bg-substrate-card p-6 mb-1">
        <div className="text-[11px] text-hazard-red font-bold uppercase tracking-widest mb-1">
          // TELEMETRY RECON 03 // MODULE BLUEPRINTS
        </div>
        <h2 className="text-2xl sm:text-3xl font-black uppercase text-phosphor-white font-sans">
          OPERATIONAL TEST MODULE BLUEPRINTS
        </h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-1 bg-substrate-border border border-substrate-border">
        {modules.map((mod, idx) => (
          <div
            key={idx}
            className="bg-substrate-card p-6 border border-substrate-border hover:border-hazard-red transition-all"
          >
            <div className="flex items-center justify-between mb-4 border-b border-substrate-border pb-2">
              <span className="bg-hazard-red text-black font-extrabold px-2 py-0.5 text-xs">
                [{mod.code}]
              </span>
              <span className="text-[11px] text-phosphor-dim uppercase font-bold">
                {mod.cases}
              </span>
            </div>

            <h3 className="text-sm font-bold text-phosphor-white uppercase mb-2">
              {mod.title}
            </h3>

            <p className="text-xs text-phosphor-dim uppercase leading-relaxed mb-4">
              {mod.desc}
            </p>

            <div className="pt-3 border-t border-substrate-border flex items-center justify-between text-[10px] uppercase">
              <span className="text-phosphor-subtle">TARGET STANDARD:</span>
              <span className="text-telemetry-green font-bold">[{mod.standard}]</span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};
