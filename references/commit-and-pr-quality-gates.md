# 提交与 PR 质量门禁（跨 git-workflow × code-review-assistant）

> 子技能 `git-workflow` 讲「怎么提」，`code-review-assistant` 讲「怎么审」。本文档补齐二者之间**缺失的决策层**：
> 什么时候该提、这次该升哪个版本号、squash 还是 merge、审查该拦哪类问题。这是子技能装不下的判断方法论。

## 1. 决策树：现在该提交吗？

```
开始
├─ 改动是否可独立回滚？（单一意图？）
│   ├─ 否 → 拆成原子提交（见 git-workflow 原子提交法）
│   └─ 是 ↓
├─ 是否通过本地自检？
│   ├─ 未跑 lint/test → 先跑，不过不提
│   └─ 已过 ↓
├─ 是否混入了调试残留（print/注释掉的代码/临时密钥）？
│   ├─ 是 → 清掉再提
│   └─ 否 ↓
└─ 提交 → 选类型 → 选版本号（第 3 节）
```

**铁律**：一个提交只解决一件事。无法用一句话说清「这个提交干了什么」= 还没拆好。

## 2. 选型矩阵：分支策略

| 团队规模 | 推荐策略 | 合并方式 | 适用原因 |
|----------|----------|----------|----------|
| 个人 / 1-2 人 | Trunk-Based + 短功能分支 | squash | 历史干净，回滚点清晰 |
| 小团队 3-10 人 | 功能分支 + PR | squash 或 rebase | 有 review 门槛，避免 main 污染 |
| 多团队 / 需发布协调 | Release 分支 | merge commit | 需要 cherry-pick 与并行维护 |
| 需要 bisect 追因 | 严格原子提交 | rebase | 每个提交都可独立验证 |

> 本仓库 `git-workflow` 默认 Trunk-Based + squash。若你所在团队用 GitFlow（长周期 develop/release 分支），本文档**不覆盖**，需人工补充。

## 3. 版本号决策矩阵（SemVer）

```
不兼容的 API 变更 / 删除公开能力？
├─ 是 → MAJOR (1.0.0 → 2.0.0)，必须在 CHANGELOG 标 BREAKING
└─ 否 ↓
新增向后兼容的功能（feat）？
├─ 是 → MINOR (1.2.3 → 1.3.0)
└─ 否 ↓
向后兼容的修复（fix/docs/style/chore）？
└─ 是 → PATCH (1.2.3 → 1.2.4)
```

**易错点**：`refactor` 不一定安全。重构若改变对外函数签名 → 视为 BREAKING（升 MAJOR）。
依赖 [scripts/check_commit_conventions.py](../scripts/check_commit_conventions.py) 可在 CI 里强制类型合法、主题行不超长、分支名匹配 `feature/*` 等约定（规则见 [assets/commit-conventions.json](../assets/commit-conventions.json)）。

```bash
# 本地提交前自检（逐行喂入待提交主题）
git log --pretty=%s HEAD~5..HEAD | python3 scripts/check_commit_conventions.py --stdin
# 校验当前分支名
python3 scripts/check_commit_conventions.py --branch "$(git rev-parse --abbrev-ref HEAD)"
```

## 4. PR 审查：该拦什么、该放什么

审查分三档（来自 code-review-assistant 五维框架的落地口径）：

| 级别 | 含义 | 处理 |
|------|------|------|
| **阻断 Blocker** | 正确性/安全/数据丢失风险 | 必须修，否则不合并 |
| **严重 Major** | 可读性/架构明显偏离、潜在 N+1 | 建议修，可协商 |
| **建议 Minor** | 命名/注释/风格 | 不阻塞，择机处理 |

**放行标准（不是「完美才放」）**：本次变更整体**改善**了代码健康度即可合并。审查的目的是「别让主线变差」，不是「挑刺到完美」。

常见误拦（应放行）：
- 风格偏好之争（用 lint 统一，别在 review 里吵）
- 与本次变更无关的重构建议（开新 issue，别堵在当前 PR）

常见漏拦（应阻断）：
- 明文密钥 / token 提交
- 未处理错误路径（`except: pass`）
- 删除的公共函数被外部调用（破坏 SemVer）

```bash
# 大 PR 分批审：只看某目录的变更
git diff --stat main...HEAD -- src/
# 找回被误删的公开函数引用
git grep -n "被删函数名" -- '*.py'  # 提交前本地先扫一遍
```

## 5. 典型坑与规避

1. **squash 吞掉上下文**：squash 后单条提交信息要重写概括，别保留「fix typo / fix again」噪声历史。
2. **WIP 提交进 main**：给分支名加 `wip/` 前缀并在 CI 屏蔽；合并前必须 rebase 成原子提交。
3. **CHANGELOG 与版本号不一致**：用 `changelog-writer`（docs-writer 仓库）从 commit 生成，不要手填。
4. **大 PR 一次性审**：超过 ~400 行强制拆 PR 或要求作者先自审，否则审查质量断崖。
5. **`--no-verify` 跳过 hook**：CI 里仍要跑 `check_commit_conventions.py`，本地 hook 被跳过不等于门禁失效。

