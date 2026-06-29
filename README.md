# LLM Evaluation Studio 🎯

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

一个大语言模型（LLM）评测框架，支持多维度指标评估、Prompt 模板管理和可视化分析。

## ✨ 特性

- **多维度评测指标**：ROUGE、BLEU、BERTScore、准确性、连贯性、指令遵循度等
- **Prompt 模板管理**：结构化 Prompt 设计，支持 Few-shot 示例
- **批量评测框架**：支持大规模数据集的自动化评测
- **可视化分析**：评测结果可视化，支持生成可视化看板
- **多模型支持**：兼容 OpenAI、Claude、本地模型等多种 LLM API
- **中英文双语**：支持中英文混合评测场景

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/RadiantLumina/llm-eval-studio.git
cd llm-eval-studio
pip install -r requirements.txt
```

### 基础使用示例

```python
from llm_eval_studio.metrics import ROUGEMetric, BLEUMetric
from llm_eval_studio.evaluators import LLMEvaluator

# 初始化评测器
evaluator = LLMEvaluator(
    metrics=[ROUGEMetric(), BLEUMetric()],
    model="gpt-3.5-turbo"
)

# 运行评测
results = evaluator.evaluate(
    references=["这是一个测试参考文本"],
    predictions=["这是一个测试预测文本"]
)

print(results)
```

## 📊 核心功能

### 1. 多维度评测指标

| 指标类型 | 指标名称 | 说明 |
|---------|---------|------|
| 自动指标 | ROUGE-1/2/L | 基于 n-gram 的重叠度评测 |
| 自动指标 | BLEU | 机器翻译质量评测 |
| 自动指标 | BERTScore | 基于语义相似度的评测 |
| 人工指标 | 准确性 | 输出内容的准确程度 |
| 人工指标 | 连贯性 | 文本流畅度和逻辑性 |
| 人工指标 | 指令遵循度 | 对 Prompt 指令的遵循程度 |

### 2. Prompt 模板管理

```python
from llm_eval_studio.prompt_templates import PromptTemplate

# 创建结构化 Prompt 模板
template = PromptTemplate(
    task_type="qa",
    system_prompt="你是一个专业的问答助手。",
    few_shot_examples=[
        {"input": "什么是机器学习？", "output": "机器学习是..."},
        {"input": "什么是深度学习？", "output": "深度学习是..."}
    ]
)

# 生成 Prompt
prompt = template.generate_prompt(user_input="什么是强化学习？")
```

### 3. 批量评测

```python
from llm_eval_studio.evaluators import BatchEvaluator

# 批量评测
evaluator = BatchEvaluator(
    metrics=[ROUGEMetric(), BLEUMetric()],
    model="gpt-3.5-turbo",
    batch_size=32
)

results = evaluator.evaluate_dataset(
    dataset_path="data/test_dataset.json",
    output_path="results/evaluation_results.json"
)
```

### 4. 可视化分析

```python
from llm_eval_studio.visualization import EvaluationDashboard

# 生成评测结果可视化看板
dashboard = EvaluationDashboard(results)
dashboard.generate_report(output_path="results/report.html")
```

## 📁 项目结构

```
llm-eval-studio/
├── src/                      # 源代码
│   ├── metrics/             # 评测指标实现
│   ├── evaluators/          # 评测器实现
│   ├── prompt_templates/    # Prompt 模板管理
│   ├── visualization/       # 可视化模块
│   └── utils/              # 工具函数
├── examples/                # 使用示例
├── tests/                   # 单元测试
├── docs/                    # 文档
├── data/                    # 示例数据集
└── results/                 # 评测结果输出
```

## 🔧 技术栈

- **核心框架**：Python 3.8+
- **NLP 工具**：transformers, torch, jieba (中文分词)
- **评测指标**：rouge-score, sacrebleu, bert-score
- **可视化**：matplotlib, seaborn, plotly
- **数据处理**：pandas, numpy
- **API 支持**：openai, anthropic, requests

## 📈 应用场景

1. **LLM 模型选型**：对比不同模型在相同任务上的表现
2. **Prompt 工程优化**：评测不同 Prompt 设计的效果
3. **模型微调评估**：量化模型微调前后的性能提升
4. **业务效果监控**：监控线上 LLM 应用的质量指标

## 🤝 贡献指南

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

## 📝 许可证

[MIT License](LICENSE)

## 🙏 致谢

- ROUGE 指标实现参考：[rouge-score](https://github.com/google-research/google-research/tree/master/rouge)
- BLEU 指标实现参考：[sacrebleu](https://github.com/mjpost/sacrebleu)
- BERTScore 实现参考：[bert-score](https://github.com/Tiiiger/bert_score)

## 📧 联系方式

- 作者： RadiantLumina
- GitHub：[@RadiantLumina](https://github.com/RadiantLumina)

---

⭐ 如果这个项目对你有帮助，请给它一个 Star！
