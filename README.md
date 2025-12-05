# BRAID-DSPy Integration

A Python library that integrates BRAID (Bounded Reasoning for Autonomous Inference and Decisions) architecture into the DSPy framework, enabling structured reasoning through Guided Reasoning Diagrams (GRD) in Mermaid format.

## Overview

BRAID-DSPy brings structured reasoning capabilities to DSPy by requiring models to first generate a machine-readable flowchart (GRD) before executing the solution. This separation of planning and execution significantly improves reliability and reduces hallucinations.

## Motivation

This project began when I first encountered the BRAID architecture during one of Armağan Amcalar's live streams. The two-phase reasoning approach — planning first, then execution — and the idea of representing this planning in a visualizable format (Mermaid diagrams) immediately captured my interest.

After the stream, I delved into OpenServ's articles and technical details about BRAID. The approach of having the model first generate a flowchart (Guided Reasoning Diagram - GRD) and then execute the solution step-by-step according to this schema seemed like a significant step forward for reliability and transparency in AI systems. I realized that integrating this architecture with the DSPy framework would need to work seamlessly with existing DSPy modules and optimizers, which led me to develop this library to make that integration a reality.

Much of the development process involved "vibe coding" — following intuition and iterating based on what felt right rather than strictly following a predefined plan. This organic approach allowed the library to evolve naturally as I explored the integration between BRAID and DSPy.

## Key Features

- **Guided Reasoning Diagrams (GRD)**: Generate Mermaid-format flowcharts that map solution steps
- **Two-Phase Reasoning**: Separate planning and execution phases for better reliability
- **DSPy Integration**: Seamlessly integrates with existing DSPy modules and optimizers
- **Auditable Reasoning**: Visualize and debug reasoning processes through GRD diagrams
- **Optimization Support**: BRAID-aware optimizers for improving GRD quality

## Installation

```bash
pip install braid-dspy
```

## Quick Start

```python
import dspy
from braid import BraidReasoning

# Configure DSPy
lm = dspy.OpenAI(model="gpt-4")
dspy.configure(lm=lm)

# Create a BRAID reasoning module
braid = BraidReasoning()

# Use it in your pipeline
result = braid(problem="Solve: If a train travels 120 km in 2 hours, what is its speed?")
print(result.answer)
print(result.grd)  # View the reasoning diagram
```

## Documentation

📚 **Full documentation is available on [Read the Docs](https://braid-py.readthedocs.io/)** (coming soon)

Local documentation:
- [API Reference](docs/api.md)
- [Examples](docs/examples.md)
- [Integration Guide](docs/integration.md)

To build documentation locally:

```bash
pip install -e ".[docs]"
cd docs
make html
```

## Examples

Check out the [examples](examples/) directory for:
- Basic usage examples
- GSM8K benchmark integration
- Optimization workflows

## License

MIT License - see [LICENSE](LICENSE) file for details.

## References

- [BRAID Blog Post](https://www.openserv.ai/blog/braid-is-the-missing-piece-in-ai-reasoning)
- [DSPy Framework](https://github.com/stanfordnlp/dspy)

