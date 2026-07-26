---
name: template-scaffolder
description: 项目模板生成器，快速搭建 Node/React/Python/CLI 项目骨架，含目录和 CI 配置
source:
  type: original
  repo: skills-repo/productivity-master
  path: skills/template-scaffolder/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
metadata:
  category: 脚手架
  platform: 通用
  difficulty: 入门
---

# 模板脚手架

> 跳过项目初始化 boilerplate，一键生成标准化项目骨架。支持 Node、React、Python、CLI 等常见项目类型。

## 能力

- **多类型模板**：Node.js 库、React 应用、Python 包、CLI 工具、Monorepo
- **标准配置**：TypeScript/ESLint/Prettier、pytest/black、CI workflow 文件
- **目录结构**：按最佳实践自动生成合理的目录布局
- **依赖管理**：package.json / pyproject.toml 初始配置
- **Git 初始化**：.gitignore、.gitattributes 自动生成

## 使用方式

```
/template-scaffold 创建一个 TypeScript CLI 项目
/template-scaffold 初始化一个 React 全栈应用（前端+API）
/template-scaffold 搭建 Python 数据分析项目骨架
```

## 支持的项目类型

| 类型 | 技术栈 | 特点 |
|------|--------|------|
| `node-lib` | TypeScript + Vitest + tsup | npm 库发布就绪 |
| `react-app` | React + Vite + Tailwind | SPA 开箱即用 |
| `nextjs-full` | Next.js + Prisma + Auth.js | 全栈应用模板 |
| `python-pkg` | Python + pytest + ruff | PyPI 发布就绪 |
| `cli-tool` | TypeScript + Commander + ink | CLI 工具模板 |
| `monorepo` | pnpm workspace + Turborepo | 多包项目管理 |

## 工作流

1. 确认项目类型和技术栈偏好
2. 生成目录结构和所有基础文件
3. 写入配置（TSConfig、ESLint、CI workflow）
4. 初始化 Git 仓库
5. 输出项目启动指引

## 适用场景

- 新项目快速启动，避免手动搭建
- Hackathon 或原型快速出活
- 团队统一项目初始化标准
- 学习新框架时获得规范的起始代码

## 限制

- 模板为通用最佳实践，高度定制需手动修改
- 不包含业务逻辑代码（仅骨架）
- 框架大版本更新可能导致模板过时，需定期维护
