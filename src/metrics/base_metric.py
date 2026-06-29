"""
Base metric class for all evaluation metrics
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union
import numpy as np

class BaseMetric(ABC):
    """
    Abstract base class for all evaluation metrics
    
    All custom metrics should inherit from this class and implement
    the compute method.
    """
    
    def __init__(self, name: str, higher_is_better: bool = True):
        """
        Initialize the metric
        
        Args:
            name: Name of the metric
            higher_is_better: Whether higher scores indicate better performance
        """
        self.name = name
        self.higher_is_better = higher_is_better
        
    @abstractmethod
    def compute(
        self,
        references: Union[str, List[str]],
        predictions: Union[str, List[str]],
        **kwargs
    ) -> Dict[str, float]:
        """
        Compute the metric score
        
        Args:
            references: Reference text(s) (ground truth)
            predictions: Predicted text(s) (model output)
            **kwargs: Additional arguments specific to the metric
            
        Returns:
            Dictionary containing metric scores
        """
        pass
    
    def compute_batch(
        self,
        references: List[str],
        predictions: List[str],
        **kwargs
    ) -> Dict[str, Union[float, List[float]]]:
        """
        Compute metric for a batch of examples
        
        Args:
            references: List of reference texts
            predictions: List of predicted texts
            **kwargs: Additional arguments
            
        Returns:
            Dictionary containing overall and per-example scores
        """
        if len(references) != len(predictions):
            raise ValueError(
                f"Number of references ({len(references)}) "
                f"must match number of predictions ({len(predictions)})"
            )
        
        # Compute per-example scores
        per_example_scores = []
        for ref, pred in zip(references, predictions):
            score = self.compute(ref, pred, **kwargs)
            per_example_scores.append(score)
        
        # Aggregate scores
        aggregated = self._aggregate_scores(per_example_scores)
        
        return {
            "overall": aggregated,
            "per_example": per_example_scores
        }
    
    def _aggregate_scores(self, scores: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Aggregate per-example scores to get overall scores
        
        Args:
            scores: List of per-example score dictionaries
            
        Returns:
            Dictionary of aggregated scores
        """
        if not scores:
            return {}
        
        # Get all keys from the first score dictionary
        keys = scores[0].keys()
        aggregated = {}
        
        for key in keys:
            values = [score[key] for score in scores if key in score]
            aggregated[key] = float(np.mean(values))
        
        return aggregated
    
    def __call__(
        self,
        references: Union[str, List[str]],
        predictions: Union[str, List[str]],
        **kwargs
    ) -> Dict[str, float]:
        """
        Convenience method to compute metric scores
        
        Args:
            references: Reference text(s)
            predictions: Predicted text(s)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary containing metric scores
        """
        if isinstance(references, list) and isinstance(predictions, list):
            return self.compute_batch(references, predictions, **kwargs)
        else:
            return self.compute(references, predictions, **kwargs)
    
    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}')"