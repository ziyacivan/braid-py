"""Mermaid diagram parser for Guided Reasoning Diagrams (GRD)."""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class NodeType(Enum):
    """Types of nodes in a Mermaid diagram."""

    RECTANGLE = "rectangle"  # [text]
    ROUNDED = "rounded"  # (text)
    STADIUM = "stadium"  # ([text])
    SUBROUTINE = "subroutine"  # [[text]]
    CYLINDRICAL = "cylindrical"  # [(text)]
    CIRCLE = "circle"  # ((text))
    DIAMOND = "diamond"  # {text}
    HEXAGON = "hexagon"  # {{text}}
    PARALLELOGRAM = "parallelogram"  # [/text/] or [\text\]
    TRAPEZOID = "trapezoid"  # [/text\] or [\text/]
    UNKNOWN = "unknown"


@dataclass
class GRDNode:
    """Represents a node in a Guided Reasoning Diagram."""

    id: str
    label: str
    node_type: NodeType = NodeType.RECTANGLE
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GRDEdge:
    """Represents an edge in a Guided Reasoning Diagram."""

    from_node: str
    to_node: str
    label: Optional[str] = None
    style: Optional[str] = None
    condition: Optional[str] = None


@dataclass
class GRDStructure:
    """Complete structure of a Guided Reasoning Diagram."""

    nodes: List[GRDNode] = field(default_factory=list)
    edges: List[GRDEdge] = field(default_factory=list)
    start_nodes: List[str] = field(default_factory=list)
    end_nodes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def get_node_by_id(self, node_id: str) -> Optional[GRDNode]:
        """Get a node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_outgoing_edges(self, node_id: str) -> List[GRDEdge]:
        """Get all edges outgoing from a node."""
        return [edge for edge in self.edges if edge.from_node == node_id]

    def get_incoming_edges(self, node_id: str) -> List[GRDEdge]:
        """Get all edges incoming to a node."""
        return [edge for edge in self.edges if edge.to_node == node_id]

    def get_execution_order(self) -> List[str]:
        """
        Get the execution order of nodes using topological sort.
        Returns a list of node IDs in execution order.
        """
        # Build adjacency list
        in_degree = {node.id: 0 for node in self.nodes}
        graph = {node.id: [] for node in self.nodes}

        for edge in self.edges:
            graph[edge.from_node].append(edge.to_node)
            in_degree[edge.to_node] = in_degree.get(edge.to_node, 0) + 1

        # Find start nodes (nodes with no incoming edges)
        queue = [node_id for node_id, degree in in_degree.items() if degree == 0]
        result = []

        while queue:
            node_id = queue.pop(0)
            result.append(node_id)

            for neighbor in graph[node_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        return result


class MermaidParser:
    """Parser for Mermaid flowchart diagrams."""

    # Node pattern: node_id[text] or node_id(text) or node_id{text} etc.
    NODE_PATTERNS = [
        (r"(\w+)\[\[(.*?)\]\]", NodeType.SUBROUTINE),  # [[text]]
        (r"(\w+)\[\((.*?)\)\]", NodeType.STADIUM),  # [(text)]
        (r"(\w+)\(\((.*?)\)\)", NodeType.CIRCLE),  # ((text))
        (r"(\w+)\{(.*?)\}", NodeType.DIAMOND),  # {text}
        (r"(\w+)\{\{(.*?)\}\}", NodeType.HEXAGON),  # {{text}}
        (r"(\w+)\((.*?)\)", NodeType.ROUNDED),  # (text)
        (r"(\w+)\[(.*?)\]", NodeType.RECTANGLE),  # [text]
        (r"(\w+)\[/?(.*?)[/\\]\]", NodeType.PARALLELOGRAM),  # [/text/] or [\text\]
    ]

    # Edge pattern: node1 --> node2 or node1 -->|label| node2
    EDGE_PATTERN = r"(\w+)\s*(--[>]|==[>])\s*(\w+)|(\w+)\s*--[->]\s*\|\s*(.*?)\s*\|\s*(\w+)"

    def __init__(self):
        """Initialize the parser."""
        pass

    def parse(self, mermaid_code: str) -> GRDStructure:
        """
        Parse Mermaid flowchart code into a GRD structure.

        Args:
            mermaid_code: Mermaid diagram code (flowchart format)

        Returns:
            GRDStructure object containing parsed nodes and edges

        Raises:
            ValueError: If the Mermaid code is invalid or cannot be parsed
        """
        if not mermaid_code:
            raise ValueError("Mermaid code cannot be empty")

        # Clean the code
        mermaid_code = self._clean_code(mermaid_code)

        # Check if it's a flowchart
        if not self._is_flowchart(mermaid_code):
            raise ValueError("Only flowchart diagrams are supported")

        # Parse nodes
        nodes = self._parse_nodes(mermaid_code)

        # Parse edges
        edges = self._parse_edges(mermaid_code, nodes)

        # Identify start and end nodes
        start_nodes, end_nodes = self._identify_start_end_nodes(nodes, edges)

        return GRDStructure(nodes=nodes, edges=edges, start_nodes=start_nodes, end_nodes=end_nodes)

    def _clean_code(self, code: str) -> str:
        """Clean and normalize Mermaid code."""
        # Remove markdown code blocks if present
        # Match opening ```mermaid or ```
        if code.strip().startswith('```'):
            # Find the first newline after ```
            lines = code.split('\n')
            # Skip the first line if it starts with ```
            if lines[0].strip().startswith('```'):
                lines = lines[1:]
            # Remove the last line if it's just ```
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            code = '\n'.join(lines)

        # Remove comments (line comments)
        code = re.sub(r"%%.*", "", code, flags=re.MULTILINE)

        # Normalize multiple spaces to single space, but preserve newlines
        # Replace multiple spaces/tabs with single space, but keep newlines
        lines = code.split('\n')
        cleaned_lines = [re.sub(r'[ \t]+', ' ', line).strip() for line in lines]
        code = '\n'.join(cleaned_lines)
        
        # Remove empty lines
        code = re.sub(r'\n\s*\n', '\n', code)
        code = code.strip()

        return code

    def _is_flowchart(self, code: str) -> bool:
        """Check if the code is a flowchart diagram."""
        return bool(re.search(r"^\s*(graph|flowchart)", code, re.MULTILINE | re.IGNORECASE))

    def _parse_nodes(self, code: str) -> List[GRDNode]:
        """Parse all nodes from Mermaid code."""
        nodes = []
        seen_ids = set()

        # Try each node pattern
        for pattern, node_type in self.NODE_PATTERNS:
            for match in re.finditer(pattern, code):
                node_id = match.group(1)
                label = match.group(2).strip() if len(match.groups()) > 1 else ""

                if node_id not in seen_ids:
                    nodes.append(GRDNode(id=node_id, label=label, node_type=node_type))
                    seen_ids.add(node_id)

        # Also extract node IDs from edges (they might not have explicit definitions)
        edge_matches = re.finditer(self.EDGE_PATTERN, code)
        for match in edge_matches:
            for group_idx in [1, 3, 4, 6]:
                if group_idx <= len(match.groups()) and match.group(group_idx):
                    node_id = match.group(group_idx)
                    if node_id not in seen_ids:
                        nodes.append(
                            GRDNode(
                                id=node_id,
                                label=node_id,  # Use ID as label if not defined
                                node_type=NodeType.RECTANGLE,
                            )
                        )
                        seen_ids.add(node_id)

        return nodes

    def _parse_edges(self, code: str, nodes: List[GRDNode]) -> List[GRDEdge]:
        """Parse all edges from Mermaid code."""
        edges = []
        node_ids = {node.id for node in nodes}

        # Pattern 1: node1 --> node2 (simple edge)
        # Pattern 2: node1 -->|label| node2 (labeled edge)
        # Pattern 3: node1 ==> node2 (thick edge)
        # Pattern 4: node1 ==|label|==> node2 (labeled thick edge)
        
        # Node definitions can be: nodeId[label] or nodeId(label) etc.
        # We need to match edges that may have node definitions before/after the arrow
        # Pattern: nodeId[optional_label] -->|optional_label| nodeId[optional_label]
        
        # First, try to match labeled edges: node1[label1] -->|edge_label| node2[label2]
        # or: node1 -->|edge_label| node2
        labeled_pattern = r"(\w+)(?:\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\})?\s*--[->]\s*\|\s*(.*?)\s*\|\s*(\w+)(?:\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\})?"
        for match in re.finditer(labeled_pattern, code):
            from_node = match.group(1)
            label = match.group(2).strip()
            to_node = match.group(3)
            
            if from_node in node_ids and to_node in node_ids:
                edges.append(GRDEdge(from_node=from_node, to_node=to_node, label=label, style="-->"))
        
        # Then, try to match simple edges: node1[label1] --> node2[label2]
        # or: node1 --> node2
        simple_pattern = r"(\w+)(?:\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\})?\s*(--[>]|==[>])\s*(\w+)(?:\[[^\]]*\]|\([^\)]*\)|\{[^\}]*\})?"
        for match in re.finditer(simple_pattern, code):
            from_node = match.group(1)
            edge_style = match.group(2)
            to_node = match.group(3)
            
            # Check if this edge was already captured as a labeled edge
            already_captured = any(
                e.from_node == from_node and e.to_node == to_node for e in edges
            )
            
            if not already_captured and from_node in node_ids and to_node in node_ids:
                edges.append(
                    GRDEdge(
                        from_node=from_node,
                        to_node=to_node,
                        style=edge_style.strip() if edge_style else None,
                    )
                )

        return edges

    def _identify_start_end_nodes(
        self, nodes: List[GRDNode], edges: List[GRDEdge]
    ) -> Tuple[List[str], List[str]]:
        """Identify start and end nodes based on edge connections."""
        node_ids = {node.id for node in nodes}
        has_incoming = {edge.to_node for edge in edges}
        has_outgoing = {edge.from_node for edge in edges}

        # Start nodes: nodes with no incoming edges
        start_nodes = [node_id for node_id in node_ids if node_id not in has_incoming]

        # End nodes: nodes with no outgoing edges
        end_nodes = [node_id for node_id in node_ids if node_id not in has_outgoing]

        return start_nodes, end_nodes

    def validate(self, mermaid_code: str) -> Tuple[bool, Optional[str]]:
        """
        Validate Mermaid code syntax.

        Args:
            mermaid_code: Mermaid diagram code to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            self.parse(mermaid_code)
            return True, None
        except ValueError as e:
            return False, str(e)

    def extract_execution_steps(self, grd: GRDStructure) -> List[Dict[str, Any]]:
        """
        Extract execution steps from a GRD structure.

        Args:
            grd: Parsed GRD structure

        Returns:
            List of execution steps with node information
        """
        execution_order = grd.get_execution_order()
        steps = []

        for node_id in execution_order:
            node = grd.get_node_by_id(node_id)
            if node:
                outgoing = grd.get_outgoing_edges(node_id)
                steps.append(
                    {
                        "step_id": node_id,
                        "label": node.label,
                        "node_type": node.node_type.value,
                        "next_steps": [edge.to_node for edge in outgoing],
                        "conditions": [edge.condition for edge in outgoing if edge.condition],
                    }
                )

        return steps
