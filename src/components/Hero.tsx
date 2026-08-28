import React from 'react';

interface HeroProps {
  topModelName: string;
  topModelScore: number;
  totalCases: number;
}

export const Hero: React.FC<HeroProps> = () => {
  return (
    <section className="relative pt-28 pb-16 px-6 max-w-7xl mx-auto font-mono">
      
      {/* Background CRT Scanlines */}
      <div className="fixed inset-0 scanlines-overlay pointer-events-none z-40 opacity-30" />

      {/* Blueprint Header Frame */}
      <div className="border border-substrate-borderStrong bg-substrate-card p-6 sm:p-10 relative">
        
        {/* Crosshair markers at corners */}
        <span className="absolute -top-2.5 -left-2 text-hazard-red font-bold text-xs select-none">+</span>
        <span className="absolute -top-2.5 -right-2 text-hazard-red font-bold text-xs select-none">+</span>
        <span className="absolute -bottom-2.5 -left-2 text-hazard-red font-bold text-xs select-none">+</span>
        <span className="absolute -bottom-2.5 -right-2 text-hazard-red font-bold text-xs select-none">+</span>

        {/* Technical Eyebrow */}
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-substrate-border pb-4 mb-6">
          <div className="flex items-center gap-2 text-xs text-hazard-red font-bold uppercase tracking-widest">
            <span>/// SPECIFICATION: TACTICAL CODE BENCHMARK</span>
            <span className="text-phosphor-subtle">|</span>
            <span className="text-phosphor-dim">DOC-REF: #B89-2026</span>
          </div>
          <div className="text-[11px] text-phosphor-dim uppercase tracking-wider">
            SUBSTRATE: DEACTIVATED CRT // REV 3.7
          </div>
        </div>

        {/* Macro-Typography Header */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight-macro leading-macro uppercase text-phosphor-white font-sans mb-6">
          EMPIRICAL LLM <br />
          <span className="text-hazard-red">BENCHMARK MATRIX</span>
        </h1>

        <p className="text-xs sm:text-sm text-phosphor-dim uppercase tracking-wide-telemetry max-w-3xl leading-relaxed mb-8">
          RIGID DETERMINISTIC EVALUATION OF LARGE LANGUAGE MODEL CODING EFFICIENCY ACROSS ANTIGRAVITY CLI, OPENAI CODEX, AND OPENCODE HARNESSES.
        </p>

        {/* Tactical Action Strip */}
        <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-substrate-border">
          <a
            href="#leaderboard"
            className="btn-brutalist-red text-xs py-3 px-6"
          >
            [01] ACCESS LEADERBOARD MATRIX &gt;&gt;&gt;
          </a>
          <a
            href="#launch-console"
            className="btn-brutalist text-xs py-3 px-6"
          >
            [02] LOCAL CLI DISPATCH
          </a>
        </div>

      </div>

      {/* Telemetry Indicator Readout Grid (4-up) */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-1 mt-1 bg-substrate-border border border-substrate-border">
        
        <div className="bg-substrate-card p-4 sm:p-6">
          <div className="text-[10px] uppercase tracking-widest text-phosphor-subtle mb-1">
            // METRIC 01: SUITE SIZE
          </div>
          <div className="text-xl sm:text-2xl font-bold uppercase text-phosphor-white tracking-wide">
            14 SCENARIOS
          </div>
          <div className="text-[10px] text-phosphor-dim mt-1 uppercase">
            HIDDEN UNIT ASSERTIONS
          </div>
        </div>

        <div className="bg-substrate-card p-4 sm:p-6">
          <div className="text-[10px] uppercase tracking-widest text-phosphor-subtle mb-1">
            // METRIC 02: REASONING TELEMETRY
          </div>
          <div className="text-xl sm:text-2xl font-bold uppercase text-telemetry-green tracking-wide">
            TOKEN BURNOUT
          </div>
          <div className="text-[10px] text-phosphor-dim mt-1 uppercase">
            THINKING EFFICIENCY RATIO
          </div>
        </div>

        <div className="bg-substrate-card p-4 sm:p-6">
          <div className="text-[10px] uppercase tracking-widest text-phosphor-subtle mb-1">
            // METRIC 03: PASS@1 PROTOCOL
          </div>
          <div className="text-xl sm:text-2xl font-bold uppercase text-phosphor-white tracking-wide">
            100% DETERMINISTIC
          </div>
          <div className="text-[10px] text-phosphor-dim mt-1 uppercase">
            ZERO PUBLIC CONTAMINATION
          </div>
        </div>

        <div className="bg-substrate-card p-4 sm:p-6">
          <div className="text-[10px] uppercase tracking-widest text-phosphor-subtle mb-1">
            // METRIC 04: PLATFORM TARGET
          </div>
          <div className="text-xl sm:text-2xl font-bold uppercase text-hazard-red tracking-wide">
            HANGGAA.XYZ
          </div>
          <div className="text-[10px] text-phosphor-dim mt-1 uppercase">
            ORBITAL DEPLOYMENT
          </div>
        </div>

      </div>

    </section>
  );
};
