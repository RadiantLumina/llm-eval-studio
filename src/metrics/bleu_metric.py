"""
BLEU metric implementation for text evaluation
"""

from typing import Dict, List, Union
import re
from .base_metric import BaseMetric

try:
    import sacrebleu
    SACREBLEU_AVAILABLE = True
except ImportError:
    SACREBLEU_AVAILABLE = False
    print("Warning: sacrebleu not installed. Install with: pip install sacrebleu")

class BLEUMetric(BaseMetric):
    """
    BLEU (Bilingual Evaluation Understudy) metric
    
    Computes BLEU score for evaluating text generation quality
    """
    
    def __init__(self, max_order: int = 4, smooth: bool = False):
        """
        Initialize BLEU metric
        
        Args:
            max_order: Maximum n-gram order to consider (default: 4)
            smooth: Whether to apply smoothing (default: False)
        """
        super().__init__(name="BLEU", higher_is_better=True)
        self.max_order = max_order
        self.smooth = smooth
    
    def compute(
        self,
        references: Union[str, List[str]],
        predictions: Union[str, List[str]],
        **kwargs
    ) -> Dict[str, float]:
        """
        Compute BLEU score
        
        Args:
            references: Reference text(s)
            predictions: Predicted text(s)
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with BLEU score
        """
        if not SACREBLEU_AVAILABLE:
            raise ImportError(
                "sacrebleu package is required to use BLEUMetric. "
                "Install it with: pip install sacrebleu"
            )
        
        # Handle single reference/prediction
        if isinstance(predictions, str):
            predictions = [predictions]
        
        if isinstance(references, str):
            references = [[references]]
        elif isinstance(references, list) and isinstance(references[0], str):
            references = [references]
        
        # Compute BLEU using sacrebleu
        # sacrebleu expects: hypotheses (list of strings), references (list of list of strings)
        bleu = sacrebleu.corpus_bleu(
            predictions,
            references,
            smooth_method='exp' if self.smooth else 'none'
        )
        
        return {
            "bleu": bleu.score / 100.0,  # Normalize to 0-1 range
            "bleu_raw": bleu.score,
            "precisions": bleu.precisions,
            "bp": bleu.bp,
            "ratio": bleu.ratio,
            "sys_len": bleu.sys_len,
            "ref_len": bleu.ref_len
        }
    
    def compute_batch(
        self,
        references: List[str],
        predictions: List[str],
        **kwargs
    ) -> Dict[str, Union[float, List[Dict[str, float]]]]:
        """
        Compute BLEU scores for a batch of examples
        
        Args:
            references: List of reference texts
            predictions: List of predicted texts
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with overall and per-example scores
        """
        if not SACREBLEU_AVAILABLE:
            raise ImportError(
                "sacrebleu package is required to use BLEUMetric. "
                "Install it with: pip install sacrebleu"
            )
        
        if len(references) != len(predictions):
            raise ValueError(
                f"Number of references ({len(references)}) "
                f"must match number of predictions ({len(predictions)})"
            )
        
        # Compute per-example BLEU scores
        per_example_scores = []
        for ref, pred in zip(references, predictions):
            # For per-example, we use sentence-level BLEU
            bleu = sacrebleu.sentence_bleu(pred, [ref])
            per_example_scores.append({
                "bleu": bleu.score / 100.0,
                "bleu_raw": bleu.score
            })
        
        # Compute overall corpus-level BLEU
        # Prepare references in sacrebleu format: list of list of strings
        refs_for_corpus = [[ref] for ref in references]
        corpus_bleu = sacrebleu.corpus_bleu(predictions, refs_for_corpus)
        
        overall = {
            "bleu": corpus_bleu.score / 100.0,
            "bleu_raw": corpus_bleu.score
        }
        
        return {
            "overall": overall,
            "per_example": per_example_scores
        }