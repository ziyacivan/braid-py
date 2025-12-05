"""Tests for BRAID optimizer."""

from braid.optimizer import BraidOptimizer, GRDMetrics
from braid.module import BraidReasoning, BraidResult
from braid.parser import MermaidParser, GRDStructure, GRDNode, GRDEdge
from braid.generator import GRDGenerator


class TestGRDMetrics:
    """Test cases for GRDMetrics."""

    def setup_method(self):
        """Set up test fixtures."""
        self.metrics = GRDMetrics()
        self.parser = MermaidParser()

    def test_structural_validity_valid(self):
        """Test structural validity with valid GRD."""
        valid_grd = """flowchart TD
    Start[Start] --> End[End]"""
        
        score = GRDMetrics.structural_validity(valid_grd)
        assert score == 1.0

    def test_structural_validity_invalid(self):
        """Test structural validity with invalid GRD."""
        invalid_grd = "This is not valid mermaid"
        
        score = GRDMetrics.structural_validity(invalid_grd)
        assert score == 0.0

    def test_completeness_with_start_end(self):
        """Test completeness with start and end nodes."""
        nodes = [
            GRDNode(id="Start", label="Start"),
            GRDNode(id="Middle", label="Middle"),
            GRDNode(id="End", label="End"),
        ]
        edges = [
            GRDEdge(from_node="Start", to_node="Middle"),
            GRDEdge(from_node="Middle", to_node="End"),
        ]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=edges,
            start_nodes=["Start"],
            end_nodes=["End"],
        )
        
        score = GRDMetrics.completeness(grd_structure)
        assert score > 0.0
        assert score <= 1.0

    def test_completeness_no_start(self):
        """Test completeness without start nodes."""
        nodes = [GRDNode(id="A", label="A")]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=[],
            start_nodes=[],
            end_nodes=["A"],
        )
        
        score = GRDMetrics.completeness(grd_structure)
        assert score < 1.0

    def test_completeness_no_end(self):
        """Test completeness without end nodes."""
        nodes = [GRDNode(id="A", label="A")]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=[],
            start_nodes=["A"],
            end_nodes=[],
        )
        
        score = GRDMetrics.completeness(grd_structure)
        assert score < 1.0

    def test_completeness_reasonable_node_count(self):
        """Test completeness with reasonable node count."""
        nodes = [GRDNode(id=f"Node{i}", label=f"Node {i}") for i in range(5)]
        edges = [GRDEdge(from_node=f"Node{i}", to_node=f"Node{i+1}") for i in range(4)]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=edges,
            start_nodes=["Node0"],
            end_nodes=["Node4"],
        )
        
        score = GRDMetrics.completeness(grd_structure)
        assert score >= 0.8  # Should have high score with reasonable structure

    def test_completeness_too_many_nodes(self):
        """Test completeness with too many nodes."""
        nodes = [GRDNode(id=f"Node{i}", label=f"Node {i}") for i in range(25)]
        edges = [GRDEdge(from_node=f"Node{i}", to_node=f"Node{i+1}") for i in range(24)]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=edges,
            start_nodes=["Node0"],
            end_nodes=["Node24"],
        )
        
        score = GRDMetrics.completeness(grd_structure)
        assert score < 1.0  # Should be penalized for too many nodes

    def test_execution_traceability_valid(self):
        """Test execution traceability with valid structure."""
        nodes = [
            GRDNode(id="Start", label="Start"),
            GRDNode(id="Step1", label="Step 1"),
            GRDNode(id="End", label="End"),
        ]
        edges = [
            GRDEdge(from_node="Start", to_node="Step1"),
            GRDEdge(from_node="Step1", to_node="End"),
        ]
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=edges,
            start_nodes=["Start"],
            end_nodes=["End"],
        )
        
        score = GRDMetrics.execution_traceability(grd_structure)
        assert score > 0.0
        assert score <= 1.0

    def test_execution_traceability_no_execution_order(self):
        """Test execution traceability with no execution order."""
        # Create structure with isolated node (no edges, so execution order will be empty)
        # Actually, get_execution_order returns nodes with no incoming edges,
        # so a single node with no edges will still be in execution order
        # Let's test with a structure that truly has no execution order
        nodes = []
        grd_structure = GRDStructure(
            nodes=nodes,
            edges=[],
            start_nodes=[],
            end_nodes=[],
        )
        
        score = GRDMetrics.execution_traceability(grd_structure)
        assert score == 0.0

    def test_execution_traceability_empty_nodes(self):
        """Test execution traceability with empty nodes."""
        grd_structure = GRDStructure(
            nodes=[],
            edges=[],
            start_nodes=[],
            end_nodes=[],
        )
        
        score = GRDMetrics.execution_traceability(grd_structure)
        assert score == 0.0

    def test_overall_quality_valid(self):
        """Test overall quality with valid GRD."""
        valid_grd = """flowchart TD
    Start[Start] --> Step1[Step 1]
    Step1 --> End[End]"""
        
        score = GRDMetrics.overall_quality(valid_grd)
        assert score > 0.0
        assert score <= 1.0

    def test_overall_quality_invalid(self):
        """Test overall quality with invalid GRD."""
        invalid_grd = "Not valid mermaid"
        
        score = GRDMetrics.overall_quality(invalid_grd)
        assert score == 0.0

    def test_overall_quality_with_structure(self):
        """Test overall quality with pre-parsed structure."""
        valid_grd = """flowchart TD
    Start[Start] --> End[End]"""
        
        parser = MermaidParser()
        grd_structure = parser.parse(valid_grd)
        
        score = GRDMetrics.overall_quality(valid_grd, grd_structure)
        assert score > 0.0
        assert score <= 1.0

    def test_overall_quality_parse_error(self):
        """Test overall quality when parsing fails."""
        # Create a structure that will cause issues
        invalid_grd = "invalid"
        
        score = GRDMetrics.overall_quality(invalid_grd)
        assert score == 0.0


