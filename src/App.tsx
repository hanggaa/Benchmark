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
      const key = JSON.stringify([item.model, item.cli, item.effort || null]);
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key)!.push(item);
    }

    const res: AggregatedModelSummary[] = [];

    grouped.forEach((items, key) => {
      const [model, cli, groupedEffort] = JSON.parse(key) as [string, string, string | null];
      const total = items.length;
      const passed = items.filter((i) => i.passed).length;
      const passRate = total > 0 ? Math.round((passed / total) * 1000) / 10 : 0;
      const difficultyWeight = (difficulty?: string) => (
        difficulty === 'hard' ? 3 : difficulty === 'easy' ? 1 : 2
      );
      const totalWeight = items.reduce((acc, item) => acc + difficultyWeight(item.difficulty), 0);
      const passedWeight = items.reduce(
        (acc, item) => acc + (item.passed ? difficultyWeight(item.difficulty) : 0),
        0,
      );
      const weightedPassRate = totalWeight > 0
        ? Math.round((passedWeight / totalWeight) * 1000) / 10
        : 0;
      const avgDuration = total > 0 ? Math.round((items.reduce((acc, i) => acc + i.duration_seconds, 0) / total) * 100) / 100 : 0;
      const totalIn = items.reduce((acc, i) => acc + (i.token_usage?.input_tokens || 0), 0);
      const totalOut = items.reduce((acc, i) => acc + (i.token_usage?.output_tokens || 0), 0);
      const totalThink = items.reduce((acc, i) => acc + (i.token_usage?.thinking_tokens || 0), 0);
      const totalCost = Math.round(items.reduce((acc, i) => acc + (i.token_usage?.estimated_cost_usd || 0), 0) * 100000) / 100000;
      
      const timeoutCount = items.filter((item) => {
        const timeoutText = `${item.error_message || ''}\n${item.evaluator_logs || ''}`.toLowerCase();
        return timeoutText.includes('timeout') || timeoutText.includes('timed out');
      }).length;
      const timeoutPenalty = timeoutCount * 0.05;

      const telemetryComplete = items.every((item) => {
        if (typeof item.token_usage?.telemetry_complete === 'boolean') {
          return item.token_usage.telemetry_complete;
        }
        return Boolean(
          item.token_usage?.input_tokens
          || item.token_usage?.output_tokens
          || item.token_usage?.thinking_tokens
          || item.token_usage?.estimated_cost_usd
        );
      });
      const effScore = telemetryComplete
        ? Math.round(((weightedPassRate * weightedPassRate) / 100.0) / (totalCost + timeoutPenalty + 0.005))
        : null;

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
        effort: groupedEffort,
        total_cases: total,
        passed_cases: passed,
        pass_rate: passRate,
        weighted_pass_rate: weightedPassRate,
        avg_duration_seconds: avgDuration,
        total_input_tokens: totalIn,
        total_output_tokens: totalOut,
        total_thinking_tokens: totalThink,
        total_cost_usd: totalCost,
        efficiency_score: effScore,
        telemetry_complete: telemetryComplete,
        category_pass_rates: categoryMap,
      });
    });

    return res.sort((a, b) => (
      b.weighted_pass_rate - a.weighted_pass_rate
      || b.pass_rate - a.pass_rate
      || (b.efficiency_score ?? -1) - (a.efficiency_score ?? -1)
    ));
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
