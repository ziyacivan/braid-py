"""Main BRAID reasoning module for DSPy."""

from typing import Dict, List, Optional, Any
import dspy
from dataclasses import dataclass

from braid.signatures import BraidPlanSignature, BraidStepSignature
from braid.generator import GRDGenerator
from braid.parser import MermaidParser, GRDStructure


@dataclass
class BraidResult:
    """Result object returned by BraidReasoning module."""

    problem: str
    grd: str
    parsed_grd: Optional[GRDStructure]
    reasoning_steps: List[Dict[str, Any]]
    answer: str
    execution_trace: List[Dict[str, Any]]
    valid: bool
    error: Optional[str] = None


class BraidReasoning(dspy.Module):
    """
    BRAID reasoning module for DSPy.

    This module implements the BRAID (Bounded Reasoning for Autonomous
    Inference and Decisions) architecture:
    1. Planning Phase: Generate a Guided Reasoning Diagram (GRD) in Mermaid format
    2. Execution Phase: Execute the GRD step by step to solve the problem

    Example:
        >>> import dspy
        >>> from braid import BraidReasoning
        >>>
        >>> lm = dspy.OpenAI(model="gpt-4")
        >>> dspy.configure(lm=lm)
        >>>
        >>> braid = BraidReasoning()
        >>> result = braid(problem="If a train travels 120 km in 2 hours, what is its speed?")
        >>> print(result.answer)
        >>> print(result.grd)
    """

    def __init__(
        self, use_generator: bool = True, max_execution_steps: int = 20, validate_grd: bool = True
    ):
        """
        Initialize the BRAID reasoning module.

        Args:
            use_generator: Whether to use GRDGenerator for planning (True)
                          or direct LLM call (False)
            max_execution_steps: Maximum number of steps to execute
            validate_grd: Whether to validate GRD syntax before execution
        """
        super().__init__()

        self.use_generator = use_generator
        self.max_execution_steps = max_execution_steps
        self.validate_grd = validate_grd

        # Initialize sub-modules
        self.plan = dspy.Predict(BraidPlanSignature)
        self.execute_step = dspy.Predict(BraidStepSignature)
        self.parser = MermaidParser()

        if use_generator:
            self.generator = GRDGenerator()
        else:
            self.generator = None

    def forward(
        self, problem: str, grd: Optional[str] = None, problem_type: Optional[str] = None
    ) -> BraidResult:
        """
        Execute BRAID reasoning on a problem.

        Args:
            problem: The problem to solve
            grd: Optional pre-generated GRD (if None, will be generated)
            problem_type: Optional problem type hint for generation

        Returns:
            BraidResult object containing GRD, reasoning steps, and answer
        """
        execution_trace = []
        reasoning_steps = []

        # Phase 1: Planning - Generate or use provided GRD
        if grd is None:
            if self.use_generator and self.generator:
                generation_result = self.generator.generate(
                    problem=problem, problem_type=problem_type
                )
                grd = generation_result.get("grd")
                if not grd:
                    return BraidResult(
                        problem=problem,
                        grd="",
                        parsed_grd=None,
                        reasoning_steps=[],
                        answer="",
                        execution_trace=execution_trace,
                        valid=False,
                        error=generation_result.get("error", "Failed to generate GRD"),
                    )
            else:
                # Use DSPy signature directly
                plan_result = self.plan(problem=problem)
                grd = plan_result.grd
                execution_trace.append(
                    {"phase": "planning", "method": "dspy_signature", "grd": grd}
                )
        else:
            execution_trace.append({"phase": "planning", "method": "provided", "grd": grd})

        # Validate GRD if requested
        parsed_grd = None
        if self.validate_grd:
            is_valid, error_msg = self.parser.validate(grd)
            if not is_valid:
                return BraidResult(
                    problem=problem,
                    grd=grd,
                    parsed_grd=None,
                    reasoning_steps=[],
                    answer="",
                    execution_trace=execution_trace,
                    valid=False,
                    error=f"Invalid GRD: {error_msg}",
                )

        # Parse GRD structure
        try:
            parsed_grd = self.parser.parse(grd)
        except Exception as e:
            return BraidResult(
                problem=problem,
                grd=grd,
                parsed_grd=None,
                reasoning_steps=[],
                answer="",
                execution_trace=execution_trace,
                valid=False,
                error=f"Failed to parse GRD: {str(e)}",
            )

        # Phase 2: Execution - Execute GRD step by step
        execution_order = parsed_grd.get_execution_order()

        if not execution_order:
            return BraidResult(
                problem=problem,
                grd=grd,
                parsed_grd=parsed_grd,
                reasoning_steps=[],
                answer="",
                execution_trace=execution_trace,
                valid=False,
                error="GRD has no execution order",
            )

        # Execute steps in order
        step_results = {}
        context = {"problem": problem, "previous_steps": []}

        for step_idx, node_id in enumerate(execution_order[: self.max_execution_steps]):
            node = parsed_grd.get_node_by_id(node_id)
            if not node:
                continue

            # Build context from previous steps
            previous_results = "\n".join(
                [
                    f"Step {i+1} ({s['step_id']}): {s['result']}"
                    for i, s in enumerate(reasoning_steps)
                ]
            )

            # Execute step
            step_context = f"Problem: {problem}\n\nPrevious Steps:\n{previous_results}"

            try:
                step_result = self.execute_step(step_description=node.label, context=step_context)

                step_output = step_result.step_output

                reasoning_steps.append(
                    {
                        "step_id": node_id,
                        "step_number": step_idx + 1,
                        "label": node.label,
                        "result": step_output,
                        "node_type": node.node_type.value,
                    }
                )

                step_results[node_id] = step_output
                context["previous_steps"].append({"step": node_id, "result": step_output})

                execution_trace.append(
                    {
                        "phase": "execution",
                        "step": step_idx + 1,
                        "node_id": node_id,
                        "result": step_output,
                    }
                )

            except Exception as e:
                execution_trace.append(
                    {
                        "phase": "execution",
                        "step": step_idx + 1,
                        "node_id": node_id,
                        "error": str(e),
                    }
                )
                # Continue execution even if a step fails
                step_results[node_id] = f"Error: {str(e)}"

        # Extract final answer from end nodes
        answer = self._extract_answer(parsed_grd, step_results, reasoning_steps)

        return BraidResult(
            problem=problem,
            grd=grd,
            parsed_grd=parsed_grd,
            reasoning_steps=reasoning_steps,
            answer=answer,
            execution_trace=execution_trace,
            valid=True,
        )

    def _extract_answer(
        self, grd: GRDStructure, step_results: Dict[str, str], reasoning_steps: List[Dict[str, Any]]
    ) -> str:
        """
        Extract the final answer from execution results.

        Args:
            grd: Parsed GRD structure
            step_results: Dictionary mapping node IDs to their results
            reasoning_steps: List of reasoning steps

        Returns:
            Final answer string
        """
        # Try to get answer from end nodes
        if grd.end_nodes:
            for end_node_id in grd.end_nodes:
                if end_node_id in step_results:
                    result = step_results[end_node_id]
                    # Check if result looks like a final answer
                    if result and len(result) < 500:  # Reasonable answer length
                        return result

        # If no end node result, use the last step result
        if reasoning_steps:
            last_step = reasoning_steps[-1]
            return last_step.get("result", "")

        # Fallback: construct answer from all steps
        if step_results:
            return "\n".join([f"{node_id}: {result}" for node_id, result in step_results.items()])

        return ""

    def __call__(self, problem: str, **kwargs) -> BraidResult:
        """Make the module callable."""
        return self.forward(problem, **kwargs)
