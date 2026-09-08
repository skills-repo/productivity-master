---
name: memory-keeper
description: 个人知识管理与持久记忆：跨会话记忆维护、第二大脑/Zettelkasten 知识库、记忆文件（CLAUDE.md/MEMORY.md/AGENTS.md）管理、信息捕获与间隔回顾
source:
  type: original
  repo: skills-repo/productivity-master
  path: skills/memory-keeper/SKILL.md
  version: 1.0.0
  updated: 2026-08-12
metadata:
  category: 知识管理
  platform: 通用
  difficulty: 进阶
---

# 记忆管家（个人知识 & 持久记忆）

> 让 AI 搭档「记得住」：把散落各处的偏好、决策、项目上下文沉淀成可检索、可回顾、跨会话不丢的个人知识系统。
> 与 `prompt-optimizer` 的「LLM 上下文预算（token 分配/压缩）」正交——本技能管的是**人/项目的长期记忆**，不是单次 Prompt 的窗口。

## 能力

- **跨会话记忆维护**：把每轮会话里值得长期保留的结论写进 `MEMORY.md` / 项目记忆文件，避免「下次对话又从零讲起」。
- **记忆文件治理**：维护 `CLAUDE.md` / `AGENTS.md` / `MEMORY.md` 三层（项目约定 / 身份契约 / 长期记忆），防止膨胀与过时。
- **第二大脑 / Zettelkasten**：用原子笔记 + 双向链接构建可生长的知识库，而非堆砌收藏夹。
- **信息捕获与回顾**：临时 inbox 收件箱 → 定期处理 → 间隔回顾（spaced recall），对抗遗忘曲线。
- **决策与偏好归档**：把「为什么这么定」连同结论一起存下，未来同类情境可直接复用，不必重新推理。

## 何时使用

- 用户说「记住这个」「以后默认…」「上次我们怎么决定的」时
- 跨多轮对话需要保持项目/人物上下文连贯时
- 知识零散、重复踩同一个坑、收藏一堆从不回看时
- 需要把 `CLAUDE.md` / `MEMORY.md` 从臃肿重写瘦身时

## 工作流

1. **捕获（Capture）**：先把任何值得留的东西丢进 inbox，不做分类（降低 friction）。
2. **处理（Process）**：每条判断——丢弃 /  actionable 进任务系统 / 知识进笔记 / 偏好进记忆文件。
3. **连接（Connect）**：知识笔记用「它和谁相关」而非「它属于哪个文件夹」组织（Zettelkasten 核心）。
4. **回顾（Review）**：每日收 inbox，每周回顾链接缺口，每月间隔复习高价值笔记。
5. **沉淀（Persist）**：把跨会话结论写进 `MEMORY.md` 对应日期/主题段，项目级约定写进项目记忆。

## 边界

- 不替用户拍板「哪些该记」——只给判断框架与模板，敏感信息是否落盘由人决定。
- 记忆文件是增量追加，绝不整文件覆写（避免丢历史）。
- 与 `prompt-optimizer` 分工：它管单次 Prompt 的上下文效率，本技能管长期知识资产。

## 深层方法

决策树、命令、记忆文件模板与踩坑清单见 [references/memory-keeper.md](../../references/memory-keeper.md)。
