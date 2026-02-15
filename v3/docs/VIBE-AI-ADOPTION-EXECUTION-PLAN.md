# Vibe AI Adoption 执行计划

> Date: 2026-02-14
> Status: Draft
> Goal: 用 AI agents 实现 GTM 10-25x 提升

---

## 架构决策

### 三层架构

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1: Scheduler (Temporal)                          │
│  - Durable execution, 跨天/周任务不丢状态                 │
│  - 自动重试, timeout 处理                                │
│  - Dashboard 可视化                                      │
└─────────────────────┬───────────────────────────────────┘
                      │ 触发
                      ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 2: Workflow Engine (LangGraph)                   │
│  - 状态机 + checkpoint                                   │
│  - 循环、分支、条件判断                                   │
│  - Human-in-the-loop (暂停等确认)                        │
│  - 错误恢复、重试路径                                     │
└─────────────────────┬───────────────────────────────────┘
                      │ 执行
                      ▼
┌─────────────────────────────────────────────────────────┐
│  Layer 3: Agent Roles (CrewAI)                          │
│  - 角色定义 (role, goal, backstory)                      │
│  - 工具绑定 (CRM API, Usage API, etc.)                   │
│  - 团队协作 (delegation, shared context)                 │
└─────────────────────────────────────────────────────────┘
```

### 技术选型

| 组件 | 选择 | 原因 |
|------|------|------|
| **Scheduler** | Temporal | Durable execution, 生产级, OpenAI/Stripe 都在用 |
| **Workflow Engine** | LangGraph | 状态持久化, HITL, LangChain 生态 |
| **Agent Framework** | CrewAI | 快速定义角色, 上手成本低 |
| **LLM** | Claude API | 推理能力强, 长上下文 |
| **Observability** | LangSmith | LangGraph 原生集成, 必须有 |

---

## Phase 0: 基础设施 (Week 1-2)

### 目标
搭建三层架构基础，验证可行性

### 任务清单

| # | 任务 | Owner | 产出 | 完成标准 |
|---|------|-------|------|----------|
| 0.1 | Temporal 环境搭建 | Infra | Temporal Cloud 或 self-hosted | Worker 能跑 hello world |
| 0.2 | LangGraph 项目初始化 | AI | Python 项目 + checkpointer | 能持久化状态到 Postgres |
| 0.3 | CrewAI 集成 | AI | CrewAI as LangGraph node | crew.kickoff() 在 graph 内执行 |
| 0.4 | LangSmith 开通 | AI | Tracing 配置完成 | 能看到每步 LLM 调用 |
| 0.5 | 基础 API 集成 | Eng | HubSpot/CRM wrapper | 能拉 leads, contacts |

### 验收
- [ ] Temporal workflow 触发 → LangGraph 执行 → CrewAI agent 完成任务 → 状态持久化
- [ ] 整个链路在 LangSmith 可观测

---

## Phase 1: 单 Agent 验证 (Week 3-4)

### 选择验证对象: Lead Qualification Agent

**为什么选它:**
- 短反馈循环 (lead 进来 → 几分钟出结果)
- 容易量化 (qualification rate)
- 不需要长时持久化 (验证核心架构够用)

### Agent 定义

```python
# CrewAI Agent
lead_qualification_agent = Agent(
    role="Lead Qualification Specialist",
    goal="快速准确地评估每个 lead 的质量和意向",
    backstory="你是 Vibe 的资深销售，能从有限信息判断 lead 价值",
    tools=[
        hubspot_enrichment_tool,
        company_research_tool,
        scoring_model_tool
    ]
)
```

### Workflow (LangGraph)

```
Lead 进入
    ↓
[Node 1] 数据 enrichment (公司、角色、tech stack)
    ↓
[Node 2] CrewAI agent 评估 (fit + intent + urgency)
    ↓
[Node 3] 打分 (0-100)
    ↓
[Conditional] 
    ├── Score >= 80 → 路由到 Sales (高优)
    ├── Score 50-79 → 进入 Nurture 序列
    └── Score < 50 → 发教育内容
    ↓
[Node 4] 更新 CRM + 记录
```

### 成功指标

| 指标 | Baseline | Target (Week 4) |
|------|----------|-----------------|
| Qualification 准确率 | 人工 benchmark | >= 85% 一致 |
| 处理时间 | - | < 2 分钟/lead |
| 覆盖率 | 20% (人工跟不上) | 100% |

---

## Phase 2: Marketing Agents (Week 5-8)

### Agent 矩阵

| Agent | 任务类型 | 架构 |
|-------|----------|------|
| **Segment Research** | 一次性 | CrewAI only |
| **Content Generation** | 一次性 | CrewAI only |
| **Content Repurposing** | 一次性 | CrewAI only |
| **Campaign Agent** | 长期循环 | LangGraph + CrewAI |
| **SEO Agent** | 定时 | Temporal + CrewAI |

### Week 5-6: Content Pipeline

```
[Temporal: 每周一 9am]
    ↓
[LangGraph Workflow]
    ├── Node 1: Segment Research Agent → 识别本周重点 segments
    ├── Node 2: Content Generation Agent → 每 segment 2 篇
    ├── Node 3: Content Repurposing Agent → 每篇 → 10 formats
    └── Node 4: 发布队列 + 排期
    ↓
[Output] 200 content pieces 排期完成
```

### Week 7-8: Campaign Automation

```
[Temporal: Campaign 启动]
    ↓
