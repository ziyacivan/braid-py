"""Optimization example for BRAID-DSPy."""

from braid import BraidReasoning, BraidOptimizer
from braid.parser import MermaidParser

# Configure DSPy
# lm = dspy.OpenAI(model="gpt-4", api_key="your-api-key")
# dspy.configure(lm=lm)

print("Note: Configure DSPy with your language model before running")

# Training examples
trainset = [
    {"problem": "If a train travels 120 km in 2 hours, what is its speed?", "answer": "60 km/h"},
    {"problem": "Solve: 3x + 5 = 14", "answer": "x = 3"},
    {
        "problem": "A rectangle has length 10 cm and width 5 cm. What is its area?",
        "answer": "50 cm²",
    },
]

# Test examples
testset = [
    {"problem": "If a car travels 240 km in 3 hours, what is its speed?", "answer": "80 km/h"},
    {"problem": "Solve: 2x - 7 = 11", "answer": "x = 9"},
]


def demonstrate_optimization():
    """Demonstrate BRAID optimization workflow."""

    # Step 1: Create initial BRAID module
    print("=== Step 1: Create Initial Module ===")
    braid = BraidReasoning(use_generator=True)
    print("BRAID module created")

    # Step 2: Evaluate before optimization
    print("\n=== Step 2: Evaluate Before Optimization ===")
    optimizer = BraidOptimizer()

    try:
        metrics_before = optimizer.evaluate(braid, testset)
        print("Metrics before optimization:")
        for key, value in metrics_before.items():
            print(f"  {key}: {value:.3f}" if isinstance(value, float) else f"  {key}: {value}")
    except Exception as e:
        print(f"Cannot evaluate without LM: {e}")
        print("(This is expected if DSPy is not configured)")

    # Step 3: Optimize
    print("\n=== Step 3: Optimize Module ===")
    print("Optimization process:")
    print("  1. Optimize GRD generation (planning phase)")
    print("  2. Optimize step-by-step execution")
    print("  3. Improve prompts based on metrics")

    # Note: Actual optimization requires a base optimizer
    # Example with MIPROv2:
    # from dspy.teleprompt import MIPROv2
    # base_optimizer = MIPROv2()
    # optimizer_with_base = BraidOptimizer(base_optimizer=base_optimizer)
    # optimized_braid = optimizer_with_base.optimize(braid, trainset)

    try:
        # Simple optimization (without base optimizer)
        optimized_braid = optimizer.optimize(braid, trainset)
        print("Optimization completed (simple mode)")
    except Exception as e:
        print(f"Cannot optimize without LM: {e}")
        print("(This is expected if DSPy is not configured)")
        optimized_braid = braid

    # Step 4: Evaluate after optimization
    print("\n=== Step 4: Evaluate After Optimization ===")
    try:
        metrics_after = optimizer.evaluate(optimized_braid, testset)
        print("Metrics after optimization:")
        for key, value in metrics_after.items():
            print(f"  {key}: {value:.3f}" if isinstance(value, float) else f"  {key}: {value}")

        # Compare
        if "average_score" in metrics_before and "average_score" in metrics_after:
            improvement = metrics_after["average_score"] - metrics_before["average_score"]
            print(f"\nScore improvement: {improvement:+.3f}")
    except Exception as e:
        print(f"Cannot evaluate without LM: {e}")

    # Step 5: Custom metrics
    print("\n=== Step 5: Custom Metrics ===")
    print("You can define custom metrics for optimization:")
    print(
        """
def custom_metric(result, expected_answer):
    # Your custom evaluation logic
    score = 0.0
    if result.answer and expected_answer:
        # Check answer correctness
        if expected_answer.lower() in result.answer.lower():
            score += 0.5
        # Check GRD quality
        if result.parsed_grd:
            score += 0.3
        # Check reasoning steps
        if len(result.reasoning_steps) >= 2:
            score += 0.2
    return score

optimizer = BraidOptimizer()
optimized = optimizer.optimize(braid, trainset, metric=custom_metric)
    """
    )


def demonstrate_grd_metrics():
    """Demonstrate GRD quality metrics."""
    print("\n=== GRD Quality Metrics ===")

    from braid.optimizer import GRDMetrics

    # Example GRD
    example_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify given values]
    Identify --> Formula[Recall formula]
    Formula --> Calculate[Calculate]
    Calculate --> Answer[Final Answer]
```"""

    print("Example GRD:")
    print(example_grd)

    # Calculate metrics
    parser = MermaidParser()
    try:
        grd_structure = parser.parse(example_grd)

        validity = GRDMetrics.structural_validity(example_grd)
        completeness = GRDMetrics.completeness(grd_structure)
        traceability = GRDMetrics.execution_traceability(grd_structure)
        overall = GRDMetrics.overall_quality(example_grd, grd_structure)

        print("\nGRD Metrics:")
        print(f"  Structural Validity: {validity:.3f}")
        print(f"  Completeness: {completeness:.3f}")
        print(f"  Execution Traceability: {traceability:.3f}")
        print(f"  Overall Quality: {overall:.3f}")
    except Exception as e:
        print(f"Error parsing GRD: {e}")


if __name__ == "__main__":
    demonstrate_optimization()
    demonstrate_grd_metrics()
