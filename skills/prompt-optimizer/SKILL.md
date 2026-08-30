---
name: prompt-optimizer
description: LLM Prompt 架构设计：系统提示、上下文管理、输出格式、评估迭代
source:
  type: derived
  repo: skills-repo/productivity-master
  path: skills/prompt-optimizer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/davila7/claude-code-templates/prompt-engineer
metadata:
  category: Prompt 工程
  platform: 通用
  difficulty: 进阶
---

# Prompt 工程优化

> Prompt 是编程——需要代码一样的严谨。小改动有大影响，凭直觉判断 Prompt 质量往往是错的。

## 能力

- **系统提示架构**：角色定义、能力边界、行为约束分层设计
- **上下文管理**：Token 预算分配、关键信息优先级、压缩策略
- **输出格式控制**：结构化输出规范、Schema 约束、错误处理
- **Few-shot 设计**：示例选择原则、正负例平衡、格式一致性
- **评估迭代**：A/B 测试方法、评估指标设计、回归测试

## 使用方式

```
/prompt-optimizer 优化这个系统提示，让它更精准
/prompt-optimizer 为这个任务设计一个 few-shot prompt
/prompt-optimizer 这个 prompt 输出不稳定，帮我分析原因
```

## 工作流

1. 明确任务目标和输出规格
2. 设计系统提示：角色 → 能力 → 约束 → 输出格式
3. 添加 few-shot 示例（2-3 个覆盖关键场景）
4. 测试边界情况，记录失败模式
5. 迭代优化：每次只改一个变量，对比效果

## 适用场景

- Claude Code 自定义指令优化
- AI Agent 系统提示设计
- Few-shot prompt 工程
- 输出格式不稳定时的排查

## 限制

- 不涉及模型训练和微调
- 不涉及 RAG 检索策略
- 不同模型对同一 prompt 反应不同，需实际测试

## 相关参考（Playbook）

可复现的 Prompt 评估协议（评估集设计、Token 预算、few-shot 选择、迭代记录表）见 `references/prompt-evaluation-protocol.md`。