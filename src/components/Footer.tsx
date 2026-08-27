import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-substrate-borderStrong bg-[#0A0A0A] py-12 px-6 font-mono text-xs">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-phosphor-dim uppercase">
        
        {/* Left Branding */}
        <div className="flex items-center gap-3">
          <span className="bg-hazard-red text-black font-extrabold px-1.5 py-0.5 text-[11px]">
            BENCHMARK
          </span>
          <span className="text-phosphor-white font-bold">
            HANGGAA.XYZ // PROTOCOL REV-2026
          </span>
        </div>

        {/* Right Links */}
        <div className="flex items-center gap-6 text-[10px]">
          <a
            href="https://github.com/hanggaa/Benchmark"
            target="_blank"
            rel="noreferrer"
            className="hover:text-hazard-red transition-colors"
          >
            [ GITHUB REPOSITORY ↗ ]
          </a>
          <a
            href="https://hanggaa.xyz"
            target="_blank"
            rel="noreferrer"
            className="hover:text-hazard-red transition-colors"
          >
            [ HANGGAA.XYZ ↗ ]
          </a>
        </div>

      </div>
    </footer>
  );
};
