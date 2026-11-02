---
name: codebase-refactoring
description: 已有代码库的结构演进：重构时机判断、现状测绘、接缝先行的小步计划与技术债偿还
source:
  type: derived
  repo: skills-repo/productivity-master
  path: skills/codebase-refactoring/SKILL.md
  version: 1.0.0
  updated: 2026-11-02
  url: https://github.com/mattpocock/skills/tree/main/skills/engineering/improve-codebase-architecture
metadata:
  category: 架构演进
  platform: 通用
  difficulty: 进阶
---

# 代码库重构与架构演进

> 面向**已经存在、还要继续长**的代码库：判断该不该动手、找到真正的结构问题、
> 把大改拆成每一步都保持绿色的小步，并识别「改了个寂寞」的无效 churn。
> 不改需求行为，不发新框架，不做组织级架构治理。

## 能力

- **重构时机判断**：该动 / 不该动的止损决策（见「不做什么」）
- **现状测绘**：读陌生代码库、定位变更热区（hot spot），区分结构问题与表面坏味道
- **问题分类**：耦合方向错误、抽象泄漏（leak across seam）、职责漂移、接缝缺失、重复的真实成本 vs 虚假成本
- **深度重构**：把 shallow module 做成 deep module——小 interface 后藏大量行为，产出调用方的 leverage 与维护者的 locality
- **计划编排**：先建接缝（seam）再搬移，strangle-the-old 新旧并行运行，每步可独立合入
- **安全网前置**：无测试覆盖时先补 characterization test，再动结构
- **技术债台账**：记录、定价（每次变更多付的利息）、约定偿还触发条件

## 使用方式

```
/codebase-refactoring 这个模块改一次要动五个地方，帮我评估值不值得重构
/codebase-refactoring 把「订单逻辑从控制器里搬出来」拆成可逐步合入的小步计划
/codebase-refactoring 扫一遍最近三个月改动最频繁的区域，列出结构改进候选
```

## 工作流

1. **划定范围（YAGNI）**：重构的收益是「未来改这里更省事」，所以只看变更热区——
   先用 `git log --oneline` 找出反复出现的路径；用户已指定方向时直接采纳，跳过推断。
   从不改动的代码里的丑陋不是问题，不要顺手"净化"。
2. **判断值不值得动手**：对每个候选跑 **deletion test**——假想删掉这个模块，
   复杂度是**收敛**到一处（值得深挖）还是只是**搬到别处**（放弃）。
3. **测绘问题**：以 fresh 视角走读，只记录摩擦点：理解一个概念是否要跳很多小文件？
   interface 是否几乎和实现一样复杂（shallow）？紧耦合模块是否跨 seam 泄漏？
   哪部分只能靠端到端跑、测不到？
4. **建安全网**：目标区域测试不足时，先写 characterization test 锁住**现有外部行为**
   （只断言外部可见行为，不断言实现细节），全绿之后才允许搬代码。
5. **编排小步计划**：按 Fowler 的口径——每一步都小到"随时看得见程序是跑得通的"。
   固定顺序：**先加 seam（不改行为）→ 新实现与旧实现并行 → 逐个迁移调用方 → 删旧路径**。
   每步一个可独立合入的提交，中间态不破坏 CI。
6. **红队自检（关键）**：动手前反问——这次改完，测试面是否变小？调用方需知的
   interface 是否变简单？未来改这里是否真的更便宜？三问全否 ⇒ 判定为 churn，撤回。
   **one adapter = hypothetical seam，two = real**：只有一个实现的抽象是想象出来的接缝，别加。
7. **产出与记录**：输出候选清单（文件 / 问题 / 方案 / 收益 / 强度 `Strong`、`Worth exploring`、
   `Speculative`）与分步计划；被否决的方向连同**理由**记进决策文档（ADR），
   避免下一轮测绘重复提出同一件事。
8. **技术债定价**：台账每条写清「每次变更多付多少、什么时候必须还」，
   偿还时机绑定事件（下一次要改这个模块时顺手做掉），而不是绑定日历。

## 适用场景

- 某个模块改起来越来越贵，需要判断是真结构问题还是错觉
- 大重构需要拆成能逐步合入、随时可停的计划
- 遗留/即将长期演进的代码要补测试接缝
- 技术债需要有个地方记账并定价

## 限制

- 不改变外部行为；需要新行为请走需求实现，不要和重构混在一次变更里
- 不做大规模重写（rewrite）：重写丢行为语义，重构保留证据
- 不设计跨团队治理流程、架构委员会与评审规范（定位是个人与 2-10 人小团队）
- 无测试且无法写 characterization test 的代码：先补测试，本技能不给"裸改"许可

## 与相邻子技能的分工

- [skills/code-review-assistant/SKILL.md](../code-review-assistant/SKILL.md) 审**这一个 PR** 写得对不对（增量、评审视角）；本技能管**代码库随时间怎么演进**（存量、结构视角）。重构后的每个小步仍要交给它审查。
- [skills/template-scaffolder/SKILL.md](../template-scaffolder/SKILL.md) 为**新项目**生成骨架；本技能处理**已有代码**的结构问题，不产出模板。
- 提交拆分与版本升级口径 → [skills/git-workflow/SKILL.md](../git-workflow/SKILL.md)。
