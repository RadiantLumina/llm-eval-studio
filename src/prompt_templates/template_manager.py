"""
Prompt Template Manager for structured prompt engineering
"""

from typing import Any, Dict, List, Optional
import json
import yaml
from pathlib import Path

class PromptTemplate:
    """
    Structured prompt template for LLM tasks
    
    Supports system prompts, few-shot examples, and dynamic user input
    """
    
    def __init__(
        self,
        task_type: str,
        system_prompt: str = "",
        few_shot_examples: List[Dict[str, str]] = None,
        template_format: str = "text",
        **kwargs
    ):
        """
        Initialize prompt template
        
        Args:
            task_type: Type of task (qa, summarization, code_generation, etc.)
            system_prompt: System-level instruction for the LLM
            few_shot_examples: List of example dicts with 'input' and 'output' keys
            template_format: Format type ('text', 'chat', 'instruction')
            **kwargs: Additional template parameters
        """
        self.task_type = task_type
        self.system_prompt = system_prompt
        self.few_shot_examples = few_shot_examples or []
        self.template_format = template_format
        self.kwargs = kwargs
        
    def generate_prompt(self, user_input: str, **kwargs) -> str:
        """
        Generate complete prompt from template
        
        Args:
            user_input: User's input/query
            **kwargs: Additional variables for template formatting
            
        Returns:
            Complete formatted prompt string
        """
        if self.template_format == "text":
            return self._generate_text_prompt(user_input)
        elif self.template_format == "chat":
            return self._generate_chat_prompt(user_input)
        elif self.template_format == "instruction":
            return self._generate_instruction_prompt(user_input)
        else:
            raise ValueError(f"Unsupported template format: {self.template_format}")
    
    def _generate_text_prompt(self, user_input: str) -> str:
        """Generate text-format prompt"""
        prompt_parts = []
        
        # Add system prompt
        if self.system_prompt:
            prompt_parts.append(f"### Instruction:\n{self.system_prompt}\n")
        
        # Add few-shot examples
        if self.few_shot_examples:
            prompt_parts.append("### Examples:")
            for i, example in enumerate(self.few_shot_examples, 1):
                prompt_parts.append(f"\nExample {i}:")
                prompt_parts.append(f"Input: {example.get('input', '')}")
                prompt_parts.append(f"Output: {example.get('output', '')}")
            prompt_parts.append("")  # Empty line
        
        # Add user input
        prompt_parts.append(f"### Input:\n{user_input}\n")
        prompt_parts.append("### Output:")
        
        return "\n".join(prompt_parts)
    
    def _generate_chat_prompt(self, user_input: str) -> List[Dict[str, str]]:
        """
        Generate chat-format prompt (for chat models)
        
        Returns:
            List of message dicts (role, content)
        """
        messages = []
        
        # System message
        if self.system_prompt:
            messages.append({
                "role": "system",
                "content": self.system_prompt
            })
        
        # Few-shot examples as conversation
        for example in self.few_shot_examples:
            messages.append({
                "role": "user",
                "content": example.get('input', '')
            })
            messages.append({
                "role": "assistant",
                "content": example.get('output', '')
            })
        
        # User input
        messages.append({
            "role": "user",
            "content": user_input
        })
        
        return messages
    
    def _generate_instruction_prompt(self, user_input: str) -> str:
        """Generate instruction-format prompt"""
        prompt_parts = []
        
        if self.system_prompt:
            prompt_parts.append(f"### Instruction:\n{self.system_prompt}\n")
        
        if self.few_shot_examples:
            prompt_parts.append("### Examples:")
            for example in self.few_shot_examples:
                prompt_parts.append(f"### Input:\n{example.get('input', '')}")
                prompt_parts.append(f"### Output:\n{example.get('output', '')}\n")
        
        prompt_parts.append(f"### Input:\n{user_input}")
        prompt_parts.append("### Output:")
        
        return "\n".join(prompt_parts)
    
    def to_dict(self) -> Dict:
        """Convert template to dictionary"""
        return {
            "task_type": self.task_type,
            "system_prompt": self.system_prompt,
            "few_shot_examples": self.few_shot_examples,
            "template_format": self.template_format,
            **self.kwargs
        }
    
    def to_json(self, filepath: str):
        """Save template to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def to_yaml(self, filepath: str):
        """Save template to YAML file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(self.to_dict(), f, allow_unicode=True, default_flow_style=False)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PromptTemplate':
        """Create template from dictionary"""
        return cls(**data)
    
    @classmethod
    def from_json(cls, filepath: str) -> 'PromptTemplate':
        """Load template from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
    
    @classmethod
    def from_yaml(cls, filepath: str) -> 'PromptTemplate':
        """Load template from YAML file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return cls.from_dict(data)
    
    def __repr__(self):
        return f"PromptTemplate(task_type='{self.task_type}', format='{self.template_format}')"


