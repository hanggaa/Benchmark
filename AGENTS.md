# Repository Guidelines

## Project Structure & Module Organization

This repository combines a reusable AI-assisted development workflow with an LLM benchmark dashboard. The React/Vite frontend lives in `src/`: page composition is in `App.tsx`, reusable UI is under `src/components/`, shared types are in `src/types.ts`, and generated leaderboard input is `src/data/benchmark-data.json`. Static files belong in `public/`.

The Python benchmark framework is under `benchmarks/`. Put case definitions in `benchmarks/cases/<category>/`, CLI integrations in `benchmarks/runners/`, evaluation logic in `benchmarks/evaluators/`, and generated Markdown/JSON output in `benchmarks/reports/`. Workflow prompts are the root `part*.md` files; reusable agent material belongs in `templates/`, with supporting guidance in `docs/` and worked samples in `examples/`.

## Build, Test, and Development Commands

- `npm ci`: install the locked frontend dependencies.
- `npm run dev`: start the Vite development server.
- `npm run build`: run strict TypeScript checks and create `dist/`.
- `npm run preview`: serve the production build locally.
- `python3 scripts/validate.py`: run the repository's structural contract checks.
- `python3 scripts/validate.py --ci`: reproduce the stricter CI validation mode.
- `python3 -m benchmarks.runner --models "codex:gpt-5.6-sol:high" --dry-run`: verify benchmark routing without spending tokens.

## Coding Style & Naming Conventions

Use two-space indentation, semicolons, and single quotes in TypeScript/TSX. Keep React component files and exported components in PascalCase; use camelCase for variables and functions. Preserve strict typing and avoid `any`. Python uses four-space indentation, snake_case names, type hints, and standard-library-first implementations. Match existing Markdown heading hierarchy and write concise, actionable English. No standalone formatter or linter is configured; follow nearby code.

## Testing Guidelines

Run `python3 scripts/validate.py` for prompt, template, skill-frontmatter, JSON, and YAML changes. Run `npm run build` for frontend or benchmark-data changes. New benchmark cases should follow the existing category folders and `<category>_<nn>_<description>.json` naming pattern; first confirm them with `--dry-run`. CI also checks required files and external links. No coverage threshold is currently defined.

## Commit & Pull Request Guidelines

Recent commits use short, imperative, sentence-case summaries such as `Add CTF test case`; no Conventional Commit prefix is required. Keep commits and PRs focused. PRs must explain what changed, why it helps, and any breaking instruction changes; list validation commands, update affected docs, link relevant issues, and include screenshots for visible UI changes. Open an issue before large workflow changes.

## Security & Configuration

Never commit `.env` files, credentials, or local CLI settings. Keep pricing, timeouts, and adapter configuration in `benchmarks/config.json`, and call out pricing-source changes in the PR.
