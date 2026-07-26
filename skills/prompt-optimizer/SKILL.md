---
name: prompt-optimizer
description: Claude Code prompt 优化：从模糊需求到精准指令，含结构化写作模板、上下文组织、迭代改进策略
source:
  type: original
  repo: skills-repo/productivity-master
  path: skills/prompt-optimizer/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
metadata:
  category: Prompt
  platform: Claude Code
  difficulty: 进阶
---

# Prompt 优化器

> 帮你写出更精准的 Claude Code prompt：结构化需求 → 减少来回沟通 → 获得更高质量的输出。

## 能力

- **需求澄清**：从模糊描述中提取核心意图，生成结构化问题
- **上下文组织**：识别哪些文件/代码应放入 prompt，哪些是噪音
- **模板库**：bug 修复、重构、review、写测试、文档生成的专用 prompt 模板
- **迭代改进**：分析 AI 输出偏差，给出 prompt 修正建议
- **Token 效率**：在信息完整的前提下最小化 token 消耗

## 使用方式

```
/prompt-optimize "帮我改一下登录功能"     # 帮你把模糊需求转为精准 prompt
/prompt-optimize --review 上一次的 prompt  # 分析上次 prompt 为什么输出不理想
```

## Prompt 模板

### Bug 修复
```
目标：修复 [issue #] [一句话现象]
上下文：[相关文件路径列表]
约束：[不改变 API / 不引入新依赖 / 需向后兼容]
预期：[修复后的行为]
```

### 代码重构
```
目标：[提取函数/拆分模块/改名]
范围：[文件:路径 或 函数:名称]
原则：[单一职责/不改变行为/保持测试通过]
```

### 写测试
```
目标：[单元测试/集成测试]
范围：[函数名/模块路径]
覆盖：[正常路径, 边界值, 异常输入, 错误处理]
框架：[Jest/Vitest/Pytest]
```

## 工作流

1. 接收用户的模糊需求
2. 提问澄清：范围？约束？预期？
3. 生成结构化 prompt，用户确认
4. 分析 AI 输出与预期的偏差
5. 给出 prompt 改进建议（如果需要迭代）

## 适用场景

- 不熟悉 Claude Code 的提示词写法
- 复杂需求一次写不清楚，来回多轮
- 同样的需求每次输出质量不稳定
- 团队想要统一的 prompt 写作风格

## 限制

- 优化后的 prompt 仍然依赖用户的领域知识完整性
- 不保证一次优化就能获得完美输出（可能需要迭代）
- 模板为起点，复杂场景需二次定制
