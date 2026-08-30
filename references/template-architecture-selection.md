# 项目模板与架构选型（template-scaffolder 增量方法论）

> 子技能 `template-scaffolder` 讲「怎么检测架构、生成蓝图」。本文档补它**装不下**的判断层：
> 检测到模式后**要不要**生成模板、生成哪种粒度、哪些项目根本不该自动生成模板。避免「为生成而生成」。

## 1. 决策树：这个项目值得生成模板吗？

```
接到「生成项目模板」请求
├─ 项目是否高度定制化 / 一次性脚本？
│   ├─ 是 → 不生成模板，直接给一次性的实现
│   └─ 否 ↓
├─ 团队是否会在同模式上重复造多个服务？
│   ├─ 否 → 不必沉淀模板，维护成本 > 收益
│   └─ 是 ↓
├─ 架构模式是否清晰可检测？（见第 2 节）
│   ├─ 否 → 先人工确认模式，再生成（别盲生成）
│   └─ 是 ↓
└─ 生成「蓝图模板」而非「可运行脚手架」（蓝图风险更低）
```

**铁律**：模板的价值 = 复用次数 × 每次节省时间 − 维护成本。复用 <3 次不值得。

## 2. 架构模式检测置信度矩阵

`template-scaffolder` 能识别分层/Clean/CQRS/Microservices/MVC/MVVM。但检测有置信度：

| 模式 | 高置信信号 | 低置信（需人工确认） |
|------|------------|----------------------|
| 分层 Layered | `controller/service/repository` 三层目录 | 只有 service 一个目录 |
| Clean | `domain/usecase/interface` 边界清晰 | 混在一起只叫 `core` |
| CQRS | 命令与查询分库/分 handler | 同表读写但代码里分了两个方法 |
| Microservices | 多独立部署单元 + 独立 data store | 单仓库多模块（实为 monolith） |
| MVC | `models/views/controllers` | MVVM 误判（有 ViewModel） |
| MVVM | 有 `ViewModel` 绑定层 | 只是把 Controller 改名 |

> 低置信时**不要**自动套模板：先问用户确认，否则生成的蓝图会误导后续开发。

## 3. 选型矩阵：生成什么粒度？

| 需求 | 推荐产出 | 理由 |
|------|----------|------|
| 新人快速上手 | 架构导图 + 目录约定文档 | 重「理解」轻「代码」 |
| 标准化功能开发 | 单功能端到端蓝图（入口→逻辑→数据→测试） | 可复制粘贴改 |
| 多服务同构 | 参数化模板骨架（变量占位） | 一处改全局生效 |
| 仅文档归档 | 工作流文档 + 序列图 | 不碰代码 |

本仓库 `assets/project-template-manifest.json` 就是「标准项目应包含什么」的清单规范，可被 `scripts/check_project_template.py` 自动核查（必需文件、README 章节、残留 TODO）。生成模板时直接对齐这份清单，产出即合规。

## 4. 蓝图模板结构（推荐骨架）

```
<feature>/
├── 入口层/        # controller / handler / route
├── 业务逻辑层/    # service / usecase
├── 数据访问层/    # repository / dao
├── 错误处理/      # 统一错误码与返回结构
├── 测试/          # 单元 + 集成 + 端到端 三档
└── 文档/          # 该功能的 ADR（架构决策记录）
```

生成时用 `template-scaffolder` 检测出的真实技术栈填占位，而不是硬编码。例如检测到 Spring → 用 `@RestController`；检测到 FastAPI → 用 `@app.get`。

## 5. 典型坑与规避

1. **把蓝图当脚手架直接跑**：蓝图是「怎么写」的指引，不是 `npm create` 级别的产物；写成可运行脚手架要额外处理依赖/配置，易过期。
2. **过度抽象**：为「未来可能复用」抽基类，结果只用一次，维护负担翻倍。YAGNI。
3. **模板与真实技术栈脱节**：检测成 Spring 却生成 Express 风格代码 → 检测置信度低时必须人工确认。
4. **忽略错误处理模板**：只给 happy path，真实项目最缺的是统一错误结构，蓝图要包含。
5. **文档不随模板更新**：模板改了 ADR/README 没改 → 用 `check_project_template.py` 定期扫残留 TODO 与缺失章节。
6. **一个模板打天下**：不同领域（CRUD vs 计算密集）套同一模板 → 按模式分多套，别贪省。

