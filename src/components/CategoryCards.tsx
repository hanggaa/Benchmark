import React from 'react';

export const CategoryCards: React.FC = () => {
  const modules = [
    {
      code: 'MOD-01',
      title: 'LOGIC & CONCURRENCY ENGINE',
      cases: '06 SCENARIOS',
      desc: 'Caches, dependency graphs, rate limiting, async workers, quorum state machines, and zero-copy binary parsing.',
      standard: 'ZERO RACE CONDITIONS'
    },
    {
      code: 'MOD-02',
      title: 'SECURITY & VULNERABILITY INTERCEPT',
      cases: '04 SCENARIOS',
      desc: 'JWT and ReDoS repairs plus adversarial token inversion and SQL injection interception.',
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
      cases: '02 SCENARIOS',
      desc: 'Self-healing connection pools and AST-based dead-code pruning with public API preservation.',
      standard: 'MINIMAL CODE CHURN'
    },
    {
      code: 'MOD-05',
      title: 'DEFENSIVE SECURITY CONTROLS',
      cases: '02 SCENARIOS',
      desc: 'Secure archive extraction and fail-closed multi-tenant authorization under adversarial inputs.',
      standard: 'DENY BY DEFAULT'
    },
    {
      code: 'MOD-06',
      title: 'STATEFUL SYSTEM RECOVERY',
      cases: '02 SCENARIOS',
      desc: 'Out-of-order payment ledger reconciliation and crash-recoverable saga compensation.',
      standard: 'EXACTLY-ONCE EFFECTS'
    },
    {
      code: 'MOD-07',
      title: 'AGENTIC REPOSITORY OPERATIONS',
      cases: '02 SCENARIOS',
      desc: 'Multi-file regression repair and indirect prompt-injection resistance in isolated fixtures.',
      standard: 'SCOPED VERIFIED DIFF'
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
