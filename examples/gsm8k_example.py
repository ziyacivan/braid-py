"""GSM8K benchmark example using BRAID-DSPy."""

from braid import BraidReasoning, BraidOptimizer

# Configure DSPy
# lm = dspy.OpenAI(model="gpt-4", api_key="your-api-key")
# dspy.configure(lm=lm)

print("Note: Configure DSPy with your language model before running")
print("Example: lm = dspy.OpenAI(model='gpt-4'); dspy.configure(lm=lm)")

# Sample GSM8K problems (grade school math word problems)
gsm8k_examples = [
    {
        "problem": "Natalia sold clips to 48 of her friends in April, and then she sold half as many clips in May. How many clips did Natalia sell altogether in April and May?",
        "answer": "72",
    },
    {"problem": "A train travels 120 km in 2 hours. What is its speed in km/h?", "answer": "60"},
    {
        "problem": "Janet's ducks lay 16 eggs per day. She eats 3 for breakfast every morning and bakes 4 for her friends every day. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?",
        "answer": "18",
    },
]


def evaluate_gsm8k(module: BraidReasoning, examples: list):
    """
    Evaluate BRAID module on GSM8K examples.

    Args:
        module: BraidReasoning module
        examples: List of examples with 'problem' and 'answer' keys
    """
    results = []

    for i, example in enumerate(examples, 1):
        problem = example["problem"]
        expected_answer = example["answer"]

        print(f"\n--- Problem {i} ---")
        print(f"Problem: {problem}")
        print(f"Expected Answer: {expected_answer}")

        try:
            result = module(problem=problem)

            print(f"Generated Answer: {result.answer}")
            print(f"Valid: {result.valid}")

            if result.parsed_grd:
                print(f"GRD Nodes: {len(result.parsed_grd.nodes)}")
                print(f"GRD Edges: {len(result.parsed_grd.edges)}")
                print(f"Execution Steps: {len(result.reasoning_steps)}")

            # Simple answer extraction check
            answer_match = (
                expected_answer.lower() in result.answer.lower()
                or result.answer.lower() in expected_answer.lower()
            )

            results.append(
                {
                    "problem": problem,
                    "expected": expected_answer,
                    "got": result.answer,
                    "correct": answer_match,
                    "valid": result.valid,
                }
            )

        except Exception as e:
            print(f"Error: {e}")
            results.append(
                {
                    "problem": problem,
                    "expected": expected_answer,
                    "got": "",
                    "correct": False,
                    "valid": False,
                    "error": str(e),
                }
            )

    # Summary
    print("\n=== Evaluation Summary ===")
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    valid = sum(1 for r in results if r["valid"])

    print(f"Total Problems: {total}")
    print(f"Valid Results: {valid}")
    print(f"Correct Answers: {correct}")
    print(f"Accuracy: {correct/total*100:.1f}%" if total > 0 else "N/A")

    return results


# Create BRAID module
braid = BraidReasoning(use_generator=True)

print("=== Running GSM8K Evaluation ===")
print("(Note: Requires configured DSPy language model)")

try:
    results = evaluate_gsm8k(braid, gsm8k_examples)
except Exception as e:
    print(f"Cannot run evaluation without LM: {e}")
    print("\nTo run this example:")
    print("1. Configure DSPy with a language model")
    print("2. Uncomment the evaluation call")
    print("3. Run the script")

# Example with optimization
print("\n=== Optimization Example ===")
print("(Shows how to use BraidOptimizer)")

optimizer = BraidOptimizer()

# Note: Actual optimization requires a configured base optimizer
# Example:
# from dspy.teleprompt import MIPROv2
# base_optimizer = MIPROv2()
# optimizer = BraidOptimizer(base_optimizer=base_optimizer)
# optimized_braid = optimizer.optimize(braid, trainset=gsm8k_examples)

print("BraidOptimizer created. Use optimizer.optimize() to optimize your module.")
