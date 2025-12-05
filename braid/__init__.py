"""
BRAID-DSPy Integration Library

This library integrates BRAID (Bounded Reasoning for Autonomous Inference and Decisions)
architecture into the DSPy framework, enabling structured reasoning through
Guided Reasoning Diagrams (GRD).
"""

from braid.module import BraidReasoning, BraidResult
from braid.signatures import (
    BraidPlanSignature,
    BraidExecuteSignature,
    BraidReasoningSignature,
    BraidStepSignature,
)
from braid.optimizer import BraidOptimizer, GRDMetrics
from braid.parser import MermaidParser, GRDStructure, GRDNode, GRDEdge
from braid.generator import GRDGenerator

__version__ = "0.1.5"

__all__ = [
    "BraidReasoning",
    "BraidResult",
    "BraidPlanSignature",
    "BraidExecuteSignature",
    "BraidReasoningSignature",
    "BraidStepSignature",
    "BraidOptimizer",
    "GRDMetrics",
    "MermaidParser",
    "GRDStructure",
    "GRDNode",
    "GRDEdge",
    "GRDGenerator",
]
