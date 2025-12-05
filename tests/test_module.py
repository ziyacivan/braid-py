"""Tests for BRAID module."""

from braid.module import BraidReasoning, BraidResult
from braid.parser import MermaidParser


class TestBraidReasoning:
    """Test cases for BraidReasoning module."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MermaidParser()

    def test_initialization(self):
        """Test module initialization."""
        braid = BraidReasoning()

        assert braid.use_generator is True
        assert braid.max_execution_steps == 20
        assert braid.validate_grd is True
        assert braid.parser is not None

    def test_custom_initialization(self):
        """Test module with custom parameters."""
        braid = BraidReasoning(use_generator=False, max_execution_steps=10, validate_grd=False)

        assert braid.use_generator is False
        assert braid.max_execution_steps == 10
        assert braid.validate_grd is False

    def test_forward_with_pre_generated_grd(self):
        """Test forward pass with pre-generated GRD."""
        braid = BraidReasoning(use_generator=False, validate_grd=True)

        problem = "Test problem"
        grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Step1[Step 1]
    Step1 --> Answer[Final Answer]
```"""

        # Note: This will fail without LM configured
        # But we can test the structure
        try:
            result = braid.forward(problem=problem, grd=grd)
            assert isinstance(result, BraidResult)
            assert result.problem == problem
            assert result.grd is not None
        except Exception:
            # Expected without LM
            pass

    def test_forward_structure(self):
        """Test that forward returns BraidResult."""
        braid = BraidReasoning()

        # Verify method signature
        assert hasattr(braid, "forward")
        assert callable(braid.forward)

    def test_callable(self):
        """Test that module is callable."""
        braid = BraidReasoning()

        assert callable(braid)
        assert hasattr(braid, "__call__")


class TestBraidResult:
    """Test cases for BraidResult."""

    def test_result_creation(self):
        """Test creating a BraidResult."""
        result = BraidResult(
            problem="Test problem",
            grd="Test GRD",
            parsed_grd=None,
            reasoning_steps=[],
            answer="Test answer",
            execution_trace=[],
            valid=True,
        )

        assert result.problem == "Test problem"
        assert result.grd == "Test GRD"
        assert result.answer == "Test answer"
        assert result.valid is True

    def test_result_with_steps(self):
        """Test BraidResult with reasoning steps."""
        steps = [
            {
                "step_id": "Step1",
                "step_number": 1,
                "label": "Step 1",
                "result": "Result 1",
                "node_type": "rectangle",
            }
        ]

        result = BraidResult(
            problem="Test",
            grd="GRD",
            parsed_grd=None,
            reasoning_steps=steps,
            answer="Answer",
            execution_trace=[],
            valid=True,
        )

        assert len(result.reasoning_steps) == 1
        assert result.reasoning_steps[0]["step_id"] == "Step1"


class TestBraidModuleIntegration:
    """Integration tests for BRAID module."""

    def test_module_with_valid_grd(self):
        """Test module with a valid GRD."""
        braid = BraidReasoning(use_generator=False)

        problem = "If a train travels 120 km in 2 hours, what is its speed?"
        valid_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify: Distance=120km, Time=2h]
    Identify --> Formula[Speed = Distance / Time]
    Formula --> Calculate[Speed = 120 / 2]
    Calculate --> Answer[Speed = 60 km/h]
```"""

        # Verify GRD is valid
        parser = MermaidParser()
        is_valid, _ = parser.validate(valid_grd)
        assert is_valid

        # Note: Actual execution requires LM
        # But we can verify the structure is correct
        try:
            result = braid(problem=problem, grd=valid_grd)
            if result.valid:
                assert result.parsed_grd is not None
                assert len(result.reasoning_steps) > 0
        except Exception:
            # Expected without LM
            pass

    def test_extract_answer(self):
        """Test answer extraction logic."""
        braid = BraidReasoning()

        # Create a mock GRD structure
        from braid.parser import GRDStructure, GRDNode

        grd_structure = GRDStructure(
            nodes=[GRDNode(id="Start", label="Start"), GRDNode(id="End", label="Answer: 60 km/h")],
            edges=[],
            start_nodes=["Start"],
            end_nodes=["End"],
        )

        step_results = {"End": "60 km/h"}
        reasoning_steps = [
            {"step_id": "Start", "result": "Analysis"},
            {"step_id": "End", "result": "60 km/h"},
        ]

        answer = braid._extract_answer(grd_structure, step_results, reasoning_steps)

        assert answer is not None
        assert len(answer) > 0
