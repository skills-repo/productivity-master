---
name: git-workflow
description: Git 工作流：Trunk-Based 开发、原子提交、语义化版本、Changelog
source:
  type: derived
  repo: skills-repo/productivity-master
  path: skills/git-workflow/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/addyosmani/agent-skills/git-workflow-and-versioning
metadata:
  category: 版本控制
  platform: 通用
  difficulty: 入门
---

# Git 工作流与版本管理

> Git 是安全网——提交是存档点，分支是沙盒，历史是文档。面向 AI 辅助开发时代的版本控制规范。

## 能力

- **Trunk-Based 开发**：main 始终可部署，短周期功能分支（1-3 天）
- **原子提交**：每个提交做一件事，可独立回滚
- **提交信息规范**：Conventional Commits 格式（feat/fix/refactor/docs）
- **分支策略**：功能分支 → PR → squash/rebase → main
- **语义化版本**：major.minor.patch 的选择规则
- **Changelog 生成**：从提交历史生成结构化变更日志

## 使用方式

```
/git-workflow 帮我规划这个功能的分支和提交策略
/git-workflow 为这次的变更生成合适的提交信息
/git-workflow 这次该升 major、minor 还是 patch？
```

## 工作流

1. 从 main 拉取最新，创建功能分支
2. 实现切片 → 测试 → 验证 → 原子提交 → 下一片
3. 每个提交信息包含：类型 + 范围 + 描述
4. 功能完成后 push → PR → review → squash merge
5. 发布时打 tag，生成 Changelog

## 适用场景

- 个人项目版本管理
- 小团队协作 Git 规范
- 发布和版本号管理
- AI Agent 辅助编码时的提交策略

## 限制

- 不涉及大型团队的 GitFlow 模式
- 不涉及 monorepo 管理（lerna/nx）
- 不涉及 CI/CD 流水线配置

## 相关参考（Playbook）

提交/分支/PR 质量门禁的决策树、版本号矩阵与审查分级口径见 [references/commit-and-pr-quality-gates.md](../../references/commit-and-pr-quality-gates.md)。