---
name: template-scaffolder
description: 项目工作流分析与蓝图生成：自动检测架构模式、技术栈，生成实现模板
source:
  type: derived
  repo: skills-repo/productivity-master
  path: skills/template-scaffolder/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/github/awesome-copilot/project-workflow-analysis-blueprint-generator
metadata:
  category: 项目模板
  platform: 通用
  difficulty: 入门
---

# 项目工作流与模板生成

> 自动检测项目架构模式和技术栈，生成端到端实现蓝图，作为相似功能的开发模板。

## 能力

- **架构检测**：自动识别分层/Clean/CQRS/Microservices/MVC/MVVM 模式
- **技术栈识别**：.NET/Java/Spring/Node.js/Python/React/Angular 自动检测
- **工作流文档**：入口 → 服务层 → 数据访问 → 错误处理 → 测试全覆盖
- **序列图生成**：请求/响应流程的可视化时序图
- **测试模式**：单元测试、集成测试、端到端测试策略

## 使用方式

```
/template-scaffolder 分析这个项目的架构，生成新功能开发模板
/template-scaffolder 为这个 API 端点生成完整的实现蓝图
/template-scaffolder 记录 3 个代表性工作流作为团队模板
```

## 工作流

1. 检测项目技术栈和架构模式
2. 选择 1-5 个代表性端到端工作流
3. 逐层分析：入口点 → 业务逻辑 → 数据访问 → 错误处理
4. 生成实现蓝图（含代码结构和测试模式）
5. 输出为可复用的开发模板

## 适用场景

- 新成员上手项目的架构指引
- 标准化功能开发流程
- 技术文档自动生成
- 微服务间调用关系梳理

## 限制

- 生成的是蓝图模板，不是可直接运行的脚手架代码
- 复杂项目需人工确认检测到的架构模式
- 不涉及 CI/CD 和部署配置

## 相关参考（Playbook）

架构模式检测置信度、模板粒度选型与「要不要生成模板」的决策树见 `references/template-architecture-selection.md`。