# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2] - 2026-06-22

### Added
- Add a professional documentation site using MkDocs with the Material theme, auto-deployed to GitHub Pages.
- Add comprehensive Google-style docstrings to all public classes and methods.
- Improve library landing page README with feature list, badges, and quick-start instructions.
- Create execution examples for basic usage, pipelines, batch processing, and custom processing steps.

### Fixed
- Resolve non-existent GitHub Action configuration in the documentation deployment workflow.

## [0.0.1] - 2026-06-22

### Added
- Expose main library facade `AudioEnhancer` to load, process, and export audio segments.
- Add `PipelineBuilder` to build fluent, multi-stage audio enhancement pipelines.
- Implement `SpectralGatingNoiseReducer` for removing continuous background stationary noise.
- Implement `ImpulseNoiseReducer` with median filtering for click/pop/crackle suppression.
- Implement `PeakNormalizer` to scale audio signal peak to a target dBFS level.
- Implement `RmsNormalizer` to scale audio average root-mean-square levels.
- Implement `LufsNormalizer` (adapter for `pyloudnorm`) for standard loudness-based normalization (ITU-R BS.1770).
- Expose click command-line interface under `audio_enhancer/cli.py` and run as `python -m audio_enhancer`.
- Create comprehensive execution examples for CLI, batch processing, custom pipelines, and custom processing steps.
- Add GitHub Actions CI configuration to test pushes/PRs on Python 3.9, 3.10, 3.11, and 3.12.
- Configure automated PyPI package distribution workflow on git version tag push.
