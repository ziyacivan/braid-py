# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.6] - 2025-01-XX

### Added
- Comprehensive test suite for `BraidOptimizer` class (`test_optimizer.py`)
- Extensive test coverage for utility functions (`test_utils.py`)
- Additional edge case tests for `GRDGenerator` class
- Tests for GRDMetrics including structural validity, completeness, and execution traceability
- Tests for optimization paths with and without base optimizer
- Tests for metric evaluation with various scenarios

### Changed
- Significantly improved test coverage from 65.36% to 84.36%
- Enhanced test coverage for `braid/optimizer.py` from 30% to 80%
- Enhanced test coverage for `braid/utils.py` from 38% to 97%
- Improved test coverage for `braid/module.py` from 80% to 81%
- Improved test coverage for `braid/parser.py` from 97% to 98%

### Fixed
- Test suite now meets the 70% coverage requirement
- All 115 tests passing successfully

## [0.1.5] - 2025-01-XX

### Added
- Comprehensive Architecture documentation section in README.md
- Mermaid diagrams illustrating BRAID-DSPy architecture and workflow
- Visual documentation of two-phase reasoning process (Planning & Execution)
- Component architecture diagrams
- Execution flow sequence diagrams

### Changed
- Enhanced README.md with detailed architecture explanations
- Improved documentation structure with visual aids

## [0.1.4] - 2025-01-XX

### Changed
- Updated all version numbers to 0.1.4
- Updated GitHub repository URL from braid-py to braid-dspy
- Updated Read the Docs URL to https://braid-dspy.readthedocs.io/en/stable/

## [0.1.3] - 2025-01-XX

### Added
- GitHub issue templates for bug reports, feature requests, and questions
- Pull request template
- Contributing guidelines (CONTRIBUTING.md)
- Code of Conduct (CODE_OF_CONDUCT.md)
- Security policy (SECURITY.md)
- Authors file (AUTHORS.md)
- Pre-commit hooks configuration
- Editor configuration (.editorconfig)
- Type checking with mypy in CI
- Coverage reporting improvements

### Changed
- Improved CI workflow with mypy type checking
- Updated documentation URLs
- Version synchronization across all files

## [0.1.2] - 2025-01-XX

### Added
- Initial release with core BRAID-DSPy functionality
- BraidReasoning module for two-phase reasoning
- MermaidParser for parsing GRD diagrams
- GRDGenerator for generating Guided Reasoning Diagrams
- BraidOptimizer for optimizing GRD quality
- DSPy signature integration
- Basic test suite
- Documentation structure
- Example scripts

### Fixed
- Initial bug fixes and improvements

## [0.1.0] - 2025-01-XX

### Added
- Initial project setup
- Basic package structure

[Unreleased]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.6...HEAD
[0.1.6]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.5...v0.1.6
[0.1.5]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.4...v0.1.5
[0.1.4]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.3...v0.1.4
[0.1.3]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/ziyacivan/braid-dspy/compare/v0.1.0...v0.1.2
[0.1.0]: https://github.com/ziyacivan/braid-dspy/releases/tag/v0.1.0

