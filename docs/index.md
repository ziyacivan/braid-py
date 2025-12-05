# BRAID-DSPy Documentation

Welcome to the BRAID-DSPy documentation!

BRAID-DSPy is a Python library that integrates BRAID (Bounded Reasoning for Autonomous Inference and Decisions) architecture into the DSPy framework, enabling structured reasoning through Guided Reasoning Diagrams (GRD) in Mermaid format.

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

## What is BRAID?

BRAID (Bounded Reasoning for Autonomous Inference and Decisions) is a structured reasoning framework that separates planning from execution:

1. **Planning Phase**: Generate a Guided Reasoning Diagram (GRD) in Mermaid format
2. **Execution Phase**: Execute the GRD step by step to solve the problem

This separation significantly improves reliability and reduces hallucinations compared to traditional Chain-of-Thought approaches.

## Key Features

- **Guided Reasoning Diagrams (GRD)**: Generate Mermaid-format flowcharts that map solution steps
- **Two-Phase Reasoning**: Separate planning and execution phases for better reliability
- **DSPy Integration**: Seamlessly integrates with existing DSPy modules and optimizers
- **Auditable Reasoning**: Visualize and debug reasoning processes through GRD diagrams
- **Optimization Support**: BRAID-aware optimizers for improving GRD quality

## Documentation Contents

```{toctree}
:maxdepth: 2
:caption: Contents

installation
api/index
examples/index
integration
```

## Installation

```bash
pip install braid-dspy
```

## Requirements

- Python >= 3.9
- dspy-ai >= 2.0.0

## License

MIT License - see the [LICENSE](https://github.com/ziyacivan/braid-dspy/blob/main/LICENSE) file for details.

## References

- [BRAID Blog Post](https://www.openserv.ai/blog/braid-is-the-missing-piece-in-ai-reasoning)
- [DSPy Framework](https://github.com/stanfordnlp/dspy)

