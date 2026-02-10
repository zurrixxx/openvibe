# Autonomous Project Agent: Build vs Configure Decision

> 核心需求：Agent 能够长时间自主推进项目，只在需要时找人

## 问题定义

### 用户故事
作为一个忙碌的 CEO，我希望：
- 把一个项目交给 agent 后，它能自己推进
- 不需要我每次 prompt 才动
- 遇到需要我决策的点才来找我
- 跨越多天/多周持续工作

### 核心能力需求

| 能力 | 描述 | 重要性 |
|------|------|--------|
| **Task Decomposition** | 把大目标拆成可执行的步骤 | 🔴 必须 |
| **State Persistence** | 记住做到哪了，下次继续 | 🔴 必须 |
| **Autonomous Execution** | 自己决定下一步做什么 | 🔴 必须 |
| **Escalation Policy** | 知道什么时候该找人 | 🔴 必须 |
| **Progress Visibility** | 让人能看到进度 | 🟡 重要 |
| **Multi-agent Coordination** | 多个 agent 协作 | 🟢 可选 |

---

## 方案一：轻量版 (OpenClaw-native)

### 架构
```
OpenClaw
├── cron job (每 30min 或按需)
│   └── "Check PROJECT-STATE.md, execute next step"
├── HEARTBEAT.md
│   └── Project check-in logic
├── PROJECT-STATE.md
│   └── Structured task state
└── memory/
    └── Daily execution logs
```

### 实现方式

**1. PROJECT-STATE.md 结构**
```markdown
# Project: [Name]

## Goal
[最终目标]

## Current Phase
[当前阶段]

## Tasks
- [x] Task 1 - completed 2026-02-08
- [ ] Task 2 - in progress
  - Status: waiting for API response
  - Blocker: none
  - Next action: check response, then process
- [ ] Task 3 - blocked
  - Blocker: needs human decision on X

## Escalation Log
- 2026-02-08: Asked human about X, waiting response

## Decision Needed
[如果有需要人决策的，写在这里]
```

**2. Cron Job 配置**
```yaml
schedule:
  kind: every
  everyMs: 1800000  # 30 min
payload:
  kind: agentTurn
  message: |
    Read PROJECT-STATE.md. 
    If there's a task in progress with no blocker, execute next action.
    If blocked on human decision, check if they responded.
    If task complete, move to next task.
    Update PROJECT-STATE.md with progress.
    If you need human input, send message to main session.
sessionTarget: isolated
```

**3. Escalation 规则 (写在 AGENTS.md 或 SOUL.md)**
```markdown
## Escalation Policy
找人的情况：
- 需要花钱 > $100
- 需要发外部消息 (email, social)
- 遇到技术 blocker 超过 2 次尝试
- 任务定义不清晰
- 完成重要 milestone

不用找人：
- 读文件、写代码、本地测试
- 更新文档
- 常规进度推进
```

### 优点
- ✅ **零开发成本** — 纯配置
- ✅ **立即可用** — 今天就能跑起来
- ✅ **灵活** — 随时改规则
- ✅ **透明** — 所有状态都是 markdown，人能直接读改

### 缺点
- ❌ **无 DAG** — 任务依赖靠人工维护
- ❌ **无并行** — 一次只能推进一个任务
- ❌ **状态简陋** — 没有正式的状态机
- ❌ **无 UI** — 只能看文件
- ❌ **Scaling 难** — 多项目管理会乱

### 适用场景
- 单个项目、线性流程
- 想快速验证这个模式是否有用
- 不想写代码

---

## 方案二：重量版 (Openvibe Platform)

### 架构
```
┌─────────────────────────────────────────────┐
│                 Openvibe                     │
├─────────────────────────────────────────────┤
│  Control Plane (Vercel/Supabase)            │
│  ├── Project Dashboard                       │
│  ├── Task Graph (DAG)                        │
│  ├── Approval Queue                          │
│  └── Agent Registry                          │
├─────────────────────────────────────────────┤
│  Execution Plane (VPS/OpenClaw)             │
│  ├── Agent Workers                           │
│  ├── Task Executor                           │
│  └── Event Bus                               │
├─────────────────────────────────────────────┤
│  Data Layer (Supabase)                       │
│  ├── projects                                │
│  ├── tasks (with dependencies)               │
│  ├── task_runs                               │
│  ├── agent_events                            │
│  └── escalations                             │
└─────────────────────────────────────────────┘
```

