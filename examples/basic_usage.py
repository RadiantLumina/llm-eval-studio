"""
Basic usage example for LLM Evaluation Studio
"""

from src.metrics.rouge_metric import ROUGEMetric
from src.metrics.bleu_metric import BLEUMetric
from src.evaluators.llm_evaluator import LLMEvaluator

def main():
    """Main function demonstrating basic usage"""
    
    print("=" * 60)
    print("LLM Evaluation Studio - Basic Usage Example")
    print("=" * 60 + "\n")
    
    # Initialize metrics
    print("1. Initializing metrics...")
    rouge_metric = ROUGEMetric(variants=['rouge1', 'rouge2', 'rougeL'])
    bleu_metric = BLEUMetric(max_order=4, smooth=False)
    
    # Initialize evaluator
    print("2. Creating evaluator...")
    evaluator = LLMEvaluator(
        metrics=[rouge_metric, bleu_metric],
        model="example_model"
    )
    
    # Example data
    print("3. Preparing example data...")
    references = [
        "机器学习是人工智能的一个重要分支。",
        "深度学习在图像识别领域取得了巨大成功。"
    ]
    
    predictions = [
        "机器学习是人工智能的一个主要分支。",
        "深度学习在图像识别方面取得了显著成果。"
    ]
    
    # Run evaluation
    print("4. Running evaluation...\n")
    results = evaluator.evaluate_batch(references, predictions)
    
    # Display results
    print("5. Evaluation Results:")
    print("-" * 40)
    
    if "overall" in results:
        print("\nOverall Scores:")
        for metric, score in results["overall"].items():
            print(f"  {metric}: {score:.4f}")
    
    if "per_example" in results:
        print(f"\nPer-Example Scores (showing first 2):")
        for i, example in enumerate(results["per_example"][:2]):
            print(f"\n  Example {i+1}:")
            if "metrics_results" in example:
                for metric_name, metric_result in example["metrics_results"].items():
                    print(f"    {metric_name}: {metric_result}")
    
    print("\n" + "=" * 60)
    print("Evaluation completed successfully!")
    print("=" * 60)
    
    # Save results
    print("\n6. Saving results...")
    evaluator.save_results("results/basic_usage_results.json", results)
    print("   Results saved to: results/basic_usage_results.json")

if __name__ == "__main__":
    main()