class PromptTemplateManager:
    """
    Manager for organizing and retrieving prompt templates
    """
    
    def __init__(self, template_dir: str = None):
        """
        Initialize template manager
        
        Args:
            template_dir: Directory to store templates
        """
        self.template_dir = Path(template_dir) if template_dir else Path("templates")
        self.template_dir.mkdir(exist_ok=True)
        self.templates = {}
        
    def add_template(self, name: str, template: PromptTemplate):
        """Add a template to the manager"""
        self.templates[name] = template
        
    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """Retrieve a template by name"""
        return self.templates.get(name)
    
    def list_templates(self) -> List[str]:
        """List all template names"""
        return list(self.templates.keys())
    
    def save_template(self, name: str, template: PromptTemplate = None):
        """
        Save template to file
        
        Args:
            name: Template name
            template: Template to save (if None, uses stored template)
        """
        if template is None:
            template = self.templates.get(name)
            if template is None:
                raise ValueError(f"Template '{name}' not found")
        
        filepath = self.template_dir / f"{name}.json"
        template.to_json(str(filepath))
        
    def load_template(self, name: str) -> PromptTemplate:
        """
        Load template from file
        
        Args:
            name: Template name
            
        Returns:
            Loaded PromptTemplate
        """
        # Try JSON first, then YAML
        json_path = self.template_dir / f"{name}.json"
        yaml_path = self.template_dir / f"{name}.yaml"
        
        if json_path.exists():
            template = PromptTemplate.from_json(str(json_path))
        elif yaml_path.exists():
            template = PromptTemplate.from_yaml(str(yaml_path))
        else:
            raise FileNotFoundError(f"Template '{name}' not found in {self.template_dir}")
        
        self.templates[name] = template
        return template
    
    def create_default_templates(self):
        """Create a set of default prompt templates"""
        
        # QA Template
        qa_template = PromptTemplate(
            task_type="qa",
            system_prompt="你是一个专业的问答助手。请根据问题给出准确、简洁的答案。",
            few_shot_examples=[
                {"input": "什么是机器学习？", "output": "机器学习是人工智能的一个分支，通过算法让计算机从数据中学习并改进。"},
                {"input": "什么是深度学习？", "output": "深度学习是基于人工神经网络的机器学习方法，特别擅长处理复杂模式识别任务。"}
            ],
            template_format="text"
        )
        self.add_template("qa_basic", qa_template)
        
        # Summarization Template
        summary_template = PromptTemplate(
            task_type="summarization",
            system_prompt="请将以下文本总结为简洁的要点。",
            few_shot_examples=[
                {"input": "今天天气很好，阳光明媚，适合出去散步。", "output": "天气晴朗，适合户外活动。"},
                {"input": "这个项目需要完成数据收集、清洗、分析和可视化四个步骤。", "output": "项目流程：数据收集→清洗→分析→可视化。"}
            ],
            template_format="text"
        )
        self.add_template("summary_basic", summary_template)
        
        # Save default templates
        for name in self.list_templates():
            self.save_template(name)