[LangGraph Workflow - 循环]
    ├── Node 1: 设计 campaign (CrewAI)
    ├── Node 2: 执行投放
    ├── Node 3: 等待 48h 数据
    ├── Node 4: 分析效果 (CrewAI)
    ├── Node 5: A/B 决策
    │   ├── 继续优化 → 回到 Node 2
    │   └── 收敛/timeout → 结束
    └── [Checkpoint] 每轮状态持久化
```

### 成功指标

| 指标 | Baseline | Target (Week 8) |
|------|----------|-----------------|
| Content volume | 2/week | 20/week (10x) |
| Segments covered | 1 | 10 |
| Campaigns parallel | 1 | 5 |

---

## Phase 3: Sales Agents (Week 9-12)

### Agent 矩阵

| Agent | 任务类型 | 架构 |
|-------|----------|------|
| **Outbound Follow-up** | 触发式 | LangGraph (多 touch sequence) |
| **Prospect Research** | 一次性 | CrewAI only |
| **Proposal Agent** | 一次性 | CrewAI only |
| **Nurture Agent** | 长期 | Temporal + LangGraph |
| **CRM Agent** | 持续 | Temporal (daily sync) |

### Nurture Workflow (复杂长任务示例)

```
[Temporal: Lead 进入 nurture]
    ↓
[LangGraph Workflow]
    Day 1:
        ├── 发 welcome email (personalized)
        └── [Checkpoint] 等待 engagement
    
    Day 3:
        ├── 检查 engagement
        ├── if opened → 发 case study
        └── if not → 换 subject line 重发
        └── [Checkpoint]
    
    Day 7:
        ├── 检查累计 engagement
        ├── if high → 升级到 Sales
        └── if low → 继续 nurture
        └── [Checkpoint]
    
    Day 14:
        ├── Final push
        └── if no response → 移到 long-term nurture
    
    [Human-in-the-loop]
        - 任何时候 lead 回复 → 暂停 workflow
        - 等 Sales 确认 → 恢复或转人工
```

### 成功指标

| 指标 | Baseline | Target (Week 12) |
|------|----------|------------------|
| Follow-up rate | 20% | 100% |
| Sales prep time | 1 hour | 5 min |
| Proposal time | 2 hours | 15 min |
| Nurture → SQL rate | 5% | 15% |

---

## Phase 4: CS Agents (Week 13-16)

### 核心: Health Monitoring System

```
[Temporal: Daily 2am]
    ↓
[LangGraph Workflow]
    ├── Node 1: 拉取所有客户 usage 数据
    ├── Node 2: 计算 health score (CrewAI Analyst Agent)
    ├── Node 3: 对比历史趋势
    ├── [Conditional] For each at-risk customer:
    │   ├── Score drop > 20% → Alert CS lead (Slack)
    │   ├── Score < 50 → Proactive outreach (auto email)
    │   └── Score < 30 → Escalate (human required)
    │   └── [Checkpoint] 等待人工确认
    └── Node 4: 更新 dashboard + 记录
```

### 成功指标

| 指标 | Baseline | Target (Week 16) |
|------|----------|------------------|
| Customer capacity | 100 | 500 |
| Churn prediction | 0 days | 30 days advance |
| Response time | 24h | 1h |

---

## 团队 & 资源

### 核心团队

| 角色 | 人数 | 职责 |
|------|------|------|
| AI Orchestrator | 1 | 架构设计, agent 调优, LangGraph 开发 |
| Backend Eng | 1 | Temporal, API 集成, 数据管道 |
| Marketing Lead | 1 | 验证 marketing agents 效果 |
| Sales Lead | 1 | 验证 sales agents 效果 |

### 基础设施成本 (月)

| 项目 | 成本 |
|------|------|
| Temporal Cloud | $200-500 |
| Claude API | $2,000-5,000 |
| LangSmith | $400 |
| 数据存储 | $100 |
| **Total** | **$3,000-6,000/月** |

---

## 风险 & 缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| Agent 输出质量差 | 高 | 先人工 review 所有输出 1-2 周 |
| LLM 成本失控 | 中 | 设置 budget alert, 优化 prompt |
| 架构过度复杂 | 中 | 先验证单 agent, 再扩展 |
| 团队学习曲线 | 中 | 预留 2 周 ramp up |

---

## Decision Points

### Week 4 (Phase 1 完成)
- Lead Qualification 准确率 >= 85%? 
  - ✅ → 继续 Phase 2
  - ❌ → 迭代 agent, 暂停扩展

### Week 8 (Phase 2 完成)
- Content 10x? Campaigns 5x parallel?
  - ✅ → 继续 Phase 3
  - ❌ → 分析瓶颈, 调整

### Week 12 (Phase 3 完成)
- Follow-up 100%? Qualified leads 显著提升?
  - ✅ → 继续 Phase 4
  - ❌ → 重新评估 ROI

---

## 立即行动 (Week 1)

### Day 1-2
- [ ] 确认 Temporal Cloud vs self-hosted
- [ ] 开通 LangSmith
- [ ] 初始化 Python 项目 (LangGraph + CrewAI)

### Day 3-4
- [ ] HubSpot API 集成
- [ ] 第一个 CrewAI agent 跑通

### Day 5
- [ ] Temporal → LangGraph → CrewAI 全链路验证
- [ ] 文档化架构决策

---

*Ready to start?*
