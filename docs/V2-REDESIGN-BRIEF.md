# OpenVibe V2 Redesign Brief

> Created: 2026-02-08
> Status: ✅ Direction Confirmed — See `V2-VISION.md`
> Owner: Charles (@zurrix)

## ✅ Decision Made (2026-02-09)

**方向已确认，详见 `V2-VISION.md`**

核心结论：
- **定位**: Agent 融入组织的操作系统 (组织层，不是智能层)
- **体验**: Trust & Governance + Agent as Employee
- **战略**: OpenVibe (开源) + Vibe AI (商业化) 双轨

---

## 背景

V1 设计基于 **Fork/Resolve** 概念发展了大量文档，但 Charles 发现核心假设有问题：

### V1 的根本问题

1. **概念 Drift** — 从原始 thesis "AI cognitive amplification" 漂移成了 "conversation management"
   - 原始想法：1 human + AI deep dive → 压缩结果给团队
   - 漂移后：多人 side-discussion → AI 最后 summarize

2. **市场定位危险** — "Slack with AI summaries" 是 crowded market
   - OpenAI、Claude 都在做类似的东西
   - 如果我们的差异只是 thread summaries，很容易被吃掉

3. **Foundation 不扎实** — 缺乏长期任务/自主 agent 的闭环设计
   - 当前设计是 reactive（等消息来）
   - 缺少 Proposal → Mission → Steps 层级
   - 缺少 Trigger / Reaction 自主循环

---

## 外部参考（来自 Twitter 讨论）

### 1. Voxyz 闭环架构
> "Between 'agents can produce output' and 'agents can run things end-to-end,' there's a full execute → feedback → re-trigger loop missing."

**关键设计：**
- Proposal → Mission → Steps 任务层级
- Event Bus 追踪所有 agent 动作
- Trigger + Reaction Matrix 实现自主闭环
- Cap Gates 在入口控制配额
- 自愈机制（30min stuck → auto fail）
- Policy-driven 配置（不改代码）

### 2. KSimback 管理方法论
> "AI 的难点不是智能，是管理"

**关键设计：**
- SOUL.md — 每个 agent 的灵魂文件
- 4 级信任 — Observer → Advisor → Operator → Autonomous
- Performance Reviews — 定期评估，可升可降
- 三层记忆 — daily notes / long-term / project-specific

### 3. Yangyi IM 框架
> "任务驱动的群组最大的意义在于隔离上下文"

**关键洞察：**
- 人 + Agent 混合 IM 是未来交互界面
- 群组隔离上下文是 Multi-Agent 的开端
- 底层基于 IM 异步消息处理机制

### Session Runner 现状 vs 目标

| 维度 | Session Runner (现有) | 目标 (Voxyz-like) |
|------|----------------------|-------------------|
| 核心定位 | Claude Code session 容器 | Agent 协作系统 |
| 任务来源 | 只有 Message（被动响应） | 人 / Trigger / Reaction |
| 状态持久化 | Task 临时，执行完就没 | proposals/missions/steps 全持久化 |
| 自主发起 | ❌ Agent 只响应消息 | ✅ Agent 可以提 proposal |
| 闭环触发 | ❌ 无 | ✅ Event → Trigger → 自动创建新 Proposal |

---

## V2 设计目标

### 核心问题要回答

1. **Product Position** — 我们到底在做什么？
   - 不是 "Slack with AI summaries"（crowded market）
   - 应该是什么？需要找到 defensible differentiation

2. **Foundation** — 架构基础是什么？
   - 是否需要 Proposal/Mission/Steps 层级？
   - 是否需要 Event Bus + Trigger/Reaction？
   - 如何支持长时间自主任务？

3. **核心体验** — 用户的 aha moment 是什么？
   - Deep Dive with AI?
   - Autonomous Agent project management?
   - 或者完全不同的东西？

4. **竞争护城河** — 如何不被 OpenAI/Claude 吃掉？
   - 数据壁垒？
   - 行为壁垒？
   - 网络效应？

---

## Agent Team Review 任务

### 输入材料

| 文档 | 路径 | 内容 |
|------|------|------|
| **V1 Core** | `docs/PRODUCT-REASONING.md` | 原始产品推导 |
| **Core Reframe** | `docs/design/PRODUCT-CORE-REFRAME.md` | Fork → Deep Dive 概念修正 |
| **Pain Analysis** | `docs/design/slack-pain-ranking.md` | Slack 痛点分析 + 解决方案评估 |
| **External Ref** | `docs/design/AGENT-ORCHESTRATION-REFERENCE.md` | Voxyz/KSimback/Yangyi 架构参考 |
| **Research** | `docs/research/` | R1-R7 + SYNTHESIS |
| **Phase 1.5** | `docs/research/phase-1.5/` | 架构、UX、BDD 设计 |

### 需要回答的问题

**Product Strategy:**
1. 原始 thesis (AI cognitive amplification) vs 漂移后 thesis (conversation management) — 哪个更有价值？
2. "Deep Dive" 模型是否足够 defensible？还是需要更大的 reframe？
3. 如何避免成为 OpenAI/Claude 的附属品？

**Technical Foundation:**
1. 是否需要 Proposal → Mission → Steps 层级？还是 overkill？
2. 长时间任务（跨 session）如何支持？
3. Agent 自主性 vs Human oversight 的平衡？

**Market Fit:**
1. Slack 替代 vs AI workspace vs 完全不同的定位？
2. Dogfood (Vibe team 20人) 是否是正确的第一步？
3. Go-to-market 路径？

---

## 流程

1. **Phase 1: Review** — Agent team 审核现有文档，回答上述问题
2. **Phase 2: Feedback Integration** — Charles 提供方向性 feedback
3. **Phase 3: Synthesis** — 整合形成 V2 核心定位
4. **Phase 4: Draft V2 Design** — 产出新的设计文档

---

## Agent Team 分工

| Agent | 职责 |
|-------|------|
| **Product Strategist** | Review product position, market fit, competitive moat |
| **Tech Architect** | Review 技术架构, Voxyz-like 闭环可行性 |
| **UX Designer** | Review 用户体验, Deep Dive vs other models |
| **Business Analyst** | 商业分析, ROI, dogfood economics |
| **Synthesizer** | 整合所有 input, draft V2 vision |

---

## Feedback Queue

*等待 Charles input...*

### Charles 初始方向 (2026-02-08)

> "目前的根基不是很扎实...我希望整合这些最新的分析以及商业上的预测，能更加务实、扎实地找到一些 Solid 的点，让我们这个项目构建在一个更好的基础之上，而不是成为一个空中楼阁"

**关键 Concerns:**
- 不想被 OpenAI/Claude 吞掉
- 需要更 solid 的 foundation
- 参考 Voxyz/KSimback/Yangyi 的设计

---

*Last updated: 2026-02-08*