### 核心数据模型

```sql
-- 项目
CREATE TABLE projects (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  goal TEXT,
  status TEXT DEFAULT 'active', -- active, paused, completed
  config JSONB, -- escalation policy, etc
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 任务 (支持 DAG)
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  project_id UUID REFERENCES projects(id),
  title TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'pending', -- pending, ready, running, blocked, completed, failed
  depends_on UUID[], -- 依赖的 task ids
  assigned_agent TEXT,
  result JSONB,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ
);

-- 任务执行记录
CREATE TABLE task_runs (
  id UUID PRIMARY KEY,
  task_id UUID REFERENCES tasks(id),
  agent_id TEXT,
  status TEXT, -- running, success, failed, escalated
  logs TEXT,
  started_at TIMESTAMPTZ DEFAULT NOW(),
  ended_at TIMESTAMPTZ
);

-- 需要人工处理的升级
CREATE TABLE escalations (
  id UUID PRIMARY KEY,
  task_id UUID REFERENCES tasks(id),
  reason TEXT,
  context JSONB,
  status TEXT DEFAULT 'pending', -- pending, resolved, dismissed
  human_response TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  resolved_at TIMESTAMPTZ
);
```

### 核心功能

**1. Task Graph (DAG)**
- 任务有依赖关系
- 自动计算哪些任务 ready to run
- 支持并行执行无依赖的任务

**2. Intelligent Scheduler**
```
每次调度:
1. 找出所有 status=ready 的任务
2. 按优先级排序
3. 分配给可用的 agent
4. 监控执行，处理超时/失败
```

**3. Escalation System**
- Agent 遇到问题 → 创建 escalation
- 通知人类 (Discord/Telegram/etc)
- 人类回复 → 更新 escalation → 任务继续

**4. Dashboard**
- 项目总览
- 任务依赖图可视化
- Escalation queue
- Agent 活动日志

### 优点
- ✅ **真正的 DAG** — 复杂依赖关系
- ✅ **并行执行** — 多任务同时跑
- ✅ **可视化** — 看得到全局
- ✅ **Scalable** — 多项目、多 agent
- ✅ **审计追踪** — 完整历史记录
- ✅ **可作为产品** — 其他人也能用

### 缺点
- ❌ **开发成本** — 需要建 infra
- ❌ **维护成本** — 又一个系统要管
- ❌ **过度工程风险** — 可能需求没那么复杂
- ❌ **Time to value** — 几周后才能用

### 适用场景
- 多个复杂项目并行
- 需要多 agent 协作
- 想把这个做成产品
- 已验证轻量版不够用

---

## 对比总结

| 维度 | 轻量版 | 重量版 |
|------|--------|--------|
| **开发时间** | 0 (今天就能用) | 2-4 周 |
| **复杂度** | 低 | 高 |
| **Task 依赖** | 手动管理 | DAG 自动 |
| **并行能力** | ❌ | ✅ |
| **可视化** | 看文件 | Dashboard |
| **多项目** | 难 | 容易 |
| **产品化** | ❌ | ✅ |
| **灵活性** | 很高 | 中等 |
| **适合阶段** | 验证想法 | 规模化 |

---

## 建议路径

### Phase 1: 验证 (1-2 周)
用**轻量版**跑一个真实项目：
1. 选一个实际项目
2. 配置 PROJECT-STATE.md + cron
3. 观察：
   - Agent 能自己推进多少？
   - 什么时候需要找你？
   - 状态追踪够用吗？
   - 遇到什么问题？

### Phase 2: 决策
根据 Phase 1 的结果：

**如果轻量版够用** → 继续用，不建 openvibe
- 可能只需要优化 escalation 规则
- 或者加个简单的状态查看页面

**如果发现明确痛点** → 建 openvibe，但只建需要的部分
- 比如只需要 DAG？只建 task graph
- 只需要 escalation queue？只建那个

### Phase 3: 产品化 (可选)
如果验证后发现：
- 自己用得很顺
- 别人也有这个痛点
- 愿意付费

→ 才考虑做成产品

---

## 下一步行动

**立即可做：**
1. 选一个项目来试轻量版
2. 创建 PROJECT-STATE.md 模板
3. 配置 cron job
4. 跑 1-2 周看效果

**等验证后再决定：**
- 是否建 openvibe
- 建哪些功能
- 用什么技术栈

---

*Created: 2026-02-08*
*Status: Decision pending - recommend Phase 1 validation first*
