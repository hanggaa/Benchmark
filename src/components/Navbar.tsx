import React from 'react';

interface NavbarProps {
  totalRuns: number;
  totalModels: number;
}

export const Navbar: React.FC<NavbarProps> = ({ totalRuns, totalModels }) => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-[#0A0A0A] border-b border-substrate-borderStrong font-mono">
      {/* Top Hazard Accent Bar */}
      <div className="h-1 w-full hazard-stripe-bar" />

      <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
        
        {/* System Identifier & Status */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="bg-hazard-red text-black font-extrabold px-2 py-0.5 text-xs tracking-wider uppercase">
              BENCHMARK // TACTICAL
            </span>
            <span className="text-xs font-bold text-phosphor-white tracking-widest uppercase hidden sm:inline">
              SYS-ID: B89-PROD
            </span>
          </div>

          <div className="hidden md:flex items-center gap-1.5 px-2 py-0.5 bg-substrate-elevated border border-substrate-border text-[10px] text-telemetry-green tracking-widest uppercase">
            <span className="h-1.5 w-1.5 bg-telemetry-green animate-ping" />
            LIVE TELEMETRY: ACTIVE
          </div>
        </div>

        {/* Tactical Nav Links */}
        <nav className="hidden lg:flex items-center gap-6 text-[11px] font-bold uppercase tracking-widest text-phosphor-dim">
          <a href="#leaderboard" className="hover:text-hazard-red transition-colors">
            [01. MATRIX]
          </a>
          <a href="#telemetry" className="hover:text-hazard-red transition-colors">
            [02. TELEMETRY]
          </a>
          <a href="#modules" className="hover:text-hazard-red transition-colors">
            [03. MODULES]
          </a>
          <a href="#launch-console" className="hover:text-hazard-red transition-colors">
            [04. DISPATCH]
          </a>
        </nav>

        {/* Right Telemetry Readout & Dispatch Button */}
        <div className="flex items-center gap-4">
          <div className="hidden sm:flex items-center gap-3 text-[10px] uppercase text-phosphor-dim border-r border-substrate-border pr-4">
            <span>FLIGHTS: <strong className="text-phosphor-white">{totalRuns}</strong></span>
            <span>UNITS: <strong className="text-phosphor-white">{totalModels}</strong></span>
          </div>

          <a
            href="#launch-console"
            className="btn-brutalist text-xs py-1.5 px-4 hover:border-hazard-red"
          >
            DISPATCH RUN &gt;&gt;&gt;
          </a>
        </div>

      </div>
    </header>
  );
};
