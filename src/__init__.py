"""
LLM Evaluation Studio
A professional LLM evaluation framework
"""

__version__ = "0.1.0"
__author__ = "RadiantLumina"

from .metrics.base_metric import BaseMetric
from .evaluators.base_evaluator import BaseEvaluator

__all__ = ["BaseMetric", "BaseEvaluator", "__version__"]
