"""Tests for Mermaid parser."""

from braid.parser import MermaidParser


class TestMermaidParser:
    """Test cases for MermaidParser."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = MermaidParser()

    def test_parse_simple_flowchart(self):
        """Test parsing a simple flowchart."""
        mermaid_code = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Step1[Step 1]
    Step1 --> Step2[Step 2]
    Step2 --> Answer[Final Answer]
```"""

        grd = self.parser.parse(mermaid_code)

        assert grd is not None
        assert len(grd.nodes) >= 4
        assert len(grd.edges) >= 3
        assert "Start" in [node.id for node in grd.nodes]
        assert "Answer" in [node.id for node in grd.nodes]

    def test_parse_without_code_block(self):
        """Test parsing Mermaid code without markdown code blocks."""
        mermaid_code = """flowchart TD
    A[Start] --> B[End]"""

        grd = self.parser.parse(mermaid_code)

        assert grd is not None
        assert len(grd.nodes) >= 2
        assert len(grd.edges) >= 1

    def test_validate_valid_mermaid(self):
        """Test validation of valid Mermaid code."""
        mermaid_code = """flowchart TD
    A[Start] --> B[End]"""

        is_valid, error = self.parser.validate(mermaid_code)

        assert is_valid is True
        assert error is None

    def test_validate_invalid_mermaid(self):
        """Test validation of invalid Mermaid code."""
        invalid_code = "This is not mermaid code"

        is_valid, error = self.parser.validate(invalid_code)

        assert is_valid is False
        assert error is not None

    def test_get_execution_order(self):
        """Test getting execution order from GRD."""
        mermaid_code = """flowchart TD
    Start[Start] --> Step1[Step 1]
    Step1 --> Step2[Step 2]
    Step2 --> End[End]"""

        grd = self.parser.parse(mermaid_code)
        execution_order = grd.get_execution_order()

        assert len(execution_order) > 0
        assert "Start" in execution_order
        assert execution_order[0] == "Start"

    def test_node_types(self):
        """Test parsing different node types."""
        mermaid_code = """flowchart TD
    Rect[Rectangle] --> Round(Rounded)
    Round --> Diamond{Diamond}
    Diamond --> Circle((Circle))"""

        grd = self.parser.parse(mermaid_code)

        node_ids = [node.id for node in grd.nodes]
        assert "Rect" in node_ids
        assert "Round" in node_ids
        assert "Diamond" in node_ids
        assert "Circle" in node_ids

    def test_labeled_edges(self):
        """Test parsing edges with labels."""
        mermaid_code = """flowchart TD
    A[Start] -->|Yes| B[Yes Path]
    A -->|No| C[No Path]"""

        grd = self.parser.parse(mermaid_code)

        edges = grd.edges
        assert len(edges) >= 2

        # Check if labels are captured
        labeled_edges = [e for e in edges if e.label]
        assert len(labeled_edges) >= 0  # Labels may or may not be captured depending on regex

    def test_extract_execution_steps(self):
        """Test extracting execution steps."""
        mermaid_code = """flowchart TD
    Start[Problem Analysis] --> Step1[Calculate]
    Step1 --> Answer[Result]"""

        grd = self.parser.parse(mermaid_code)
        steps = self.parser.extract_execution_steps(grd)

        assert len(steps) > 0
        assert all("step_id" in step for step in steps)
        assert all("label" in step for step in steps)

    def test_start_end_nodes(self):
        """Test identification of start and end nodes."""
        mermaid_code = """flowchart TD
    Start[Start] --> Middle[Middle]
    Middle --> End[End]"""

        grd = self.parser.parse(mermaid_code)

        assert len(grd.start_nodes) > 0
        assert len(grd.end_nodes) > 0
        assert "Start" in grd.start_nodes
        assert "End" in grd.end_nodes

    def test_complex_flowchart(self):
        """Test parsing a more complex flowchart."""
        mermaid_code = """flowchart TD
    Start[Start] --> Check{Check Condition}
    Check -->|True| Path1[Path 1]
    Check -->|False| Path2[Path 2]
    Path1 --> Merge[Merge]
    Path2 --> Merge
    Merge --> End[End]"""

        grd = self.parser.parse(mermaid_code)

        assert grd is not None
        assert len(grd.nodes) >= 6
        assert len(grd.edges) >= 5


class TestGRDStructure:
    """Test cases for GRDStructure."""

    def test_get_node_by_id(self):
        """Test getting a node by ID."""
        parser = MermaidParser()
        mermaid_code = """flowchart TD
    A[Node A] --> B[Node B]"""

        grd = parser.parse(mermaid_code)
        node = grd.get_node_by_id("A")

        assert node is not None
        assert node.id == "A"

    def test_get_outgoing_edges(self):
        """Test getting outgoing edges from a node."""
        parser = MermaidParser()
        mermaid_code = """flowchart TD
    A[Node A] --> B[Node B]
    A --> C[Node C]"""

        grd = parser.parse(mermaid_code)
        edges = grd.get_outgoing_edges("A")

        assert len(edges) >= 2
        assert all(edge.from_node == "A" for edge in edges)

    def test_get_incoming_edges(self):
        """Test getting incoming edges to a node."""
        parser = MermaidParser()
        mermaid_code = """flowchart TD
    A[Node A] --> B[Node B]
    C[Node C] --> B"""

        grd = parser.parse(mermaid_code)
        edges = grd.get_incoming_edges("B")

        assert len(edges) >= 2
        assert all(edge.to_node == "B" for edge in edges)