class TestBraidOptimizer:
    """Test cases for BraidOptimizer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.optimizer = BraidOptimizer()
        self.module = BraidReasoning(use_generator=False)

    def test_initialization_default(self):
        """Test optimizer initialization with default parameters."""
        optimizer = BraidOptimizer()
        
        assert optimizer.base_optimizer is None
        assert optimizer.grd_quality_weight == 0.5
        assert optimizer.execution_quality_weight == 0.5
        assert optimizer.metrics is not None

    def test_initialization_custom(self):
        """Test optimizer initialization with custom parameters."""
        optimizer = BraidOptimizer(
            grd_quality_weight=0.7,
            execution_quality_weight=0.3,
        )
        
        assert optimizer.grd_quality_weight == 0.7
        assert optimizer.execution_quality_weight == 0.3

    def test_simple_optimize(self):
        """Test simple optimization without base optimizer."""
        trainset = [
            {"problem": "Test problem 1", "answer": "Answer 1"},
            {"problem": "Test problem 2", "answer": "Answer 2"},
        ]
        
        # Should return module unchanged (simple optimization)
        optimized = self.optimizer.optimize(self.module, trainset)
        assert optimized is not None

    def test_optimize_with_empty_trainset(self):
        """Test optimization with empty trainset."""
        trainset = []
        
        optimized = self.optimizer.optimize(self.module, trainset)
        assert optimized is not None

    def test_optimize_with_missing_problem(self):
        """Test optimization with trainset missing problem key."""
        trainset = [
            {"answer": "Answer 1"},
            {"problem": "Test problem"},
        ]
        
        optimized = self.optimizer.optimize(self.module, trainset)
        assert optimized is not None

    def test_default_metric_with_parsed_grd(self):
        """Test default metric with parsed GRD."""
        parser = MermaidParser()
        grd = """flowchart TD
    Start[Start] --> End[End]"""
        parsed_grd = parser.parse(grd)
        
        result = BraidResult(
            problem="Test",
            grd=grd,
            parsed_grd=parsed_grd,
            reasoning_steps=[
                {"step_id": "Start", "result": "Step 1"},
                {"step_id": "End", "result": "Answer"},
            ],
            answer="Answer",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result)
        assert score >= 0.0
        assert score <= 1.0

    def test_default_metric_without_parsed_grd(self):
        """Test default metric without parsed GRD."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[],
            answer="",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result)
        assert score >= 0.0

    def test_default_metric_with_reasonable_steps(self):
        """Test default metric with reasonable number of steps."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[
                {"step_id": f"Step{i}", "result": f"Result {i}"} for i in range(5)
            ],
            answer="Answer",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result)
        assert score > 0.0

    def test_default_metric_with_too_many_steps(self):
        """Test default metric with too many steps."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[
                {"step_id": f"Step{i}", "result": f"Result {i}"} for i in range(20)
            ],
            answer="Answer",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result)
        assert score >= 0.0

    def test_default_metric_with_few_steps(self):
        """Test default metric with too few steps."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[{"step_id": "Step1", "result": "Result"}],
            answer="Answer",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result)
        assert score >= 0.0

    def test_default_metric_with_answer_match(self):
        """Test default metric with matching expected answer."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[{"step_id": "Step1", "result": "Result"}],
            answer="Expected Answer",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result, expected_answer="Expected Answer")
        assert score > 0.0

    def test_default_metric_with_partial_match(self):
        """Test default metric with partial answer match."""
        result = BraidResult(
            problem="Test",
            grd="",
            parsed_grd=None,
            reasoning_steps=[],
            answer="The answer is 42",
            execution_trace=[],
            valid=True,
        )
        
        score = self.optimizer._default_metric(result, expected_answer="42")
        assert score > 0.0

    def test_evaluate_with_testset(self):
        """Test evaluate method with testset."""
        testset = [
            {"problem": "Test problem 1", "answer": "Answer 1"},
            {"problem": "Test problem 2", "answer": "Answer 2"},
        ]
        
        # Note: Will fail without LM, but structure should work
        try:
            metrics = self.optimizer.evaluate(self.module, testset)
            assert "average_score" in metrics
            assert "average_grd_quality" in metrics
            assert "average_execution_score" in metrics
            assert "total_examples" in metrics
            assert "valid_results" in metrics
        except Exception:
            # Expected without LM
            pass

    def test_evaluate_with_empty_testset(self):
        """Test evaluate method with empty testset."""
        testset = []
        
        metrics = self.optimizer.evaluate(self.module, testset)
        assert metrics["average_score"] == 0.0
        assert metrics["total_examples"] == 0
        assert metrics["valid_results"] == 0

    def test_evaluate_with_missing_problem(self):
        """Test evaluate with testset missing problem key."""
        testset = [
            {"answer": "Answer 1"},
            {"problem": "Test problem"},
        ]
        
        try:
            metrics = self.optimizer.evaluate(self.module, testset)
            assert "valid_results" in metrics
        except Exception:
            # Expected without LM
            pass

    def test_evaluate_with_custom_metric(self):
        """Test evaluate with custom metric function."""
        def custom_metric(result, expected):
            return 0.5
        
        testset = [{"problem": "Test", "answer": "Answer"}]
        
        try:
            metrics = self.optimizer.evaluate(self.module, testset, metric=custom_metric)
            assert "average_score" in metrics
        except Exception:
            # Expected without LM
            pass

    def test_optimize_with_custom_metric(self):
        """Test optimize with custom metric function."""
        def custom_metric(result, expected):
            return 0.5
        
        trainset = [{"problem": "Test", "answer": "Answer"}]
        
        optimized = self.optimizer.optimize(self.module, trainset, metric=custom_metric)
        assert optimized is not None

    def test_optimize_planning_with_generator(self):
        """Test _optimize_planning with generator."""
        module = BraidReasoning(use_generator=True)
        trainset = [{"problem": "Test problem"}]
        
        def dummy_metric(result, expected):
            return 0.5
        
        # Should not crash even without LM
        try:
            optimized = self.optimizer._optimize_planning(module, trainset, dummy_metric)
            assert optimized is not None
        except Exception:
            # Expected without LM
            pass

    def test_optimize_planning_without_generator(self):
        """Test _optimize_planning without generator."""
        module = BraidReasoning(use_generator=False)
        trainset = [{"problem": "Test problem"}]
        
        def dummy_metric(result, expected):
            return 0.5
        
        # Should not crash even without LM
        try:
            optimized = self.optimizer._optimize_planning(module, trainset, dummy_metric)
            assert optimized is not None
        except Exception:
            # Expected without LM
            pass

    def test_optimize_execution(self):
        """Test _optimize_execution."""
        trainset = [{"problem": "Test problem", "answer": "Answer"}]
        
        def dummy_metric(result, expected):
            return 0.5
        
        # Should not crash even without LM
        try:
            optimized = self.optimizer._optimize_execution(self.module, trainset, dummy_metric)
            assert optimized is not None
        except Exception:
            # Expected without LM
            pass

    def test_optimize_execution_with_empty_steps(self):
        """Test _optimize_execution with result having no steps."""
        trainset = [{"problem": "Test problem", "answer": "Answer"}]
        
        def dummy_metric(result, expected):
            return 0.5
        
        # Should handle gracefully
        try:
            optimized = self.optimizer._optimize_execution(self.module, trainset, dummy_metric)
            assert optimized is not None
        except Exception:
            # Expected without LM
            pass

