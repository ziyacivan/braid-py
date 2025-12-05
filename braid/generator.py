"""GRD Generator module for creating Guided Reasoning Diagrams using LLMs."""

from typing import Dict, List, Optional, Any
import dspy
from braid.parser import MermaidParser
from braid.utils import extract_mermaid_code
from braid.signatures import BraidPlanSignature


class GRDGenerator:
    """Generator for Guided Reasoning Diagrams in Mermaid format."""

    # Few-shot examples for GRD generation
    DEFAULT_EXAMPLES = [
        {
            "problem": "If a train travels 120 km in 2 hours, what is its speed?",
            "grd": """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify given values:<br/>Distance = 120 km<br/>Time = 2 hours]
    Identify --> Formula[Recall speed formula:<br/>Speed = Distance / Time]
    Formula --> Calculate[Calculate:<br/>Speed = 120 / 2]
    Calculate --> Answer[Speed = 60 km/h]
```""",
        },
        {
            "problem": "Solve: 3x + 5 = 14",
            "grd": """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify equation:<br/>3x + 5 = 14]
    Identify --> Isolate[Isolate variable term:<br/>3x = 14 - 5]
    Isolate --> Simplify[Simplify:<br/>3x = 9]
    Simplify --> Solve[Solve for x:<br/>x = 9 / 3]
    Solve --> Answer[x = 3]
```""",
        },
    ]

    def __init__(
        self,
        examples: Optional[List[Dict[str, str]]] = None,
        max_retries: int = 3,
        temperature: float = 0.3,
        use_dspy_predict: bool = True,
    ):
        """
        Initialize the GRD Generator.

        Args:
            examples: Few-shot examples for GRD generation
            max_retries: Maximum number of retries if generation fails
            temperature: Temperature for LLM generation (lower = more deterministic)
            use_dspy_predict: Whether to use DSPy's Predict API (recommended)
        """
        self.examples = examples or self.DEFAULT_EXAMPLES
        self.max_retries = max_retries
        self.temperature = temperature
        self.use_dspy_predict = use_dspy_predict
        self.parser = MermaidParser()

        if use_dspy_predict:
            self.predictor = dspy.Predict(BraidPlanSignature)

    def generate(
        self,
        problem: str,
        problem_type: Optional[str] = None,
        custom_instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Generate a GRD for a given problem.

        Args:
            problem: The problem to solve
            problem_type: Optional type hint (e.g., "math", "logic", "reasoning")
            custom_instructions: Optional custom instructions for generation

        Returns:
            Dictionary containing:
                - grd: Mermaid code string
                - raw_response: Raw LLM response
                - parsed_structure: Parsed GRDStructure object
                - valid: Whether the GRD is valid
        """
        prompt = self._build_prompt(problem, problem_type, custom_instructions)

        for attempt in range(self.max_retries):
            try:
                if self.use_dspy_predict:
                    # Use DSPy's Predict API (recommended)
                    result = self.predictor(problem=problem)
                    raw_response = result.grd
                else:
                    # Direct LM access (fallback)
                    lm = dspy.settings.lm if hasattr(dspy, "settings") else None
                    if not lm:
                        # Try alternative way to get LM
                        try:
                            lm = dspy.LM()
                        except:
                            raise ValueError(
                                "DSPy language model not configured. Call dspy.configure(lm=...) first."
                            )

                    # Configure temperature if supported
                    original_temp = getattr(lm, "temperature", None)
                    if hasattr(lm, "temperature"):
                        lm.temperature = self.temperature

                    try:
                        response = lm(prompt)
                        raw_response = (
                            response
                            if isinstance(response, str)
                            else getattr(response, "text", str(response))
                        )
                    finally:
                        # Restore original temperature
                        if hasattr(lm, "temperature") and original_temp is not None:
                            lm.temperature = original_temp

                # Extract Mermaid code
                mermaid_code = extract_mermaid_code(raw_response)

                if not mermaid_code:
                    if attempt < self.max_retries - 1:
                        continue
                    return {
                        "grd": None,
                        "raw_response": raw_response,
                        "parsed_structure": None,
                        "valid": False,
                        "error": "Could not extract Mermaid code from response",
                    }

                # Validate syntax
                is_valid, error_msg = self.parser.validate(mermaid_code)

                if not is_valid and attempt < self.max_retries - 1:
                    continue

                # Parse structure
                parsed_structure = None
                if is_valid:
                    try:
                        parsed_structure = self.parser.parse(mermaid_code)
                    except Exception as e:
                        error_msg = f"Parsing error: {str(e)}"
                        is_valid = False

                return {
                    "grd": mermaid_code,
                    "raw_response": raw_response,
                    "parsed_structure": parsed_structure,
                    "valid": is_valid,
                    "error": error_msg if not is_valid else None,
                }

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return {
                        "grd": None,
                        "raw_response": None,
                        "parsed_structure": None,
                        "valid": False,
                        "error": f"Generation failed after {self.max_retries} attempts: {str(e)}",
                    }
                continue

        return {
            "grd": None,
            "raw_response": None,
            "parsed_structure": None,
            "valid": False,
            "error": "Generation failed after maximum retries",
        }

    def _build_prompt(
        self,
        problem: str,
        problem_type: Optional[str] = None,
        custom_instructions: Optional[str] = None,
    ) -> str:
        """Build the prompt for GRD generation."""
        prompt_parts = [
            "You are an expert at creating structured reasoning diagrams.",
            "Your task is to create a Guided Reasoning Diagram (GRD) in Mermaid flowchart format",
            "that maps out the solution steps for a given problem.",
            "",
            "The GRD should:",
            "1. Start with problem analysis",
            "2. Break down the solution into clear, sequential steps",
            "3. Include decision points if the problem requires conditional logic",
            "4. End with the final answer or conclusion",
            "",
            "Use Mermaid flowchart syntax with the following format:",
            "```mermaid",
            "flowchart TD",
            "    Start[Problem Analysis] --> Step1[Step 1 Description]",
            "    Step1 --> Step2[Step 2 Description]",
            "    Step2 --> Answer[Final Answer]",
            "```",
        ]

        if problem_type:
            prompt_parts.append(f"\nProblem Type: {problem_type}")

        if custom_instructions:
            prompt_parts.append(f"\nAdditional Instructions: {custom_instructions}")

        prompt_parts.append("\nExamples:")
        for i, example in enumerate(self.examples, 1):
            prompt_parts.append(f"\nExample {i}:")
            prompt_parts.append(f"Problem: {example['problem']}")
            prompt_parts.append(f"GRD:\n{example['grd']}")

        prompt_parts.append("\n\nNow create a GRD for this problem:")
        prompt_parts.append(f"Problem: {problem}")
        prompt_parts.append("\nGenerate the Mermaid flowchart:")

        return "\n".join(prompt_parts)

    def add_example(self, problem: str, grd: str):
        """
        Add a custom example to the generator.

        Args:
            problem: Example problem
            grd: Example GRD in Mermaid format
        """
        self.examples.append({"problem": problem, "grd": grd})

    def get_template(self, problem_type: str) -> Optional[str]:
        """
        Get a template GRD for a specific problem type.

        Args:
            problem_type: Type of problem (e.g., "math", "logic", "reasoning")

        Returns:
            Template Mermaid code or None
        """
        templates = {
            "math": """```mermaid
flowchart TD
    Start[Read Problem] --> Identify[Identify Given Values]
    Identify --> Formula[Recall Relevant Formula]
    Formula --> Substitute[Substitute Values]
    Substitute --> Calculate[Perform Calculation]
    Calculate --> Verify[Verify Answer]
    Verify --> Answer[Final Answer]
```""",
            "logic": """```mermaid
flowchart TD
    Start[Problem Analysis] --> Premises[Identify Premises]
    Premises --> Rules[Apply Logical Rules]
    Rules --> Deduce[Deduce Conclusion]
    Deduce --> Answer[Final Conclusion]
```""",
            "reasoning": """```mermaid
flowchart TD
    Start[Understand Problem] --> Break[Break into Sub-problems]
    Break --> Solve[Solve Each Sub-problem]
    Solve --> Combine[Combine Solutions]
    Combine --> Answer[Final Answer]
```""",
        }

        return templates.get(problem_type.lower())
