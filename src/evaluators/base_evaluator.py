"""
Base evaluator class for LLM evaluation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
from ..metrics.base_metric import BaseMetric

class BaseEvaluator(ABC):
    """
    Abstract base class for all evaluators
    
    Evaluators coordinate the evaluation process using multiple metrics
    """
    
    def __init__(
        self,
        metrics: List[BaseMetric],
        **kwargs
    ):
        """
        Initialize the evaluator
        
        Args:
            metrics: List of metrics to use for evaluation
            **kwargs: Additional arguments
        """
        self.metrics = metrics
        self.results = []
    
    @abstractmethod
    def evaluate(
        self,
        references: Union[str, List[str]],
        predictions: Union[str, List[str]],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate predictions against references
        
        Args:
            references: Reference text(s) (ground truth)
            predictions: Predicted text(s) (model output)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary containing evaluation results
        """
        pass
    
    def evaluate_batch(
        self,
        references: List[str],
        predictions: List[str],
        **kwargs
    ) -> Dict[str, Any]:
        """
        Evaluate a batch of predictions
        
        Args:
            references: List of reference texts
            predictions: List of predicted texts
            **kwargs: Additional arguments
            
        Returns:
            Dictionary containing batch evaluation results
        """
        if len(references) != len(predictions):
            raise ValueError(
                f"Number of references ({len(references)}) "
                f"must match number of predictions ({len(predictions)})"
            )
        
        # Evaluate each example
        all_results = []
        for i, (ref, pred) in enumerate(zip(references, predictions)):
            result = self.evaluate(ref, pred, **kwargs)
            result["example_id"] = i
            all_results.append(result)
        
        # Aggregate results
        aggregated = self._aggregate_results(all_results)
        
        return {
            "overall": aggregated,
            "per_example": all_results,
            "num_examples": len(references)
        }
    
    def _aggregate_results(self, results: List[Dict]) -> Dict:
        """
        Aggregate per-example results
        
        Args:
            results: List of per-example result dictionaries
            
        Returns:
            Dictionary of aggregated results
        """
        if not results:
            return {}
        
        aggregated = {}
        
        # Get all keys from the first result
        for key in results[0].keys():
            if key == "example_id":
                continue
            
            # Try to aggregate numeric values
            try:
                values = [r[key] for r in results if key in r]
                if all(isinstance(v, (int, float)) for v in values):
                    aggregated[f"{key}_mean"] = sum(values) / len(values)
                    aggregated[f"{key}_min"] = min(values)
                    aggregated[f"{key}_max"] = max(values)
            except:
                # Skip non-numeric values
                pass
        
        return aggregated
    
    def __repr__(self):
        metric_names = [m.name for m in self.metrics]
        return f"{self.__class__.__name__}(metrics={metric_names})"