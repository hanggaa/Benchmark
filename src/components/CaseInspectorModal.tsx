import React from 'react';
import { BenchmarkItem } from '../types';

interface CaseInspectorModalProps {
  item: BenchmarkItem | null;
  onClose: () => void;
}

export const CaseInspectorModal: React.FC<CaseInspectorModalProps> = ({ item, onClose }) => {
  if (!item) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/90 backdrop-blur-sm font-mono">
      <div className="relative w-full max-w-4xl max-h-[90vh] flex flex-col border border-hazard-red bg-substrate-card text-phosphor-white p-6 overflow-hidden">
        
        {/* Corner Crosshairs */}
        <span className="absolute -top-2.5 -left-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -top-2.5 -right-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -bottom-2.5 -left-2 text-hazard-red font-bold text-xs">+</span>
        <span className="absolute -bottom-2.5 -right-2 text-hazard-red font-bold text-xs">+</span>

        {/* Modal Header */}
        <div className="flex items-start justify-between gap-4 border-b border-substrate-border pb-4 mb-4 shrink-0">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2 py-0.5 text-xs font-bold uppercase ${
                item.passed ? 'bg-telemetry-green text-black' : 'bg-hazard-red text-black'
              }`}>
                {item.passed ? '✓ MISSION VERIFIED' : '✗ TELEMETRY FAILURE'}
              </span>
              <span className="text-[10px] border border-substrate-borderStrong px-2 py-0.5 uppercase text-phosphor-dim">
                MODULE: {item.category.toUpperCase()}
              </span>
            </div>
            <h3 className="text-lg sm:text-xl font-bold uppercase text-phosphor-white">
              {item.case_title}
            </h3>
            <p className="text-[10px] uppercase text-phosphor-dim mt-0.5">
              UNIT: <span className="text-phosphor-white font-bold">{item.model}</span> // HARNESS: <span className="text-phosphor-white font-bold">{item.cli}</span>
            </p>
          </div>

          <button
            onClick={onClose}
            className="border border-substrate-borderStrong bg-substrate-dark px-3 py-1 text-xs hover:bg-hazard-red hover:text-black hover:border-hazard-red transition-colors"
          >
            [ ESC // CLOSE ]
          </button>
        </div>

        {/* Telemetry Indicator Readout */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-1 bg-substrate-border border border-substrate-border mb-4 shrink-0 text-[10px] uppercase">
          <div className="bg-substrate-dark p-3">
            <span className="text-phosphor-subtle block mb-0.5">DURATION:</span>
            <span className="text-phosphor-white font-bold text-sm">{item.duration_seconds.toFixed(2)}S</span>
          </div>
          <div className="bg-substrate-dark p-3">
            <span className="text-phosphor-subtle block mb-0.5">THINKING TOKENS:</span>
            <span className="text-hazard-red font-bold text-sm">{item.token_usage.thinking_tokens.toLocaleString()}</span>
          </div>
          <div className="bg-substrate-dark p-3">
            <span className="text-phosphor-subtle block mb-0.5">OUTPUT TOKENS:</span>
            <span className="text-phosphor-white font-bold text-sm">{item.token_usage.output_tokens.toLocaleString()}</span>
          </div>
          <div className="bg-substrate-dark p-3">
            <span className="text-phosphor-subtle block mb-0.5">ESTIMATED COST:</span>
            <span className="text-phosphor-white font-bold text-sm">${item.token_usage.estimated_cost_usd.toFixed(5)}</span>
          </div>
        </div>

        {/* Terminal Logs & Output */}
        <div className="flex-1 overflow-y-auto space-y-4 pr-2 text-xs">
          {item.evaluator_logs && (
            <div>
              <div className="text-[10px] uppercase tracking-widest text-hazard-red font-bold mb-1">
                // SANDBOX EVALUATOR TELEMETRY:
              </div>
              <pre className={`p-3 border overflow-x-auto text-[11px] ${
                item.passed
                  ? 'bg-substrate-dark border-telemetry-green/40 text-telemetry-green'
                  : 'bg-substrate-dark border-hazard-red/40 text-hazard-red'
              }`}>
                {item.evaluator_logs}
              </pre>
            </div>
          )}

          {item.raw_response && (
            <div>
              <div className="text-[10px] uppercase tracking-widest text-phosphor-dim font-bold mb-1">
                // RAW GENERATED OUTPUT:
              </div>
              <pre className="p-3 border border-substrate-border bg-substrate-dark text-[11px] text-phosphor-dim overflow-x-auto whitespace-pre-wrap leading-relaxed">
                {item.raw_response}
              </pre>
            </div>
          )}
        </div>

      </div>
    </div>
  );
};
