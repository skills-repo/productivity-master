# Productivity Master — 开发者生产力技能库

> 面向个人和小团队的开发者效率工具集，覆盖 Git 工作流、代码审查、项目模板、Prompt 优化四大场景。

## 架构说明

本仓库采用 **superpower 架构**（skills-repo 组织默认架构）：

- `SKILL.md` — L1 路由层，只做能力索引，不写方法论
- `references/` — L2 深层 playbook（提交/PR 质量门禁、Prompt 评估协议、模板架构选型）
- `skills/` — L3 四个细粒度子技能，可单独安装
- `scripts/` — L4 确定性质量门禁脚本（提交约定 / 项目模板核查）
- `assets/` — L5 可复用规范与清单（提交约定、模板清单）

## 技能列表

| 技能 | 描述 | 难度 | 来源 |
|------|------|------|------|
| [git-workflow](skills/git-workflow/SKILL.md) | Git 工作流：Trunk-Based 开发、原子提交、语义化版本 | 入门 | [衍生](https://skills.sh/addyosmani/agent-skills/git-workflow-and-versioning) |
| [code-review-assistant](skills/code-review-assistant/SKILL.md) | 多维度代码审查：正确性、可读性、架构、安全、性能 | 入门 | [衍生](https://skills.sh/addyosmani/agent-skills/code-review-and-quality) |
| [template-scaffolder](skills/template-scaffolder/SKILL.md) | 项目工作流分析与蓝图生成：架构检测、技术栈识别 | 入门 | [衍生](https://skills.sh/github/awesome-copilot/project-workflow-analysis-blueprint-generator) |
| [prompt-optimizer](skills/prompt-optimizer/SKILL.md) | LLM Prompt 架构设计：系统提示、上下文管理、评估迭代 | 进阶 | [衍生](https://skills.sh/davila7/claude-code-templates/prompt-engineer) |

## 安装

整库安装（推荐，拿到路由层 + 全部 references/scripts/assets）：

```bash
npx skills add skills-repo/productivity-master -g -y
```

单技能安装（只要某一个细粒度能力）：

```bash
npx skills add skills-repo/productivity-master@git-workflow -g -y
npx skills add skills-repo/productivity-master@code-review-assistant -g -y
npx skills add skills-repo/productivity-master@template-scaffolder -g -y
npx skills add skills-repo/productivity-master@prompt-optimizer -g -y
```

## 内置脚本

```bash
python3 scripts/check_commit_conventions.py --check-rules          # 提交/分支约定自检
git log --pretty=%s main..HEAD | python3 scripts/check_commit_conventions.py --stdin
python3 scripts/check_project_template.py --target ./my-project    # 项目模板核查
```

## 贡献

欢迎提交 Issue 或 PR 补充新的生产力技能。请参考 [CONTRIBUTING.md](../skills-repo-admin/rules/skill-format.md) 的格式规范。
