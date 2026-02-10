# OpenVibe V2 Vision

> Created: 2026-02-09
> Status: ✅ Direction Confirmed
> Owner: Charles (@zurrix)

---

## 一句话定位

**OpenVibe = 让 Agent 融入公司组织的操作系统**

不是让 Agent 更聪明 (OpenAI/Claude 做这个)，
而是让 Agent 能被信任、被管理、像员工一样工作。

---

## 核心洞察

### OpenAI/Claude 做的：
- 让 Agent 更聪明
- 让 Agent 能做更多事

### OpenAI/Claude 不做的：
- Agent 怎么融入组织
- Agent 怎么和人协作
- Agent 怎么被信任和管理
- 多个 Agent 怎么协调
- 公司怎么 scale agent workforce

### OpenVibe 的护城河 = 组织层，不是智能层

---

## 愿景

**塑造新一代公司组织形态 — 人和 Agent 混合协作的公司**

| 旧世界 | 新世界 (OpenVibe) |
|--------|-------------------|
| 员工只有人 | 人 + Agent 混合 |
| 人的层级结构 | 人+Agent 的协作网络 |
| Manager 分配任务给人 | 系统分配任务给人或 Agent |
| 人做执行 | Agent 做执行，人 review |
| 知识在人脑/文档里 | Agent 有 memory，持续积累 |

---

## 核心体验

### 基础层: Trust & Governance
> "Agent 可以自主，但有边界和监督"

**Trust Level 体系：**
- **L1 Observer**: 只能建议，不能行动
- **L2 Advisor**: 可以做低风险操作 (读数据、写草稿)
- **L3 Operator**: 可以做中风险操作 (发内部消息、执行 assigned tasks)
- **L4 Autonomous**: 可以做高风险操作 (发外部邮件、花钱) — 仍有 guardrails

**关键机制：**
- Agent 在权限内 → 直接做
- Agent 超出权限 → 请求 approval
- 敏感操作 → 强制 human review
- 所有行为可追溯 (audit log + reasoning)

### 体验层: Agent as Employee
> "Agent 像员工一样有职责、汇报、考核"

**用户 mental model：**
```
1. "招聘" Agent
   - 给它角色 (Marketing Analyst)
   - 定义职责 (每周出 growth report)
   - 设置权限 (可读 Mixpanel，不能发邮件)

2. Agent 自主工作
   - 主动执行职责范围内的任务
   - 有发现主动汇报
   - 需要决策时来问你

3. 定期 Review
   - 看它做了什么 (audit log)
   - 给 feedback (调整行为)
   - 升降 trust level
```

**Aha moment:** 
> "这个 Agent 真的像个员工 — 我不用管它，它自己会做事，但我随时能看到它在做什么、为什么这么做。"

---

## 技术架构方向

基于 Voxyz 闭环架构 + KSimback 管理方法论：

### 核心组件

```
┌─────────────────────────────────────────────────────────────┐
│                    Organization Layer                        │
│   Agents, Roles, Permissions, Trust Levels, Audit Log       │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Orchestration Layer                       │
│   Proposal → Mission → Steps, Event Bus, Trigger/Reaction   │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    Execution Layer                           │
│   Agent Runtime (Claude/GPT), Tools (MCP), Memory           │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    State Layer                               │
│   Supabase (Postgres + Realtime), Policy Config             │
└─────────────────────────────────────────────────────────────┘
```

### 关键设计参考

| 来源 | 借鉴什么 |
|------|----------|
| **Voxyz** | Proposal → Mission → Steps, Event Bus, Trigger/Reaction, Cap Gates, 自愈机制 |
| **KSimback** | SOUL.md, 4 级 Trust Level, Performance Review, 三层记忆 |
| **Yangyi** | 任务驱动群组隔离上下文, IM 作为交互基础 |

---

## 战略定位

### 双轨策略

| | **OpenVibe** | **Vibe AI** |
|---|---|---|
| 性质 | 开源 | 商业化 |
| 定位 | Agent 组织层基础设施 | 基于 OpenVibe 的企业产品 |
| 目标 | 建立标准、社区、生态 | 赚钱、养公司 |

### 差异化

| 竞争者 | 他们做什么 | 我们做什么 |
|--------|-----------|-----------|
| **OpenAI/Claude** | Agent 智能 | Agent 治理 |
| **LangChain/CrewAI** | Agent 开发框架 | Agent 组织框架 |
| **Slack/Teams** | 人的协作 | 人+Agent 协作 |

### 为什么不会被吃掉

1. **OpenAI/Claude 不做组织层** — 他们做通用能力，不做企业治理
2. **企业需要治理** — Trust, Permission, Audit, Compliance
3. **开源建立标准** — 社区 + 生态 > 一家公司

---

## 品牌方向

**候选名字：**
- OpenVibe (开源感强)
- The Vibe Company (新型公司形态)

**可用域名：**
- thevibecompany.ai ✅ (可注册)

**品牌关系：**
- Vibe (母品牌)
- Vibe AI (商业产品)
- OpenVibe / The Vibe Company (开源框架)

---

## 路径

### Phase 1: Internal Dogfood (Q1-Q2 2026)
- 给 Vibe team 用
- 验证核心体验
- 快速迭代

### Phase 2: Open Source Prep (Q3 2026)
- 清理代码、文档
- 建立 GitHub 仓库
- 准备 launch

### Phase 3: Public Launch (Q4 2026)
- 开源发布
- 社区运营
- Vibe AI 基于此商业化

---

## 与 V1 的关系

### V1 概念 (已归档)
- Fork/Resolve → Deep Dive
- Slack 替代
- Team collaboration with AI

### V2 方向 (确认)
- Agent 融入组织
- Trust & Governance
- Agent as Employee

### 保留什么
- 技术调研 (R1-R7) 仍有参考价值
- Supabase + 技术栈选择仍适用
- 部分 UX 思考可复用

### 放弃什么
- "替代 Slack" 的定位
- "Deep Dive" 作为核心体验
- Fork/Resolve 交互模型

---

## Next Steps for Claude Code

1. **Review 此文档** — 理解 V2 方向
2. **归档 V1 docs** — 移动到 `docs/archive/v1/`
3. **创建 V2 结构** — 新的 docs 目录结构
4. **开始设计** — 从 Organization Layer 开始

### 关键设计问题

1. **Agent 定义模型** — Agent 的 SOUL.md 结构是什么？
2. **Trust Level 机制** — 具体怎么实现升降级？
3. **Audit Log 设计** — 记录什么？怎么展示？
4. **权限系统** — 和现有 RBAC 怎么结合？
5. **任务流转** — Proposal → Mission → Steps 的具体实现

---

*Confirmed: 2026-02-09 01:01 MST*
*Based on: Discord #OpenVibe Redesign discussion*
