import { useMemo, useState } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { HeroRankCard } from './components/HeroRankCard';
import { LeaderboardTable } from './components/LeaderboardTable';
import { ScatterChart } from './components/ScatterChart';
import { CategoryCards } from './components/CategoryCards';
import { CLIQuickStart } from './components/CLIQuickStart';
import { CaseInspectorModal } from './components/CaseInspectorModal';
import { Footer } from './components/Footer';

import rawBenchmarkData from './data/benchmark-data.json';
import { AggregatedModelSummary, BenchmarkItem } from './types';
import { aggregateBenchmarks } from './benchmarkSummary';

export function App() {
  const [selectedCase, setSelectedCase] = useState<BenchmarkItem | null>(null);

  const benchmarkItems: BenchmarkItem[] = useMemo(() => {
    return rawBenchmarkData as BenchmarkItem[];
  }, []);

  // Aggregate model summaries
  const summaries: AggregatedModelSummary[] = useMemo(() => {
    return aggregateBenchmarks(benchmarkItems);
  }, [benchmarkItems]);

  const topModel = summaries.length > 0 ? summaries[0] : null;
  const totalCases = new Set(benchmarkItems.map((item) => item.case_id)).size;

  return (
    <div className="min-h-screen bg-[#050507] text-[#ededed] relative selection:bg-emerald-500/20 selection:text-emerald-300">
      
      {/* Background ambient radial mesh */}
      <div className="fixed inset-0 bg-grain pointer-events-none -z-10" />
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[500px] bg-gradient-to-b from-emerald-500/[0.04] via-indigo-500/[0.02] to-transparent blur-[160px] pointer-events-none -z-10" />

      {/* Floating Navbar */}
      <Navbar totalRuns={benchmarkItems.length} totalModels={summaries.length} />

      {/* Main Content */}
      <main>
        <Hero
          totalCases={totalCases}
        />

        <HeroRankCard
          topModel={topModel}
          onSelectModel={() => {
            const el = document.getElementById('leaderboard');
            el?.scrollIntoView({ behavior: 'smooth' });
          }}
        />

        <LeaderboardTable
          summaries={summaries}
          benchmarkItems={benchmarkItems}
          onOpenCase={(c) => setSelectedCase(c)}
        />

        <ScatterChart summaries={summaries} />

        <CategoryCards />

        <CLIQuickStart />
      </main>

      {/* Footer */}
      <Footer />

      {/* Modal Inspector */}
      {selectedCase && (
        <CaseInspectorModal
          item={selectedCase}
          onClose={() => setSelectedCase(null)}
        />
      )}
    </div>
  );
}

export default App;
