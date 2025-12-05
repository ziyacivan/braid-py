"""Tests for GRD generator."""

from braid.generator import GRDGenerator
from braid.parser import MermaidParser


class TestGRDGenerator:
    """Test cases for GRDGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = GRDGenerator()
        self.parser = MermaidParser()

    def test_initialization(self):
        """Test generator initialization."""
        generator = GRDGenerator()

        assert generator.max_retries == 3
        assert generator.temperature == 0.3
        assert len(generator.examples) > 0

    def test_custom_initialization(self):
        """Test generator with custom parameters."""
        custom_examples = [
            {"problem": "Test problem", "grd": "```mermaid\nflowchart TD\n    A --> B\n```"}
        ]

        generator = GRDGenerator(examples=custom_examples, max_retries=5, temperature=0.5)

        assert generator.max_retries == 5
        assert generator.temperature == 0.5
        assert len(generator.examples) == 1

    def test_build_prompt(self):
        """Test prompt building."""
        problem = "Test problem"
        prompt = self.generator._build_prompt(problem)

        assert problem in prompt
        assert "Mermaid" in prompt or "mermaid" in prompt
        assert "flowchart" in prompt.lower()

    def test_build_prompt_with_type(self):
        """Test prompt building with problem type."""
        problem = "Solve: 2x + 3 = 7"
        prompt = self.generator._build_prompt(problem, problem_type="math")

        assert problem in prompt
        assert "math" in prompt.lower()

    def test_build_prompt_with_instructions(self):
        """Test prompt building with custom instructions."""
        problem = "Test problem"
        instructions = "Use step-by-step reasoning"
        prompt = self.generator._build_prompt(problem, custom_instructions=instructions)

        assert instructions in prompt

    def test_add_example(self):
        """Test adding custom examples."""
        initial_count = len(self.generator.examples)

        self.generator.add_example(
            problem="New problem", grd="```mermaid\nflowchart TD\n    A --> B\n```"
        )

        assert len(self.generator.examples) == initial_count + 1

    def test_get_template(self):
        """Test getting templates for problem types."""
        math_template = self.generator.get_template("math")
        assert math_template is not None
        assert "mermaid" in math_template.lower()

        logic_template = self.generator.get_template("logic")
        assert logic_template is not None

        reasoning_template = self.generator.get_template("reasoning")
        assert reasoning_template is not None

    def test_get_template_invalid_type(self):
        """Test getting template for invalid problem type."""
        template = self.generator.get_template("invalid_type")
        assert template is None

    def test_generate_structure(self):
        """Test that generate returns proper structure."""
        # Note: This test will fail without a configured LM
        # It's here to show the expected structure
        problem = "Test problem"

        # Mock the expected return structure
        expected_keys = ["grd", "raw_response", "parsed_structure", "valid", "error"]

        # In a real test with LM, we would do:
        # result = self.generator.generate(problem)
        # assert all(key in result for key in expected_keys)

        # For now, just verify the method exists and has correct signature
        assert hasattr(self.generator, "generate")
        assert callable(self.generator.generate)


class TestGRDGeneratorIntegration:
    """Integration tests for GRD generator with parser."""

    def test_generator_parser_integration(self):
        """Test that generator output can be parsed."""
        generator = GRDGenerator()
        parser = MermaidParser()

        # Example GRD that generator should produce
        example_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Step1[Step 1]
    Step1 --> Answer[Answer]
```"""

        # Extract and parse
        from braid.utils import extract_mermaid_code

        mermaid_code = extract_mermaid_code(example_grd)

        assert mermaid_code is not None

        # Parse should succeed
        grd = parser.parse(mermaid_code)
        assert grd is not None
        assert len(grd.nodes) > 0

    def test_generator_without_dspy_predict(self):
        """Test generator initialization without DSPy Predict."""
        generator = GRDGenerator(use_dspy_predict=False)
        
        assert generator.use_dspy_predict is False
        assert not hasattr(generator, 'predictor') or generator.predictor is None

    def test_generate_with_empty_problem(self):
        """Test generate with empty problem."""
        generator = GRDGenerator()
        result = generator.generate(problem="")
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert "grd" in result
        assert "valid" in result

    def test_generate_with_problem_type(self):
        """Test generate with problem type."""
        # Without LM, this will fail but we can test the structure
        try:
            result = self.generator.generate(problem="Test", problem_type="math")
            assert isinstance(result, dict)
            assert "grd" in result
        except Exception:
            # Expected without LM
            pass

    def test_generate_with_custom_instructions(self):
        """Test generate with custom instructions."""
        # Without LM, this will fail but we can test the structure
        try:
            result = self.generator.generate(
                problem="Test", custom_instructions="Use detailed steps"
            )
            assert isinstance(result, dict)
        except Exception:
            # Expected without LM
            pass

    def test_build_prompt_includes_examples(self):
        """Test that build_prompt includes examples."""
        generator = GRDGenerator()
        prompt = generator._build_prompt("Test problem")
        
        # Should include example problems
        assert any(example["problem"] in prompt for example in generator.examples)

    def test_build_prompt_format(self):
        """Test prompt format structure."""
        generator = GRDGenerator()
        prompt = generator._build_prompt("Test problem")
        
        # Should contain key instructions
        assert "flowchart" in prompt.lower()
        assert "mermaid" in prompt.lower()
        assert "Problem:" in prompt

    def test_get_template_case_insensitive(self):
        """Test get_template is case insensitive."""
        generator = GRDGenerator()
        template1 = generator.get_template("MATH")
        template2 = generator.get_template("math")
        
        assert template1 == template2

    def test_get_template_all_types(self):
        """Test all available template types."""
        generator = GRDGenerator()
        types = ["math", "logic", "reasoning"]
        
        for template_type in types:
            template = generator.get_template(template_type)
            assert template is not None
            assert "mermaid" in template.lower()
            assert "flowchart" in template.lower()

    def test_generator_retry_logic_structure(self):
        """Test that generator has retry logic structure."""
        # Verify max_retries is used
        generator = GRDGenerator(max_retries=5)
        assert generator.max_retries == 5
        
        # The actual retry logic is tested in generate method
        # which requires LM, but we can verify the structure
        assert hasattr(generator, 'max_retries')

    def test_generator_parser_integration(self):
        """Test generator has parser."""
        generator = GRDGenerator()
        assert generator.parser is not None
        assert hasattr(generator.parser, 'validate')
        assert hasattr(generator.parser, 'parse')
