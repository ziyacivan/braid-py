# BRAID-DSPy Integration

[![CI](https://github.com/ziyacivan/braid-dspy/actions/workflows/ci.yml/badge.svg)](https://github.com/ziyacivan/braid-dspy/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/braid-dspy.svg)](https://badge.fury.io/py/braid-dspy)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python library that integrates BRAID (Bounded Reasoning for Autonomous Inference and Decisions) architecture into the DSPy framework, enabling structured reasoning through Guided Reasoning Diagrams (GRD) in Mermaid format.

## Overview

BRAID-DSPy brings structured reasoning capabilities to DSPy by requiring models to first generate a machine-readable flowchart (GRD) before executing the solution. This separation of planning and execution significantly improves reliability and reduces hallucinations.

## Motivation

This project began when I first encountered the BRAID architecture during one of [Armağan Amcalar](https://github.com/dashersw)'s live streams. The two-phase reasoning approach — planning first, then execution — and the idea of representing this planning in a visualizable format (Mermaid diagrams) immediately captured my interest.

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

## Architecture

BRAID-DSPy implements a two-phase reasoning architecture that separates planning from execution, significantly improving reliability and reducing hallucinations compared to traditional Chain-of-Thought approaches.

### High-Level Architecture

```mermaid
flowchart TD
    A[Problem Input] --> B[Planning Phase]
    B --> C[GRD Generation]
    C --> D[Mermaid Diagram]
    D --> E[Parsing Phase]
    E --> F[GRD Structure]
    F --> G[Execution Phase]
    G --> H[Step-by-Step Execution]
    H --> I[Final Answer]
    
    B --> B1["GRDGenerator<br/>or<br/>Direct LLM Call"]
    E --> E1["MermaidParser<br/>Validates & Parses"]
    G --> G1["Execute Each Node<br/>in Order"]
    G1 --> G2["Build Context<br/>from Previous Steps"]
    G2 --> G3["LLM Execution<br/>per Step"]
    
    classDef planningPhase fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef parsingPhase fill:#fff4e1,stroke:#e65100,stroke-width:2px
    classDef executionPhase fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class B,B1,C planningPhase
    class E,E1,F parsingPhase
    class G,G1,G2,G3,H executionPhase
```

### Two-Phase Reasoning Process

#### Phase 1: Planning

In the planning phase, the system generates a **Guided Reasoning Diagram (GRD)** in Mermaid format that maps out the solution steps:

```mermaid
flowchart LR
    A[Problem] --> B[GRDGenerator]
    B --> C{Generation Method}
    C -->|With Generator| D["Few-shot Examples<br/>+ Structured Prompt"]
    C -->|Direct| E["DSPy Signature<br/>BraidPlanSignature"]
    D --> F[Mermaid GRD]
    E --> F
    F --> G[Validation]
    G -->|Valid| H[Parsed Structure]
    G -->|Invalid| I[Error]
    
    classDef generator fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef grd fill:#fff4e1,stroke:#e65100,stroke-width:2px
    classDef parsed fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class B,D,E generator
    class F,G grd
    class H parsed
```

**Example GRD Output:**
```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify given values:<br/>Distance = 120 km<br/>Time = 2 hours]
    Identify --> Formula[Recall speed formula:<br/>Speed = Distance / Time]
    Formula --> Calculate[Calculate:<br/>Speed = 120 / 2]
    Calculate --> Answer[Speed = 60 km/h]
```

#### Phase 2: Execution

The execution phase follows the GRD structure step-by-step:

```mermaid
flowchart TD
    A[Parsed GRD] --> B[Get Execution Order]
    B --> C[For Each Node]
    C --> D["Build Context<br/>Problem + Previous Steps"]
    D --> E["Execute Step<br/>via LLM"]
    E --> F[Store Result]
    F --> G{More Steps?}
    G -->|Yes| C
    G -->|No| H[Extract Final Answer]
    H --> I[Return BraidResult]
    
    classDef loop fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef execution fill:#fff4e1,stroke:#e65100,stroke-width:2px
    classDef result fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class C,D loop
    class E,F execution
    class H,I result
```

### Component Architecture

```mermaid
graph TB
    subgraph BRAID["BRAID-DSPy Components"]
        A["BraidReasoning<br/>Main Module"]
        B["GRDGenerator<br/>Planning"]
        C["MermaidParser<br/>Parsing & Validation"]
        D["BraidOptimizer<br/>Optimization"]
        E["DSPy Signatures<br/>BraidPlanSignature<br/>BraidStepSignature"]
    end
    
    subgraph DSPY["DSPy Framework"]
        F[DSPy Modules]
        G[LLM Backend]
        H[Optimizers]
    end
    
    A --> B
    A --> C
    A --> E
    A --> D
    B --> F
    E --> F
    D --> H
    F --> G
    
    classDef main fill:#4a90e2,stroke:#01579b,stroke-width:3px,color:#fff
    classDef planning fill:#e1f5ff,stroke:#01579b,stroke-width:2px
    classDef parsing fill:#fff4e1,stroke:#e65100,stroke-width:2px
    classDef optimization fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px
    
    class A main
    class B,E planning
    class C parsing
    class D optimization
```

### Key Components

1. **BraidReasoning**: Main module that orchestrates the two-phase process
   - Manages planning and execution phases
   - Handles GRD generation or accepts pre-generated GRDs
   - Executes steps sequentially with context accumulation

2. **GRDGenerator**: Generates Mermaid-formatted GRDs using few-shot examples
   - Uses structured prompts with examples
   - Supports retry logic for robust generation
   - Extracts Mermaid code from LLM responses

3. **MermaidParser**: Parses and validates Mermaid diagrams
   - Converts Mermaid syntax to structured `GRDStructure` objects
   - Validates diagram syntax and structure
   - Determines execution order using topological sorting

4. **BraidOptimizer**: Optimizes both planning and execution phases
   - Can optimize GRD generation quality
   - Improves step execution through DSPy optimizers
   - Supports custom metrics for evaluation

### Execution Flow Example

For a problem like "If a train travels 120 km in 2 hours, what is its speed?":

```mermaid
sequenceDiagram
    participant User
    participant BraidReasoning
    participant GRDGenerator
    participant MermaidParser
    participant LLM
    
    User->>BraidReasoning: problem="..."
    BraidReasoning->>GRDGenerator: generate(problem)
    GRDGenerator->>LLM: Generate GRD with examples
    LLM-->>GRDGenerator: Mermaid diagram
    GRDGenerator-->>BraidReasoning: GRD string
    
    BraidReasoning->>MermaidParser: parse(grd)
    MermaidParser->>MermaidParser: Validate syntax
    MermaidParser->>MermaidParser: Extract nodes & edges
    MermaidParser->>MermaidParser: Determine execution order
    MermaidParser-->>BraidReasoning: GRDStructure
    
    loop For each step in execution order
        BraidReasoning->>BraidReasoning: Build context
        BraidReasoning->>LLM: Execute step
        LLM-->>BraidReasoning: Step result
        BraidReasoning->>BraidReasoning: Store result
    end
    
    BraidReasoning->>BraidReasoning: Extract final answer
    BraidReasoning-->>User: BraidResult(answer, grd, steps)
```

### Benefits of This Architecture

- **Reliability**: Planning phase ensures structured approach before execution
- **Transparency**: GRD diagrams provide visual reasoning trace
- **Debuggability**: Each step is isolated and traceable
- **Optimization**: Both phases can be optimized independently
- **Flexibility**: Supports pre-generated GRDs or dynamic generation

## Documentation

📚 **Full documentation is available on [Read the Docs](https://braid-dspy.readthedocs.io/en/stable/)**

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

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## References

- [BRAID Blog Post](https://www.openserv.ai/blog/braid-is-the-missing-piece-in-ai-reasoning)
- [DSPy Framework](https://github.com/stanfordnlp/dspy)

