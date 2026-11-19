import { AggregatedModelSummary, BenchmarkItem } from './types';

export function aggregateBenchmarks(benchmarkItems: BenchmarkItem[]): AggregatedModelSummary[] {
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
    const scoredItems = items.filter((item) => !item.error_message);
    const total = scoredItems.length;
    const passed = scoredItems.filter((i) => i.passed).length;
    const passRate = total > 0 ? Math.round((passed / total) * 1000) / 10 : 0;
    const difficultyWeight = (difficulty?: string) => (
      difficulty === 'hard' ? 3 : difficulty === 'easy' ? 1 : 2
    );
    const totalWeight = scoredItems.reduce((acc, item) => acc + difficultyWeight(item.difficulty), 0);
    const passedWeight = scoredItems.reduce(
      (acc, item) => acc + (item.passed ? difficultyWeight(item.difficulty) : 0),
      0,
    );
    const weightedPassRate = totalWeight > 0
      ? Math.round((passedWeight / totalWeight) * 1000) / 10
      : 0;
    const avgDuration = total > 0 ? Math.round((scoredItems.reduce((acc, i) => acc + i.duration_seconds, 0) / total) * 100) / 100 : 0;
    const totalIn = items.reduce((acc, i) => acc + (i.token_usage?.input_tokens || 0), 0);
    const totalOut = items.reduce((acc, i) => acc + (i.token_usage?.output_tokens || 0), 0);
    const totalThink = items.reduce((acc, i) => acc + (i.token_usage?.thinking_tokens || 0), 0);
    const totalCost = Math.round(items.reduce((acc, i) => acc + (i.token_usage?.estimated_cost_usd || 0), 0) * 1000000) / 1000000;
    
    const timeoutCount = scoredItems.filter((item) => {
      const timeoutText = `${item.error_message || ''}\n${item.evaluator_logs || ''}`.toLowerCase();
      return timeoutText.includes('timeout') || timeoutText.includes('timed out');
    }).length;
    const timeoutPenalty = timeoutCount * 0.05;

    const telemetryComplete = items.every((item) => {
      if (typeof item.token_usage?.telemetry_complete === 'boolean') {
        return item.token_usage.telemetry_complete;
      }
      return false;
    });
    const pricingVerified = items.every((item) => {
      const pricing = item.metadata?.pricing as { verified?: boolean } | undefined;
      return pricing?.verified !== false;
    });
    const effScore = telemetryComplete && pricingVerified && total > 0
      ? Math.round((((weightedPassRate * weightedPassRate) / 100.0) / (totalCost + timeoutPenalty + 0.005)) * 10) / 10
      : null;

    const categoryMap: Record<string, { passed: number; total: number; rate: number }> = {};
    scoredItems.forEach((it) => {
      const cat = it.category || 'other';
      if (!categoryMap[cat]) categoryMap[cat] = { passed: 0, total: 0, rate: 0 };
      categoryMap[cat].total += 1;
      if (it.passed) categoryMap[cat].passed += 1;
    });

    Object.keys(categoryMap).forEach((c) => {
      categoryMap[c].rate = Math.round((categoryMap[c].passed / categoryMap[c].total) * 100);
    });

    const firstAttempts = items.map((item) => {
      const recorded = item.metadata?.first_attempt_passed;
      if (typeof recorded === 'boolean') return recorded;
      return item.metadata?.prior_cli_error_attempt_count ? null : item.passed && !item.error_message;
    });
    res.push({
      cli_error_cases: items.length - total,
      first_attempt_passes: firstAttempts.includes(null) ? null : firstAttempts.filter(Boolean).length,
      attempted_cases: items.length,
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
    || a.total_cost_usd - b.total_cost_usd
  ));
}
