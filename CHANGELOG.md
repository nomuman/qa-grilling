# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-08-29

### Added

- explicit-only invocation metadata for Codex and Claude Code;
- an untrusted-input and read-only review boundary;
- `quick`, `standard`, and `deep` review depths;
- interactive and one-shot decision modes;
- domain-specific references loaded through progressive disclosure;
- an Agent Skill domain pack covering invocation, authority, context isolation, host portability, evaluation integrity, and release provenance;
- deterministic structural validation, a behavioral evaluation rubric, and GitHub Actions;
- validator negative tests and persistent release-candidate evidence classes;
- an English and Japanese dogfooding case study tracing the skill's self-review into verified changes;
- MIT License and a reproducible tagged-release installation flow.

### Changed

- default review depth is now `standard`;
- interactive reviews ask only unresolved P0/P1 decisions by default;
- P2/P3 decisions use documented recommended assumptions unless they materially change architecture, a public contract, or irreversible behavior;
- supporting examples are documented as optional references rather than runtime dependencies.
- substantial reports can trace findings through decisions, specification changes, acceptance criteria, tests, and verification evidence.

[1.0.0]: https://github.com/nomuman/qa-grilling/releases/tag/v1.0.0
