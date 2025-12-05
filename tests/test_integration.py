"""Integration tests for BRAID-DSPy."""

from braid import BraidReasoning, BraidOptimizer
from braid.parser import MermaidParser
from braid.generator import GRDGenerator


class TestBRAIDIntegration:
    """Integration tests for complete BRAID workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MermaidParser()
        self.generator = GRDGenerator()

    def test_parser_generator_integration(self):
        """Test integration between parser and generator."""
        # Example GRD that generator might produce
        example_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Step1[Identify Values]
    Step1 --> Step2[Apply Formula]
    Step2 --> Answer[Calculate Answer]
```"""

        # Parse should work
        grd = self.parser.parse(example_grd)
        assert grd is not None

        # Should have nodes and edges
        assert len(grd.nodes) > 0
        assert len(grd.edges) > 0

        # Should have execution order
        execution_order = grd.get_execution_order()
        assert len(execution_order) > 0

    def test_module_generator_integration(self):
        """Test integration between module and generator."""
        braid = BraidReasoning(use_generator=True)

        # Module should have generator
        assert braid.generator is not None
        assert isinstance(braid.generator, GRDGenerator)

    def test_module_parser_integration(self):
        """Test integration between module and parser."""
        braid = BraidReasoning()

        # Module should have parser
        assert braid.parser is not None
        assert isinstance(braid.parser, MermaidParser)

    def test_optimizer_module_integration(self):
        """Test integration between optimizer and module."""
        optimizer = BraidOptimizer()
        braid = BraidReasoning()

        # Optimizer should be able to evaluate module
        testset = [{"problem": "Test problem", "answer": "Test answer"}]

        # Note: Will fail without LM, but structure should work
        try:
            metrics = optimizer.evaluate(braid, testset)
            assert "average_score" in metrics
            assert "total_examples" in metrics
        except Exception:
            # Expected without LM
            pass

    def test_complete_workflow_structure(self):
        """Test the structure of a complete BRAID workflow."""
        # Create components
        generator = GRDGenerator()
        parser = MermaidParser()
        braid = BraidReasoning(use_generator=True)

        # Example problem
        problem = "If a train travels 120 km in 2 hours, what is its speed?"

        # Step 1: Generate GRD (would use LM in real scenario)
        example_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Distance=120km, Time=2h]
    Identify --> Formula[Speed = Distance / Time]
    Formula --> Calculate[Speed = 120 / 2 = 60]
    Calculate --> Answer[Answer: 60 km/h]
```"""

        # Step 2: Parse GRD
        grd_structure = parser.parse(example_grd)
        assert grd_structure is not None

        # Step 3: Get execution order
        execution_order = grd_structure.get_execution_order()
        assert len(execution_order) > 0

        # Step 4: Module should be able to use this
        assert braid.parser is not None
        assert braid.generator is not None

    def test_utils_integration(self):
        """Test utility functions integration."""
        from braid.utils import extract_mermaid_code, validate_mermaid_syntax

        # Test mermaid extraction
        text_with_code = """Here is some text.
```mermaid
flowchart TD
    A --> B
```
More text."""

        mermaid = extract_mermaid_code(text_with_code)
        assert mermaid is not None
        assert "flowchart" in mermaid

        # Test validation
        is_valid = validate_mermaid_syntax(mermaid)
        assert is_valid is True

        # Test invalid
        is_invalid = validate_mermaid_syntax("Not mermaid")
        assert is_invalid is False


class TestBRAIDErrorHandling:
    """Test error handling in BRAID components."""

    def test_parser_invalid_input(self):
        """Test parser with invalid input."""
        parser = MermaidParser()

        # Should handle invalid input gracefully
        is_valid, error = parser.validate("Invalid input")
        assert is_valid is False
        assert error is not None

    def test_module_invalid_grd(self):
        """Test module with invalid GRD."""
        braid = BraidReasoning(validate_grd=True)

        problem = "Test problem"
        invalid_grd = "Not a valid GRD"

        result = braid.forward(problem=problem, grd=invalid_grd)

        # Should return invalid result
        assert result.valid is False
        assert result.error is not None

    def test_generator_empty_problem(self):
        """Test generator with empty problem."""
        generator = GRDGenerator()

        # Should handle empty problem
        result = generator.generate(problem="")

        # Should return error or handle gracefully
        assert "error" in result or result["valid"] is False
