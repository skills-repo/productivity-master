# AGENTS.md — 开发者生产力技能库

> 本仓库为 **skills-repo/productivity-master**，面向个人和小团队开发者，提供效率工具和工作流优化技能。采用 superpower 架构。

## 目录约定（superpower）

| 层 | 目录 | 职责 | Agent 何时读 |
|----|------|------|--------------|
| L1 | `SKILL.md` | 路由层，能力索引 | 始终先读 |
| L2 | `references/` | 深层 playbook（决策树/矩阵/坑/清单） | 按路由表按需加载 |
| L3 | `skills/` | 四个细粒度子技能 | 落地具体动作时调用 |
| L4 | `scripts/` | 确定性质量门禁脚本 | 需重复/可复现检查时运行 |
| L5 | `assets/` | 提交约定、模板清单等规范 | 被 scripts 读取执行 |

## 加载顺序

1. 读 `SKILL.md` 路由表，判断任务属于哪一类。
2. 做方法论决策（提交规范、版本号、Prompt 评估、架构选型）→ 读对应 `references/`。
3. 要落地具体动作（写提交、做审查、优化 prompt、生成模板）→ 调 `skills/` 子技能。
4. 需要确定性检查（CI 门禁、模板核查）→ 跑 `scripts/`，规则来自 `assets/`。

## 技能清单

| # | 技能 | 用途 |
|---|------|------|
| 1 | git-workflow | Git 分支策略、提交规范、rebase/squash 最佳实践 |
| 2 | code-review-assistant | 代码审查自动化：预审、问题分类、修复建议 |
| 3 | template-scaffolder | 项目模板生成器：快速搭建项目骨架 |
| 4 | prompt-optimizer | Claude Code prompt 优化：写作、调试、重构 |

## 定位

- 面向个人开发者和小团队（2-10 人）
- 聚焦"写代码前的准备"和"写代码后的审查"
- 不替代 CI/CD 或 DevOps 工具