## 6. 序列图指引（工作流文档的一部分）

`template-scaffolder` 会生成请求/响应时序图。画之前确认：

```text
participant Client
participant Controller
participant Service
participant Repository
Client -> Controller: HTTP 请求
Controller -> Service: 调用业务
Service -> Repository: 查数据
Repository --> Service: 结果
Service --> Controller: 领域对象
Controller --> Client: 响应
```

> 时序图的价值是暴露「跨层调用是否绕弯」。若出现 Controller 直接调 Repository 跳过 Service，是架构偏离信号。

## 7. 跨模式复用：参数化模板怎么写

当需要为多服务生成同构骨架时，用占位变量而不是复制粘贴：

```yaml
# template.meta.yaml（示意）
service_name: "{{name}}"
layers: [controller, service, repository]
error_contract: "{{err_code}}: {{message}}"
test_tiers: [unit, integration, e2e]
```

生成脚本读这份 meta，按检测到的技术栈渲染每一层。好处：改一处（如统一错误结构）所有服务同步更新，不会出现「A 服务用 code，B 服务用 message」的漂移。

> 但参数化有代价：占位越多越难读。约定占位只用于「技术栈相关」的部分（注解风格、目录名），业务逻辑留给人工填。

## 8. 与 `check_project_template.py` 的闭环

生成模板不是终点，要能自动验证「按模板建的项目是否合规」：

```bash
# 对刚生成的项目跑模板清单核查
python3 scripts/check_project_template.py --target ./generated-service
# 期望输出 [OK]；若报缺失 README 章节或残留 TODO，回去补模板
```

把这条命令接进生成流程的收尾，保证「生成的每个项目开箱即合规」。清单文件 `assets/project-template-manifest.json` 是唯一事实来源，团队调整「标准项目该有什么」只改它。

## 9. 实战：从零到蓝图的一天

```
09:00 检测技术栈（Spring Boot + PostgreSQL）→ 高置信 Layered
09:30 与团队确认：3 个同类服务要建 → 值得沉淀
10:00 生成单功能蓝图（登录）：入口→Service→Repository→错误处理→测试
11:00 抽参数化 meta，渲染另外 2 个服务的骨架
14:00 跑 check_project_template.py 批量核查 3 个产出 → 1 个漏 README 许可段
14:30 补模板 + 重生成，3/3 通过
15:00 写 ADR 记录「为何选 Layered 而非 Clean」
```

## 10. 典型坑与规避（续）

7. **模板过期**：技术栈升级后老模板还用旧注解 → 模板要随栈版本打 tag。
8. **忽略团队习惯**：检测对但团队有自己约定（如所有 Service 后缀 Manager）→ 模板支持后缀占位。
9. **序列图与代码不符**：画了 Service→Repository 但代码里绕了缓存层 → 图要回归代码复核。
10. **ADR 缺失**：半年后没人记得「为什么用 CQRS」→ 每个蓝图强制附一份 ADR。

## 11. 可勾选清单

- [ ] 已确认项目复用价值（≥3 次才沉淀模板）
- [ ] 架构模式检测置信度高，或已人工确认
- [ ] 产出粒度匹配需求（文档/蓝图/骨架）
- [ ] 蓝图对齐 `project-template-manifest.json` 必需项
- [ ] 含统一错误处理与三档测试结构
- [ ] 技术栈占位真实（非硬编码错配）
- [ ] 附 ADR 记录关键架构决策
- [ ] 没为「可能复用」过度抽象（YAGNI）
- [ ] 用 `check_project_template.py` 扫过残留 TODO
- [ ] 参数化 meta 仅覆盖技术栈相关部分
- [ ] 生成产物已批量跑模板核查且全通过

## 12. 相关子技能与层次边界（L2 → L3）

本文档是 L2 选型判断层，落地调用 L3 子技能：

- `skills/template-scaffolder/SKILL.md` — 架构检测与蓝图生成（具体模式识别、技术栈检测）

边界：本文档只补「检测到模式后要不要生成模板、生成哪种粒度」的判断层；具体检测与生成流程在子技能，本文档不复制。
