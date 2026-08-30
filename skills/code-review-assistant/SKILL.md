---
name: code-review-assistant
description: 多维度代码审查：正确性、可读性、架构、安全、性能，合并前必检
source:
  type: derived
  repo: skills-repo/productivity-master
  path: skills/code-review-assistant/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/addyosmani/agent-skills/code-review-and-quality
metadata:
  category: 代码质量
  platform: 通用
  difficulty: 入门
---

# 代码审查与质量

> 多维度代码审查，五个维度全面评估：正确性、可读性、架构、安全、性能。合并前必检。

## 能力

- **正确性**：匹配需求规格、边界值处理、错误路径覆盖、测试质量
- **可读性**：命名一致性、控制流清晰度、死代码检测、抽象是否物有所值
- **架构**：遵循已有模式、单一职责、模块边界清晰
- **安全**：输入验证、注入风险、敏感数据暴露
- **性能**：不必要的循环、N+1 查询、内存泄漏风险

## 使用方式

```
/code-review-assistant 审查这个 PR
/code-review-assistant 检查我刚才写的这段代码
```

## 工作流

1. 确认审查范围和变更意图
2. 按五轴逐项审查：正确性 → 可读性 → 架构 → 安全 → 性能
3. 按严重程度分级问题：阻断/严重/建议
4. 输出审查报告，给出具体修复建议
5. 批准标准：变更整体改善代码健康度即可，不追求完美

## 适用场景

- PR 合并前审查
- 功能实现完成后的自查
- AI 生成代码的质量评估
- 重构后的代码审查

## 限制

- 不替代自动化 lint/测试工具
- 不涉及业务逻辑正确性验证（需领域知识）
- 审查速度受代码量影响，大 PR 建议分批

## 相关参考（Playbook）

提交/分支/PR 质量门禁里 PR 审查「该拦什么 / 该放什么」的分级口径与放行标准见 `references/commit-and-pr-quality-gates.md`。