## 6. 实战：把一个「大杂烩」提交拆干净

假设工作区有 3 类改动混在一起：新增登录接口、顺手改了日志格式、修了个小 bug。正确拆法：

```bash
# 1) 看混合差异
git diff --stat
# 2) 按文件分批改：先只加登录相关
git add src/auth/ tests/test_auth.py
git commit -m "feat(auth): add OAuth login endpoint"
# 3) 再单独提日志格式（属 style/refactor）
git add src/logger.py
git commit -m "refactor(logger): standardize JSON log fields"
# 4) 最后提 bug 修复
git add src/session.py
git commit -m "fix(session): prevent nil deref on expired token"
# 5) 复核每个提交都单一意图
git log --oneline -3
```

若已经「一锅端」提交了，用软重置拆回工作区再逐个提交：

```bash
git reset --soft HEAD~1      # 撤回到暂存区，保留改动
git restore --staged .       # 全部退到工作区
# 然后按上面的 add+commit 逐条来
```

## 7. CI 门禁集成（GitHub Actions 示例）

把约定检查接进 CI，让「提交规范」从口头约定变成自动拦截：

```yaml
# .github/workflows/conventions.yml
name: commit-conventions
on: [pull_request]
jobs:
  lint-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - run: |
          git log --pretty=%s origin/main..HEAD \
            | python3 scripts/check_commit_conventions.py --stdin
      - run: |
          python3 scripts/check_commit_conventions.py \
            --branch "${{ github.head_ref }}"
```

> 注意：`scripts/` 在本仓库内，CI 需先 checkout 本仓库或把脚本复制进被检项目。规则文件 [assets/commit-conventions.json](../assets/commit-conventions.json) 是脚本的单一事实来源，团队改约定只改这一处。

## 8. 典型坑与规避（续）

6. **rebase 冲突后丢失提交**：rebase 冲突解决完务必 `git rebase --continue`，别直接 `commit` 另起炉灶，否则历史分叉。
7. **`fixup`/`squash` 提交忘了 rebase**：交互式 rebase 留下的 `fixup!` 提交进入 main 会污染历史，合并前清理。
8. **CHANGELOG 漏记安全修复**：`security` 类修复要单独在 CHANGELOG 列 Security 段，不能埋进 Fixed。
9. **把 `chore` 当万能类型**：依赖升级若是安全补丁应标 `fix`，仅 format/构建改动才用 `chore`。
10. **review 只在 GitHub 网页点**：大改动先在本地 `git diff main...HEAD` 通读再评，网页逐行易漏全局问题。

## 9. 可勾选清单

- [ ] 每个提交单一意图，能一句话说清
- [ ] 本地 lint/test 通过，无调试残留
- [ ] 提交类型在 `feat/fix/docs/...` 白名单内
- [ ] 主题行 ≤72 字符，分支名匹配 `feature/*` 约定
- [ ] 破坏性变更已标 BREAKING 并计划升 MAJOR
- [ ] PR 描述含「为什么」与「测试方式」
- [ ] 阻断级问题已清零，严重级已协商
- [ ] CHANGELOG 与版本号一致（发布时）
- [ ] CI 已接入 `check_commit_conventions.py` 提交/分支门禁
- [ ] 混合改动已拆成原子提交（无「一锅端」）

## 10. 发布前速查（从提交到 tag）

```
合并到 main
├─ 跑 changelog-writer 生成 CHANGELOG（docs-writer 仓库能力）
├─ 据变更类型定版本号（第 3 节矩阵）
├─ 打 tag: git tag -a vX.Y.Z -m "..."
├─ 推 tag: git push origin vX.Y.Z
└─ 发布说明引用 CHANGELOG 的 Added/Fixed/Breaking 段
```

**不要**在 tag 之后又往 main 追加「忘记的」fix 却不升版本——已发布的版本号不可复用，必须升 PATCH 重新发。

## 12. 相关子技能与层次边界（L2 → L3）

本文档是 L2 决策层，落地调用以下 L3 子技能：

- [skills/git-workflow/SKILL.md](../skills/git-workflow/SKILL.md) — 怎么提（Trunk-Based、原子提交、语义化版本）
- [skills/code-review-assistant/SKILL.md](../skills/code-review-assistant/SKILL.md) — 怎么审（五维框架、分级口径）

边界：本文档只补「何时提 / 升哪个版本 / squash 还是 merge / 审查拦哪类」的判断层；具体提交命令与逐维审查流程在对应子技能，本文档不复制。

