"""Offline regressions for model support, accounting, and interrupted runs."""
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timezone
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from benchmarks.evaluators.evaluators import extract_python_code
from benchmarks.models import TestCase, TokenUsage
from benchmarks.runner import (
    BenchmarkConfigurationError, load_config, load_test_cases, parse_model_spec,
    run_benchmark, _load_resume_results, _run_metadata,
)
from benchmarks.runners.antigravity_runner import AntigravityRunner, execute_agy
from benchmarks.models import BenchmarkResult
from benchmarks.reporters.reporters import MarkdownReporter


class HardeningTests(unittest.TestCase):
    def test_pricing_period_switch(self):
        runner = AntigravityRunner(load_config())
        with patch('benchmarks.runners.base_runner.datetime') as clock:
            clock.now.return_value = datetime(2026, 11, 30, 23, 59, tzinfo=timezone.utc)
            self.assertEqual(runner.get_pricing('Gemini 4 Argon (High)')['output'], 10)
            clock.now.return_value = datetime(2026, 12, 1, tzinfo=timezone.utc)
            self.assertEqual(runner.get_pricing('Gemini 4 Argon (High)')['output'], 20)
            self.assertEqual(runner.get_pricing('Gemini 3.8 Flash (High)')['cache_read'], .075)
            clock.now.return_value = datetime(2027, 1, 1, tzinfo=timezone.utc)
            self.assertEqual(runner.get_pricing('Gemini 3.8 Flash (High)')['cache_read'], .15)

    def test_dashboard_and_markdown_exclude_same_errors(self):
        root = Path(__file__).resolve().parents[2]
        compiler = root / 'node_modules/.bin/tsc'
        if not compiler.exists():
            self.skipTest('Frontend dependencies not installed')
        rows = [BenchmarkResult(
            case_id=str(i), case_title='Test', category='logic', model='test', cli='agy',
            passed=i == 0, duration_seconds=10,
            token_usage=TokenUsage(estimated_cost_usd=.1, telemetry_complete=True),
            error_message='connection reset' if i == 2 else None,
        ) for i in range(3)]
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run([str(compiler), 'src/benchmarkSummary.ts', '--module', 'commonjs',
                            '--target', 'es2020', '--skipLibCheck', '--outDir', directory],
                           cwd=root, capture_output=True, text=True, check=True)
            script = "const {aggregateBenchmarks}=require(process.argv[1]); console.log(JSON.stringify(aggregateBenchmarks(JSON.parse(process.argv[2]))));"
            result = subprocess.run(['node', '-e', script, str(Path(directory)/'benchmarkSummary.js'),
                                     json.dumps([row.to_dict() for row in rows])],
                                    capture_output=True, text=True, check=True)
        summary = json.loads(result.stdout)[0]
        self.assertEqual(summary['total_cases'], 2)
        self.assertEqual(summary['cli_error_cases'], 1)
        self.assertEqual(summary['pass_rate'], 50)
        self.assertEqual(summary['first_attempt_passes'], 1)
        self.assertEqual(summary['attempted_cases'], 3)
        self.assertEqual(summary['total_cost_usd'], .3)
        report = MarkdownReporter.generate_report(rows)
        self.assertIn('**33.3%** (1/3) | **50.0%** (1/2)', report)

    def test_argon_and_flash_use_configured_rates(self):
        runner = AntigravityRunner(load_config())
        with patch('benchmarks.runners.base_runner.datetime') as clock:
            clock.now.return_value = datetime(2026, 11, 19, tzinfo=timezone.utc)
            self.assertEqual(runner.get_pricing('Gemini 3.8 Flash (High)')['cache_read'], .075)
            self.assertEqual(runner.get_pricing('Gemini 4 Argon (High)')['output'], 10)
        self.assertTrue(runner.pricing_provenance('Gemini 4 Argon (High)')['verified'])
        self.assertFalse(runner.pricing_provenance('Gemini Unknown')['verified'])

    def test_new_gemini_models_use_verified_rates(self):
        runner = AntigravityRunner(load_config())
        for model, input_rate, output_rate, cache_rate in (
            ('Gemini 4 Neon (High)', 3, 15, .15),
            ('Gemini 4 Hydrogen (High)', 1.5, 7.5, .075),
        ):
            with self.subTest(model=model):
                self.assertTrue(runner.pricing_provenance(model)['verified'])
                self.assertEqual(runner.get_pricing(model), {
                    'input': input_rate, 'output': output_rate,
                    'thinking': output_rate, 'cache_read': cache_rate,
                })

    def test_named_suite_publishes_to_separate_dashboard_dataset(self):
        case = TestCase(id='example', title='Test', category='logic', description='',
                        prompt='solve', evaluator_type='python_unit_test', test_code='assert True',
                        case_hash='hash')
        with tempfile.TemporaryDirectory() as directory, \
             patch('benchmarks.runner.load_test_cases', return_value=[case]) as load_cases, \
             patch('benchmarks.runner.get_runner') as runner, \
             patch('benchmarks.runner.UnitTestEvaluator.evaluate', return_value=(True, 'ok')), \
             patch('benchmarks.runner.JSONReporter.save_report') as save_report, \
             redirect_stdout(StringIO()):
            runner.return_value.run_prompt.return_value = ('answer', TokenUsage(), .1, None)
            results = run_benchmark(['agy'], ['Gemini 4 Neon (High)'], output_dir=directory,
                                    suite_preset='core10-v1', publish=True)
            self.assertEqual(len(load_cases.call_args.args[1]), 10)
            self.assertEqual(results[0].metadata['suite_preset'], 'core10-v1')
            self.assertEqual(save_report.call_args.args[1].name, 'benchmark-data-core10-v1.json')
            self.assertTrue((Path(directory) / 'latest_report_core10-v1.md').exists())
            self.assertFalse((Path(directory) / 'latest_report.md').exists())

    def test_effort_conflict_and_unknown_filters_fail(self):
        with self.assertRaises(BenchmarkConfigurationError):
            parse_model_spec('Gemini 4 Argon (High)', 'low')
        self.assertEqual(parse_model_spec('Gemini 4 Argon (High)')[2], 'high')
        with self.assertRaises(BenchmarkConfigurationError):
            load_test_cases(case_ids=['logic_01_lru_ttl', 'typo'])
        for kwargs in ({'timeout_override': -1}, {'models': ['gpt-test', 'gpt-test']}):
            args = {'clis': ['codex'], 'models': ['gpt-test'], 'dry_run': True, **kwargs}
            with self.assertRaises(BenchmarkConfigurationError):
                run_benchmark(**args)

    def test_mixed_fences_extract_python_not_prose(self):
        response = '```regex\n[x]+\n```\nExplanation here.\n```python\ndef answer():\n    return 42\n```'
        self.assertEqual(extract_python_code(response), 'def answer():\n    return 42')
        self.assertEqual(extract_python_code('I cannot do that.'), '')
        self.assertEqual(extract_python_code('```regex\n[x]+\n```'), '')

    def test_error_exit_preserves_usage(self):
        payload = json.dumps({'status': 'ERROR', 'error': 'connection reset', 'usage': {
            'input_tokens': 100, 'output_tokens': 40, 'thinking_tokens': 20,
        }})
        with patch('benchmarks.runners.antigravity_runner.execute_agy', return_value=SimpleNamespace(
            returncode=1, stdout=payload, stderr=''
        )):
            _, usage, _, error = AntigravityRunner({}).run_prompt('test', 'Gemini 4 Argon (High)')
        self.assertEqual(usage.total_tokens, 140)
        self.assertEqual(error, 'connection reset')

    def test_timeout_keeps_partial_usage_without_inventing_counts(self):
        for output, expected in ((None, 0), ('{"usage":{"input_tokens":123}}', 123)):
            with patch('benchmarks.runners.antigravity_runner.execute_agy', side_effect=
                       subprocess.TimeoutExpired('agy', 10, output=output)):
                _, usage, _, error = AntigravityRunner({}).run_prompt('test', 'Gemini 4 Argon (High)')
            self.assertEqual(usage.input_tokens, expected)
            self.assertFalse(usage.telemetry_complete)
            self.assertIn('TIMEOUT', error)

    def test_process_group_cleanup_on_timeout(self):
        with patch('benchmarks.runners.antigravity_runner.subprocess.Popen') as popen, \
             patch('benchmarks.runners.antigravity_runner.os.killpg') as kill:
            popen.return_value.pid = 123
            popen.return_value.communicate.side_effect = [
                subprocess.TimeoutExpired('agy', 1), ('partial', 'error'),
            ]
            with self.assertRaises(subprocess.TimeoutExpired) as caught:
                execute_agy(['agy'], timeout=1, cwd='/tmp')
            kill.assert_called_once()
            self.assertEqual(caught.exception.output, 'partial')

    def test_interrupted_run_checkpoint_resumes_only_missing_case(self):
        cases = [TestCase(id=f'case_{i}', title='Test', category='logic', description='',
                         prompt='solve', evaluator_type='python_unit_test', test_code='assert True',
                         case_hash=f'hash{i}') for i in range(2)]
        with tempfile.TemporaryDirectory() as directory, \
             patch('benchmarks.runner.load_test_cases', return_value=cases), \
             patch('benchmarks.runner.get_runner') as runner, \
             patch('benchmarks.runner.UnitTestEvaluator.evaluate', return_value=(True, 'ok')), \
             redirect_stdout(StringIO()):
            runner.return_value.run_prompt.side_effect = [('answer', TokenUsage(), .1, None), KeyboardInterrupt()]
            with self.assertRaises(KeyboardInterrupt):
                run_benchmark(['codex'], ['gpt-test'], output_dir=directory)
            checkpoint = next(Path(directory).glob('benchmark_checkpoint_*.json'))
            self.assertEqual(len(json.loads(checkpoint.read_text())['results']), 1)
            inconsistent = json.loads(checkpoint.read_text())
            inconsistent['results'][0]['metadata']['config_hash'] = 'changed'
            with patch('benchmarks.runner.Path.read_text', return_value=json.dumps(inconsistent)):
                with self.assertRaisesRegex(BenchmarkConfigurationError, 'inconsistent provenance'):
                    _load_resume_results(str(checkpoint), cases, [('codex', 'gpt-test', None)],
                                         inconsistent['metadata'])
            runner.return_value.run_prompt.reset_mock()
            runner.return_value.run_prompt.side_effect = None
            runner.return_value.run_prompt.return_value = ('answer', TokenUsage(), .1, None)
            results = run_benchmark(['codex'], ['gpt-test'], output_dir=directory, resume_from=str(checkpoint))
            self.assertEqual(len(results), 2)
            self.assertEqual(runner.return_value.run_prompt.call_count, 1)
            with self.assertRaises(BenchmarkConfigurationError):
                run_benchmark(['codex'], ['gpt-test'], output_dir=directory,
                              resume_from=str(checkpoint), timeout_override=1200)

    def test_resume_rejects_mixed_provenance(self):
        cases = load_test_cases()
        plan = [('agy', 'Gemini 4 Argon (High)', 'high')]
        metadata = _run_metadata(cases, plan)
        # Missing provenance must fail even in an empty checkpoint.
        payload = {'metadata': {}, 'expected_keys': [list((*plan[0], case.id)) for case in cases], 'results': []}
        with patch('benchmarks.runner.Path.read_text', return_value=json.dumps(payload)):
            with self.assertRaises(BenchmarkConfigurationError):
                _load_resume_results('mock.json', cases, plan, metadata)
