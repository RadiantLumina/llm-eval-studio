"""
ROUGE metric implementation for text evaluation
"""

from typing import Dict, List, Union
import re
from .base_metric import BaseMetric

try:
    from rouge_score import rouge_scorer
    ROUGE_AVAILABLE = True
except ImportError:
    ROUGE_AVAILABLE = False
    print("Warning: rouge-score not installed. Install with: pip install rouge-score")

class ROUGEMetric(BaseMetric):
    """
    ROUGE (Recall-Oriented Understudy for Gisting Evaluation) metric
    
    Supports ROUGE-1, ROUGE-2, and ROUGE-L
    """
    
    def __init__(self, variants: List[str] = None):
        """
        Initialize ROUGE metric
        
        Args:
            variants: List of ROUGE variants to compute
                     Options: ['rouge1', 'rouge2', 'rougeL']
                     Default: all variants
        """
        super().__init__(name="ROUGE", higher_is_better=True)
        
        if variants is None:
            variants = ['rouge1', 'rouge2', 'rougeL']
        self.variants = variants
        
        if ROUGE_AVAILABLE:
            self.scorer = rouge_scorer.RougeScorer(variants, use_stemmer=True)
        else:
            self.scorer = None
    
    def compute(
        self,
        references: Union[str, List[str]],
        predictions: Union[str, List[str]],
        **kwargs
    ) -> Dict[str, float]:
        """
        Compute ROUGE scores
        
        Args:
            references: Reference text(s)
            predictions: Predicted text(s)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with ROUGE scores (precision, recall, fmeasure)
        """
        if not ROUGE_AVAILABLE:
            raise ImportError(
                "rouge-score package is required to use ROUGEMetric. "
                "Install it with: pip install rouge-score"
            )
        
        # Handle single reference/prediction
        if isinstance(references, str):
            references = [references]
        if isinstance(predictions, str):
            predictions = [predictions]
        
        # Use first reference if multiple provided
        reference = references[0]
        prediction = predictions[0]
        
        # Compute ROUGE scores
        scores = self.scorer.score(reference, prediction)
        
        # Extract and format scores
        results = {}
        for variant in self.variants:
            if variant in scores:
                results[f"{variant}_precision"] = scores[variant].precision
                results[f"{variant}_recall"] = scores[variant].recall
                results[f"{variant}_fmeasure"] = scores[variant].fmeasure
        
        return results
    
    def compute_batch(
        self,
        references: List[str],
        predictions: List[str],
        **kwargs
    ) -> Dict[str, Union[float, List[Dict[str, float]]]]:
        """
        Compute ROUGE scores for a batch of examples
        
        Args:
            references: List of reference texts
            predictions: List of predicted texts
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with overall and per-example scores
        """
        if not ROUGE_AVAILABLE:
            raise ImportError(
                "rouge-score package is required to use ROUGEMetric. "
                "Install it with: pip install rouge-score"
            )
        
        if len(references) != len(predictions):
            raise ValueError(
                f"Number of references ({len(references)}) "
                f"must match number of predictions ({len(predictions)})"
            )
        
        # Compute per-example scores
        per_example_scores = []
        for ref, pred in zip(references, predictions):
            score = self.compute(ref, pred)
            per_example_scores.append(score)
        
        # Aggregate scores
        aggregated = self._aggregate_scores(per_example_scores)
        
        return {
            "overall": aggregated,
            "per_example": per_example_scores
        }
    
    def _aggregate_scores(self, scores: List[Dict[str, float]]) -> Dict[str, float]:
        """
        Aggregate per-example ROUGE scores
        
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
            aggregated[key] = sum(values) / len(values)
        
        return aggregated