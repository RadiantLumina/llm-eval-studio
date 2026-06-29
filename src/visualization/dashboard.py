"""
Visualization module for LLM Evaluation Studio
"""

from typing import Any, Dict, List, Optional
import json
from pathlib import Path

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    import numpy as np
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: Visualization libraries not installed.")
    print("Install with: pip install matplotlib seaborn pandas numpy")

class EvaluationDashboard:
    """
    Dashboard for visualizing evaluation results
    """
    
    def __init__(
        self,
        results: Optional[Dict] = None,
        style: str = "whitegrid",
        palette: str = "viridis"
    ):
        """
        Initialize dashboard
        
        Args:
            results: Evaluation results to visualize
            style: Seaborn style theme
            palette: Color palette
        """
        self.results = results
        self.style = style
        self.palette = palette
        
        if VISUALIZATION_AVAILABLE:
            sns.set_style(style)
            plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
    
    def set_results(self, results: Dict):
        """Set evaluation results"""
        self.results = results
    
    def plot_metric_comparison(
        self,
        metrics: List[str] = None,
        figsize: tuple = (10, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot comparison of different metrics
        
        Args:
            metrics: List of metric names to plot (if None, plot all)
            figsize: Figure size
            save_path: Path to save the plot
        """
        if not VISUALIZATION_AVAILABLE:
            raise ImportError("Visualization libraries required")
        
        if self.results is None:
            raise ValueError("No results to visualize")
        
        # Extract metric scores
        scores = self._extract_scores(metrics)
        
        # Create plot
        fig, ax = plt.subplots(figsize=figsize)
        
        metrics_names = list(scores.keys())
        scores_values = list(scores.values())
        
        bars = ax.bar(metrics_names, scores_values, color=sns.color_palette(self.palette, len(metrics_names)))
        
        # Add value labels on bars
        for bar, score in zip(bars, scores_values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{score:.3f}',
                   ha='center', va='bottom')
        
        ax.set_xlabel('Metrics', fontsize=12)
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title('Evaluation Metrics Comparison', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 1.1)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_per_example_scores(
        self,
        metric_name: str,
        figsize: tuple = (12, 6),
        save_path: Optional[str] = None
    ):
        """
        Plot per-example scores for a metric
        
        Args:
            metric_name: Name of the metric to plot
            figsize: Figure size
            save_path: Path to save the plot
        """
        if not VISUALIZATION_AVAILABLE:
            raise ImportError("Visualization libraries required")
        
        if self.results is None:
            raise ValueError("No results to visualize")
        
        # Extract per-example scores
        per_example = self._extract_per_example_scores(metric_name)
        
        if not per_example:
            raise ValueError(f"No per-example scores found for metric '{metric_name}'")
        
        # Create plot
        fig, axes = plt.subplots(1, 2, figsize=figsize)
        
        # Box plot
        axes[0].boxplot(per_example)
        axes[0].set_xlabel(metric_name)
        axes[0].set_ylabel('Score')
        axes[0].set_title(f'{metric_name} Distribution')
        
        # Histogram
        axes[1].hist(per_example, bins=20, edgecolor='black', alpha=0.7)
        axes[1].set_xlabel('Score')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'{metric_name} Histogram')
        axes[1].axvline(np.mean(per_example), color='red', linestyle='--', label=f'Mean: {np.mean(per_example):.3f}')
        axes[1].legend()
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def generate_report(
        self,
        output_path: str,
        format: str = "html"
    ):
        """
        Generate evaluation report
        
        Args:
            output_path: Path to save the report
            format: Report format ('html', 'json', 'txt')
        """
        if self.results is None:
            raise ValueError("No results to generate report")
        
        if format == "html":
            self._generate_html_report(output_path)
        elif format == "json":
            self._generate_json_report(output_path)
        elif format == "txt":
            self._generate_text_report(output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _extract_scores(self, metrics: Optional[List[str]]) -> Dict[str, float]:
        """Extract overall scores from results"""
        scores = {}
        
        if "overall" in self.results:
            overall = self.results["overall"]
            if metrics is None:
                metrics = list(overall.keys())
            
            for metric in metrics:
                if metric in overall:
                    scores[metric] = overall[metric]
        
        return scores
    
    def _extract_per_example_scores(self, metric_name: str) -> List[float]:
        """Extract per-example scores for a metric"""
        scores = []
        
        if "per_example" in self.results:
            for example in self.results["per_example"]:
                if "metrics_results" in example:
                    for metric, result in example["metrics_results"].items():
                        if metric_name.lower() in metric.lower():
                            if isinstance(result, dict):
                                # Get first numeric value
                                for key, value in result.items():
                                    if isinstance(value, (int, float)):
                                        scores.append(value)
                                        break
                            elif isinstance(result, (int, float)):
                                scores.append(result)
        
        return scores
    
    def _generate_html_report(self, output_path: str):
        """Generate HTML report"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>LLM Evaluation Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #4CAF50; color: white; }
                tr:nth-child(even) { background-color: #f2f2f2; }
            </style>
        </head>
        <body>
            <h1>LLM Evaluation Report</h1>
        """
        
        # Add results
        html_content += f"<p><strong>Number of examples:</strong> {self.results.get('num_examples', 'N/A')}</p>"
        
        if "overall" in self.results:
            html_content += "<h2>Overall Results</h2><table><tr><th>Metric</th><th>Score</th></tr>"
            for metric, score in self.results["overall"].items():
                html_content += f"<tr><td>{metric}</td><td>{score:.4f}</td></tr>"
            html_content += "</table>"
        
        html_content += """
        </body>
        </html>
        """
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML report saved to {output_path}")
    
    def _generate_json_report(self, output_path: str):
        """Generate JSON report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"JSON report saved to {output_path}")
    
    def _generate_text_report(self, output_path: str):
        """Generate text report"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("LLM Evaluation Report\n")
            f.write("=" * 60 + "\n\n")
            
            f.write(f"Number of examples: {self.results.get('num_examples', 'N/A')}\n\n")
            
            if "overall" in self.results:
                f.write("Overall Results:\n")
                f.write("-" * 40 + "\n")
                for metric, score in self.results["overall"].items():
                    f.write(f"  {metric}: {score:.4f}\n")
                f.write("\n")
        
        print(f"Text report saved to {output_path}")