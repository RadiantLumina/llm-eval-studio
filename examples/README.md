# LLM Evaluation Studio - 使用示例

This directory contains example scripts and notebooks demonstrating how to use the LLM Evaluation Studio.

## Files

- `basic_usage.py` - Basic usage example
- `batch_evaluation.py` - Batch evaluation example
- `prompt_engineering.py` - Prompt template usage example
- `visualization_demo.py` - Visualization examples

## Quick Start

```python
from llm_eval_studio.metrics import ROUGEMetric, BLEUMetric
from llm_eval_studio.evaluators import LLMEvaluator

# Initialize evaluator
evaluator = LLMEvaluator(
    metrics=[ROUGEMetric(), BLEUMetric()],
    model="gpt-3.5-turbo"
)

# Run evaluation
results = evaluator.evaluate(
    references=["这是一个测试参考文本"],
    predictions=["这是一个测试预测文本"]
)

print(results)
```

## Running Examples

```bash
# Run basic usage example
python examples/basic_usage.py

# Run batch evaluation
python examples/batch_evaluation.py

# Generate visualizations
python examples/visualization_demo.py
```