import React, { useState } from 'react';

export const CLIQuickStart: React.FC = () => {
  const [copied, setCopied] = useState(false);
  const command = `python3 -m benchmarks.runner --models "Gemini 3.7 Flash (High), gpt-5.6-terra --effort high"`;

  const handleCopy = () => {
    navigator.clipboard.writeText(command);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <section className="max-w-7xl mx-auto px-6 py-12 font-mono" id="launch-console">
      <div className="border border-substrate-borderStrong bg-substrate-card p-6 sm:p-8">
        
        {/* Header */}
        <div className="flex flex-wrap items-end justify-between gap-4 border-b border-substrate-border pb-4 mb-6">
          <div>
            <div className="text-[11px] text-hazard-red font-bold uppercase tracking-widest mb-1">
              // TELEMETRY RECON 04 // DISPATCH CONTROL
            </div>
            <h3 className="text-2xl sm:text-3xl font-black uppercase text-phosphor-white font-sans">
              EXECUTE LOCAL BENCHMARK HARNESS
            </h3>
          </div>

          <button
            onClick={handleCopy}
            className="btn-brutalist-red text-xs py-2 px-5"
          >
            {copied ? '[ COMMAND COPIED ✓ ]' : '[+] COPY DISPATCH COMMAND'}
          </button>
        </div>

        <p className="text-xs text-phosphor-dim uppercase max-w-3xl leading-relaxed mb-6">
          DISPATCH THE BENCHMARK RUNNER ACROSS ALL YOUR INSTALLED CODING CLIS WITH AUTOMATIC TELEMETRY LOGGING AND LEADERBOARD SYNC.
        </p>

        {/* Terminal Window */}
        <div className="border border-substrate-borderStrong bg-substrate-dark p-4 font-mono text-xs text-phosphor-white overflow-x-auto">
          <div className="flex items-center justify-between pb-2 mb-3 border-b border-substrate-border text-[10px] text-phosphor-subtle uppercase">
            <span>TERMINAL INTERFACE // BASH DISPATCH</span>
            <span>STATUS: READY</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-hazard-red font-bold select-none">&gt;&gt;</span>
            <span className="text-phosphor-white">{command}</span>
          </div>
        </div>

        {/* 3-Column Industrial Technical Specs */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-1 mt-6 bg-substrate-border border border-substrate-border text-[10px] uppercase">
          <div className="bg-substrate-dark p-4">
            <strong className="text-phosphor-white block mb-1 font-bold">[01] AUTO-ROUTING ENGINE</strong>
            <span className="text-phosphor-dim">MODELS ARE DISPATCHED EXCLUSIVELY TO THEIR NATIVE CLI ADAPTERS.</span>
          </div>
          <div className="bg-substrate-dark p-4">
            <strong className="text-phosphor-white block mb-1 font-bold">[02] FULL TELEMETRY</strong>
            <span className="text-phosphor-dim">AUTOMATIC CAPTURE OF THINKING TOKENS, DURATIONS, AND REAL RUN COSTS.</span>
          </div>
          <div className="bg-substrate-dark p-4">
            <strong className="text-phosphor-white block mb-1 font-bold">[03] STATIC GITHUB PAGES</strong>
            <span className="text-phosphor-dim">DEPLOY IN ONE STEP USING <code className="text-hazard-red">npm run deploy</code>.</span>
          </div>
        </div>

      </div>
    </section>
  );
};
