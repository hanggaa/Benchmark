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

export function App() {
  const [selectedCase, setSelectedCase] = useState<BenchmarkItem | null>(null);

  const benchmarkItems: BenchmarkItem[] = useMemo(() => {
    return rawBenchmarkData as BenchmarkItem[];
  }, []);

  // Aggregate model summaries
  const summaries: AggregatedModelSummary[] = useMemo(() => {
    const grouped = new Map<string, BenchmarkItem[]>();

    for (const item of benchmarkItems) {
      const key = `${item.model}___${item.cli}`;
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key)!.push(item);
    }

    const res: AggregatedModelSummary[] = [];

    grouped.forEach((items, key) => {
      const [model, cli] = key.split('___');
      const total = items.length;
      const passed = items.filter((i) => i.passed).length;
      const passRate = total > 0 ? Math.round((passed / total) * 1000) / 10 : 0;
      const avgDuration = total > 0 ? Math.round((items.reduce((acc, i) => acc + i.duration_seconds, 0) / total) * 100) / 100 : 0;
      const totalIn = items.reduce((acc, i) => acc + (i.token_usage?.input_tokens || 0), 0);
      const totalOut = items.reduce((acc, i) => acc + (i.token_usage?.output_tokens || 0), 0);
      const totalThink = items.reduce((acc, i) => acc + (i.token_usage?.thinking_tokens || 0), 0);
      const totalCost = Math.round(items.reduce((acc, i) => acc + (i.token_usage?.estimated_cost_usd || 0), 0) * 100000) / 100000;
      
      const timeoutCount = items.filter(
        (it) => it.error_message?.includes('TIMEOUT') || it.error_message?.includes('Timed out') || (!it.passed && it.duration_seconds >= 120)
      ).length;
      const timeoutPenalty = timeoutCount * 0.05;

      // Quadratic Accuracy Efficiency Index: (PassRate^2 / 100) / (Cost + TimeoutPenalty + 0.005)
      const effScore = Math.round(((passRate * passRate) / 100.0) / (totalCost + timeoutPenalty + 0.005));

      const categoryMap: Record<string, { passed: number; total: number; rate: number }> = {};
      items.forEach((it) => {
        const cat = it.category || 'other';
        if (!categoryMap[cat]) categoryMap[cat] = { passed: 0, total: 0, rate: 0 };
        categoryMap[cat].total += 1;
        if (it.passed) categoryMap[cat].passed += 1;
      });

      Object.keys(categoryMap).forEach((c) => {
        categoryMap[c].rate = Math.round((categoryMap[c].passed / categoryMap[c].total) * 100);
      });

      res.push({
        model,
        cli,
        effort: items[0]?.effort || null,
        total_cases: total,
        passed_cases: passed,
        pass_rate: passRate,
        avg_duration_seconds: avgDuration,
        total_input_tokens: totalIn,
        total_output_tokens: totalOut,
        total_thinking_tokens: totalThink,
        total_cost_usd: totalCost,
        efficiency_score: effScore,
        category_pass_rates: categoryMap,
      });
    });

    return res.sort((a, b) => b.pass_rate - a.pass_rate || b.efficiency_score - a.efficiency_score);
  }, [benchmarkItems]);

  const topModel = summaries.length > 0 ? summaries[0] : null;

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
          topModelName={topModel?.model || 'Gemini 3.7 Flash'}
          topModelScore={topModel?.efficiency_score || 873}
          totalCases={benchmarkItems.length}
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
