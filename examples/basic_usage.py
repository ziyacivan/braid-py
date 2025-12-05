"""Basic usage example for BRAID-DSPy integration."""

from braid import BraidReasoning

# Configure DSPy with your language model
# For OpenAI:
# lm = dspy.OpenAI(model="gpt-4", api_key="your-api-key")
# dspy.configure(lm=lm)

# For local models or other providers, use appropriate DSPy LM class
# Example with a mock configuration (replace with actual LM):
print("Note: Configure DSPy with your language model before running")
print("Example: lm = dspy.OpenAI(model='gpt-4'); dspy.configure(lm=lm)")

# Create a BRAID reasoning module
braid = BraidReasoning()

# Example 1: Simple math problem
print("\n=== Example 1: Simple Math Problem ===")
problem1 = "If a train travels 120 km in 2 hours, what is its speed?"

# Note: This will fail without a configured LM, but shows the API
try:
    result1 = braid(problem=problem1)
    print(f"Problem: {problem1}")
    print(f"Answer: {result1.answer}")
    print(f"\nGRD:\n{result1.grd}")
    print(f"\nReasoning Steps:")
    for step in result1.reasoning_steps:
        print(f"  Step {step['step_number']}: {step['label']}")
        print(f"    Result: {step['result']}")
except Exception as e:
    print(f"Error (expected without LM configured): {e}")

# Example 2: Using a pre-generated GRD
print("\n=== Example 2: Using Pre-generated GRD ===")
pre_generated_grd = """```mermaid
flowchart TD
    Start[Problem Analysis] --> Identify[Identify given values:<br/>Distance = 120 km<br/>Time = 2 hours]
    Identify --> Formula[Recall speed formula:<br/>Speed = Distance / Time]
    Formula --> Calculate[Calculate:<br/>Speed = 120 / 2]
    Calculate --> Answer[Speed = 60 km/h]
```"""

try:
    result2 = braid(problem=problem1, grd=pre_generated_grd)
    print(f"Problem: {problem1}")
    print(f"Answer: {result2.answer}")
    print(f"\nExecution Trace:")
    for trace in result2.execution_trace:
        print(f"  {trace}")
except Exception as e:
    print(f"Error (expected without LM configured): {e}")

# Example 3: Custom configuration
print("\n=== Example 3: Custom Configuration ===")
braid_custom = BraidReasoning(use_generator=True, max_execution_steps=15, validate_grd=True)

print("BRAID module configured with:")
print(f"  - Use generator: {braid_custom.use_generator}")
print(f"  - Max execution steps: {braid_custom.max_execution_steps}")
print(f"  - Validate GRD: {braid_custom.validate_grd}")
