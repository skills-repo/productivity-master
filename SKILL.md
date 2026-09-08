---
name: productivity-master
description: >-
  开发者生产力技能库：覆盖 Git 提交/分支规范与版本管理、多维度代码审查、LLM Prompt 工程优化、项目架构检测与模板生成四大场景，并附可直接运行的质量门禁脚本。
  当用户说"提交规范"、"代码审查"、"优化 prompt"、"项目模板"、"分支命名"、"changelog"时触发。
agent_created: true
metadata:
  version: 1.0.0
  category: 生产力
  difficulty: 进阶
  architecture: superpower
---

# 生产力大师

> 把 AI 变成一名「写代码前帮你定规范、写代码后帮你把关」的开发搭档，让重复的质量动作交给脚本，人只做判断。

本技能采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 放在 `references/` 中**按需加载**，细粒度能力放在 `skills/` 子技能，确定性任务交给 `scripts/`，可复用清单放在 `assets/`。

## 何时使用

- 规划功能分支、写提交信息、决定升 major/minor/patch 版本号时
- 合并 PR 前做多维度代码审查（正确性/可读性/架构/安全/性能）时
- 输出不稳定的 Prompt 需要系统评估与迭代优化时
- 需要把项目架构沉淀成可复用模板或蓝图时
- 想用脚本自动校验提交约定 / 项目模板清单（CI 门禁）时
- 团队要统一 Git 与代码质量规范时
- 需要把跨会话的偏好、决策、项目上下文沉淀成持久记忆，或维护 `CLAUDE.md`/`MEMORY.md` 记忆文件时

## 能力索引（超级技能路由）

| 任务 | 读取 / 调用 | 关键词（grep 线索） |
|------|------------|---------------------|
| 提交/分支约定、PR 审查该拦什么、版本号怎么定 | [references/commit-and-pr-quality-gates.md](references/commit-and-pr-quality-gates.md) | 提交规范 分支命名 PR审查 版本号 squash |
| Prompt 评估协议、few-shot 选择、上下文预算 | [references/prompt-evaluation-protocol.md](references/prompt-evaluation-protocol.md) | prompt 评估 迭代 few-shot token预算 回归 |
| 架构检测置信度、模板粒度选型、参数化蓝图 | [references/template-architecture-selection.md](references/template-architecture-selection.md) | 架构检测 模板选型 蓝图 参数化 ADR |
| 记忆/知识管理决策树、Zettelkasten、记忆文件维护、间隔回顾 | [references/memory-keeper.md](references/memory-keeper.md) | 记忆 知识管理 第二大脑 回顾 记忆文件 沉淀 |
| Git 工作流与语义化版本（细粒度调用） | [skills/git-workflow/SKILL.md](skills/git-workflow/SKILL.md) | git workflow trunk-based conventional commits 版本 |
| 多维度代码审查（细粒度调用） | [skills/code-review-assistant/SKILL.md](skills/code-review-assistant/SKILL.md) | code review 审查 正确性 安全 性能 |
| Prompt 架构与输出格式优化（细粒度调用） | [skills/prompt-optimizer/SKILL.md](skills/prompt-optimizer/SKILL.md) | prompt optimizer 系统提示 few-shot 输出格式 |
| 项目工作流分析与模板生成（细粒度调用） | [skills/template-scaffolder/SKILL.md](skills/template-scaffolder/SKILL.md) | template scaffolder 架构检测 蓝图 工作流 |
| 记忆/知识管理（细粒度调用） | [skills/memory-keeper/SKILL.md](skills/memory-keeper/SKILL.md) | memory-keeper 记住 知识库 笔记 回顾 inbox 跨会话 |

## 内置脚本（确定性、可重复执行）

放在 `scripts/`，纯标准库、零依赖、只读、不联网，规则来自 `assets/`：

- [scripts/check_commit_conventions.py](scripts/check_commit_conventions.py) — 校验提交信息（Conventional Commits）与分支命名是否合规
- [scripts/check_project_template.py](scripts/check_project_template.py) — 按项目模板清单核查目录结构、README 章节与残留 TODO

运行示例：

```bash
python3 scripts/check_commit_conventions.py --check-rules        # 自检规则（0 错误）
git log --pretty=%s main..HEAD | python3 scripts/check_commit_conventions.py --stdin
python3 scripts/check_project_template.py --target ./my-project  # 核查项目模板
```

## 模板资源

`assets/` 提供可直接套用的规范与清单（被上述脚本读取执行）：

- [assets/commit-conventions.json](assets/commit-conventions.json) — 提交类型白名单、分支命名正则、版本号规则
- [assets/project-template-manifest.json](assets/project-template-manifest.json) — 标准项目必需文件/README 章节/残留 token 清单

## 核心原则（始终遵循）

1. **渐进式加载**：先读本路由表与对应 `references/`，再动手；不凭记忆猜命令与 API。
2. **原子提交优先**：一个提交只解决一件事，无法一句话说清就还没拆好。
3. **审查保底线**：阻断级（正确性/安全/数据丢失）必须拦，建议级不阻塞合并。
4. **优化靠证据**：Prompt 改动每次只变一个变量，用评估集量化前后对比，不靠感觉。
5. **模板讲复用**：复用 <3 次不值得沉淀模板，维护成本会超过收益（YAGNI）。
6. **明确边界**：脚本只做确定性检查、只出报告不替你拍板；架构选型与发布决策由人定。

## 与其他技能协作

- 文档类变更记录 → `skills-repo/docs-writer`（`changelog-writer` 从 commit 生成 CHANGELOG）
- 办公文档处理 → `skills-repo/office-master`
- 本仓库所有子技能来源见各自 `source` 字段，均为 skills.sh 社区成熟技能衍生
- `memory-keeper`（个人知识/持久记忆）与 `prompt-optimizer` 的「LLM 上下文预算」正交：前者管人/项目的长期记忆资产，后者管单次 Prompt 的窗口效率，互不重叠
