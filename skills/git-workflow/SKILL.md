---
name: git-workflow
description: Git 分支策略、提交规范、rebase/squash 最佳实践，面向个人和小团队的 Git 工作流
source:
  type: original
  repo: skills-repo/productivity-master
  path: skills/git-workflow/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
metadata:
  category: Git
  platform: 通用
  difficulty: 入门
---

# Git 工作流专家

> 为个人和小团队制定高效的 Git 工作流：分支策略选择、提交信息规范、rebase/squash 操作、冲突解决。

## 能力

- **分支策略推荐**：根据项目规模和发布节奏推荐合适的分支模型（Trunk-based / GitFlow-lite / GitHub Flow）
- **提交信息生成**：Conventional Commits 格式自动生成，含 scope 建议
- **Rebase/Squash 指导**：交互式 rebase 操作、Squash 合并策略、历史清理
- **冲突解决**：分析冲突类型（逻辑/格式/结构），提供分步骤解决方案
- **Git Hooks**：pre-commit、commit-msg、pre-push hooks 配置

## 使用方式

```
/git-workflow 分析当前仓库的提交历史，给优化建议
/git-workflow 帮我 squash 最近 5 个 commit 为一个
/git-workflow 推荐适合 3 人小团队的分支策略
```

## 工作流

1. 分析当前仓库状态（分支结构、提交历史、团队规模）
2. 推荐匹配的分支策略和工作流
3. 生成 Conventional Commits 格式的提交信息
4. 指导 rebase/squash 操作步骤
5. 验证操作结果

## 分支策略快速选择

| 团队规模 | 发布频率 | 推荐策略 |
|---------|---------|---------|
| 1-3 人 | 每日 | Trunk-based（main 直推） |
| 2-5 人 | 每周 | GitHub Flow（feature branch） |
| 5-10 人 | 双周/月 | GitFlow-lite（main + develop） |
| 10+ | 定期 | 完整 GitFlow |

## 适用场景

- 新项目初始化时的 Git 工作流设定
- 提交历史混乱需要清理
- 团队协作中出现频繁冲突需要优化策略
- 准备开源项目的 CONTRIBUTING.md

## 限制

- 不涉及 Git 服务器管理（GitHub/GitLab 运维）
- 复杂 Monorepo 策略不在范围内
- 推荐策略需结合项目实际调整
