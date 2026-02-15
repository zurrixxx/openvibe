# OpenVibe V2: Resources & Budget

> **Agent**: Resource Planning Agent
> **Created**: 2026-02-10
> **Status**: Draft
> **Prerequisites**: Read `THESIS.md` and `STRATEGY.md`

---

## Executive Summary

**Team Size**: 12 (Month 6) → 23 (Month 12) → 38 (Month 18)
**6-Month Burn**: $1.89M
**18-Month Total**: $8.52M
**Funding Need**: $10-12M (Seed/Series A) for 24-30 months runway

**Key Insight**: Partner-led GTM model requires front-loading Partner Success team (40% of GTM headcount by Month 12) while maintaining lean engineering (8-10 engineers sufficient through GA with monolith architecture). The moat is distribution speed, not feature depth.

---

## 1. Team Structure

### 1.1 Month 6 Org Chart (GA Launch)

**Total Headcount**: 12

```
CEO (existing)
│
├─ CTO / VP Engineering (1)
│  ├─ Engineering Manager (1)
│  │  ├─ Full-stack Engineers (4)
│  │  └─ Backend Engineer (1)
│  ├─ Product Manager (1)
│  └─ Product Designer (1)
│
├─ Head of Partner Success (1)
│  └─ Partner Success Managers (2)
│
└─ Operations (part-time/fractional)
```

**By Function**:
- **Engineering & Product**: 8 (67%)
  - Engineering Manager: 1
  - Full-stack Engineers: 4
  - Backend Engineer: 1
  - Product Manager: 1
  - Product Designer: 1
- **Go-to-Market**: 3 (25%)
  - Head of Partner Success: 1
  - Partner Success Managers: 2
- **Operations**: 1 (8%)
  - Fractional COO/Ops Manager

**Rationale**:
- **Engineering sizing**: 5-6 engineers is optimal for monolith through GA ([Binary Republik](https://blog.binaryrepublik.com/2026/02/modular-monolith-vs-microservices.html), [Software Seni](https://www.softwareseni.com/what-is-a-modular-monolith-and-how-does-it-combine-the-best-of-both-architectural-worlds/)). Teams <8 developers should build monoliths, not microservices. Architecture: packages/core + apps/web + apps/board.
- **Partner Success**: 2 PSMs can support 10-20 partners in co-development phase (Alpha/Beta). Each PSM supports 5-10 active partners during onboarding-heavy period.
- **Lean ops**: Fractional support for finance, HR, legal until Month 12.

### 1.2 Month 12 Org Chart (Scale Phase)

**Total Headcount**: 23

```
CEO
│
├─ CTO / VP Engineering (1)
│  ├─ Engineering Manager (1)
│  │  ├─ Full-stack Engineers (5)
│  │  ├─ Backend Engineers (2)
│  │  └─ Mobile/Board Engineer (1)
│  ├─ Product Manager (1)
│  └─ Product Designer (1)
│
├─ VP GTM (1)
│  ├─ Head of Partner Success (1)
│  │  └─ Partner Success Managers (6)
│  ├─ Marketing Lead (1)
│  └─ Sales Rep (Direct) (1)
│
└─ Operations Manager (1)
   ├─ Customer Support (1)
   └─ Finance/HR (fractional)
```

**By Function**:
- **Engineering & Product**: 11 (48%)
- **Go-to-Market**: 10 (43%)
  - Partner Success: 7 (Head + 6 PSMs)
  - Marketing: 1
  - Direct Sales: 1
  - VP GTM: 1
- **Operations**: 2 (9%)

**Rationale**:
- **Engineering**: +2 engineers (7→9) to support board firmware, connectors, and mobile web. Still monolith-appropriate (<10 engineers).
- **Partner Success**: 6 PSMs to support 40-60 partners (10 partners per PSM during active onboarding, scaling to 15-20 post-launch). Based on CSM benchmarks: Mid-market CSMs manage 100-250 customers ([Vitally](https://www.vitally.io/post/what-is-the-golden-ratio-of-customer-success-managers-to-customers)). PSMs manage fewer partners but higher complexity.
- **Marketing**: Needed by Month 6-7 to support partner recruitment (content, events, website).

### 1.3 Month 18 Org Chart (Maturity Phase)

**Total Headcount**: 38

```
CEO
│
├─ CTO / VP Engineering (1)
│  ├─ Engineering Manager, Core (1)
│  │  ├─ Full-stack Engineers (6)
│  │  └─ Backend Engineers (2)
│  ├─ Engineering Manager, Platform (1)
│  │  ├─ Infrastructure Engineer (1)
│  │  └─ ML/AI Engineer (1)
│  ├─ Product Manager, Core (1)
│  ├─ Product Manager, Board (1)
│  └─ Product Designer (2)
│
├─ VP GTM (1)
│  ├─ Director of Partner Success (1)
│  │  └─ Partner Success Managers (12)
│  ├─ Marketing Manager (1)
│  │  └─ Content/Events (2)
│  └─ Sales Manager (1)
│     └─ Sales Reps (2)
│
└─ COO (1)
   ├─ Customer Support (3)
   └─ Finance/HR (2)
```

**By Function**:
- **Engineering & Product**: 17 (45%)
- **Go-to-Market**: 17 (45%)
  - Partner Success: 13 (Director + 12 PSMs)
  - Marketing: 3
  - Direct Sales: 3
  - VP GTM: 1
- **Operations**: 4 (10%)

**Rationale**:
- **Engineering**: 10-12 engineers at upper bound for monolith. Approaching inflection point where modular architecture becomes valuable. Two eng managers reflect team size (5-6 reports each).
- **Partner Success**: 12 PSMs to support 120 partners (10 partners per PSM). At 120 partners × 50 avg deployments = 6,000 end customers. Benchmark: Consulting firms serve 20-200 clients each ([Strategy doc](./STRATEGY.md)).
- **Operations**: Full-time COO + support staff to handle growth operations (finance, HR, compliance).

**Key Hiring Milestones**:
- Month 6: Core team in place (12)
- Month 12: Partner Success team scaled 3x (6 PSMs), GTM org formed
- Month 18: Dual eng managers, mature GTM, ops professionalized

---

## 2. Key Role Definitions

### 2.1 Engineering Manager

**Why Critical**: Lead 7 sprints (24 weeks) to GA. Own technical architecture decisions (monolith vs microservices), sprint planning, and team velocity.

**Responsibilities**:
- Sprint planning and execution (2-week sprints)
- Technical architecture decisions (packages/core, apps/web, apps/board)
- Engineering allocation enforcement (70% core/web, 20% board, 10% connectors)
- Hiring and team growth (hire 3-4 engineers by Month 6)
- Stakeholder communication (weekly progress to CEO/CTO)

**When to Hire**: Month 0 (immediately)

**Profile**:
- 5-8 years engineering experience, 2+ years management
- Experience with AI products (LLM integration, agent frameworks)
- Monolith → microservices migration experience
- Next.js, tRPC, Supabase, PostgreSQL
- Comfortable with small teams (3-8 engineers)

**Comp Range**: $180,000 - $210,000 base + 0.5-1.0% equity
*Benchmark*: [Wellfound](https://wellfound.com/hiring-data/r/engineering-manager-1/i/saas) reports $196K avg for SaaS startups, range $150K-$316K.

---

### 2.2 Full-Stack Engineer (4-6 hires)

**Why Critical**: Build core product (web workspace, agents, integrations). 70% of engineering time on core/web.

**Responsibilities**:
- Build web workspace (Next.js frontend, tRPC API, Supabase backend)
- Implement agent system (SOUL, trust levels, memory)
- Integrate LLM providers (Claude, GPT, Gemini)
- Build feedback system and progressive disclosure UI
- Write tests and maintain quality (test-first for bugs per [Code Quality Rules](../../@apos/rules/code-quality.md))

**When to Hire**: Month 0-4 (stagger 4 hires over 4 months)

**Profile**:
- 3-6 years full-stack experience
- Next.js, TypeScript, React, PostgreSQL
- LLM/AI product experience (preferred but not required)
- Comfortable with ambiguity and rapid iteration
- Strong product sense (shipping features, not just code)

**Comp Range**: $120,000 - $150,000 base + 0.2-0.5% equity
*Benchmark*: [Glassdoor](https://www.glassdoor.com/Salaries/full-stack-engineer-salary-SRCH_KO0,19.htm) reports $126K avg, range $96K-$168K. [Wellfound](https://wellfound.com/hiring-data/r/developer/i/saas) SaaS startup avg $128K.

---

### 2.3 Backend Engineer (1-2 hires)

**Why Critical**: Own database schema, API architecture, and performance as system scales.

**Responsibilities**:
- Design database schema (conversations, agents, memory, knowledge)
- Optimize query performance (PostgreSQL, indexing)
- Build APIs for external integrations (Slack, GitHub, etc.)
- Implement caching and performance optimization
- Own monitoring and observability (logs, metrics, alerting)

**When to Hire**: Month 4 (after product-market fit signals)

**Profile**:
- 4-7 years backend experience
- PostgreSQL, database design, API architecture
- Performance optimization and scaling
- Real-time systems (WebSockets, server-sent events)
- DevOps familiarity (deployment, monitoring)

**Comp Range**: $140,000 - $180,000 base + 0.3-0.6% equity
*Benchmark*: [Glassdoor](https://www.glassdoor.com/Salaries/backend-engineer-salary-SRCH_KO0,16.htm) reports $174K avg. [Wellfound](https://wellfound.com/hiring-data/r/backend-developer) reports $146K avg for startups.

---

### 2.4 Product Manager

**Why Critical**: Define roadmap, prioritize features, conduct user research during Alpha/Beta. Product manager-to-engineer ratio of 1:6-8 is standard ([Sharebird](https://sharebird.com/h/product-management/q/what-is-the-right-pm-to-eng-ratio-im-the-first-pm-and-we-have-8-engineers-and-1-designer)).

**Responsibilities**:
- Define 7-sprint roadmap (Sprint 2-7 features)
- Write specs and acceptance criteria
- Conduct user research (dogfood team, Alpha partners)
- Prioritize backlog and manage tradeoffs
- Own success metrics (acceptance rate, @mentions/day, dive publish rate)

**When to Hire**: Month 1-2

**Profile**:
- 4-7 years product management in B2B SaaS
- AI product experience (understanding LLM limitations, prompt design)
- Technical background (can read code, understand architecture)
- User research and interview skills
- Data-driven (comfortable with SQL, metrics dashboards)

**Comp Range**: $150,000 - $180,000 base + 0.4-0.8% equity
*Benchmark*: [Wellfound](https://wellfound.com/hiring-data/r/product_manager/i/saas) reports $167K avg for SaaS startups, range $80K-$253K.

---

### 2.5 Product Designer

**Why Critical**: Visual direction needed (PROGRESS.md open question #2). Own UI/UX for agent messages, progressive disclosure, and board interface.

**Responsibilities**:
- Design agent message styling (headline/summary/full)
- Design progressive disclosure UI
- Build design system (components, patterns, guidelines)
- Design board interface (meeting summary, @mention, agent cards)
- User testing and iteration

**When to Hire**: Month 0-1 (early for visual direction)

**Profile**:
- 3-5 years product design in SaaS
- AI/conversational UI experience (preferred)
- Strong interaction design skills
- Figma, prototyping, design systems
- Can code basic HTML/CSS (design-to-code handoff)

**Comp Range**: $90,000 - $130,000 base + 0.2-0.5% equity
*Benchmark*: [Wellfound](https://wellfound.com/hiring-data/r/ui-ux-designer/i/saas) reports $85K avg for SaaS startups, range $1K-$225K. [UI UX Jobs Board](https://uiuxjobsboard.com/salary/product-designer) reports $90K-$130K for product designers.

---

### 2.6 Head of Partner Success

**Why Critical**: Partner GTM is the strategy. Owns partner recruitment, enablement, and success. Must be hired before Beta (Month 3-5) to enable partners.

**Responsibilities**:
- Build partner program (tier structure, benefits, pricing)
- Recruit first 10 partners (consulting firms, existing Vibe relationships)
- Design partner enablement (training, certification, playbooks)
- Own partner success metrics (deployments per partner, time to first deployment)
- Build PSM team (hire and manage 6-12 PSMs)

**When to Hire**: Month 2-3 (before Beta)

**Profile**:
- 6-10 years channel/partner sales experience
- B2B2B experience (selling through partners to end customers)
- Consultative selling (partner is buyer and user)
- Relationship-driven (building trust with partners)
- SaaS/tech industry experience

**Comp Range**: $150,000 - $180,000 base + 0.6-1.2% equity
*Benchmark*: Head of Partner Success (director level). Estimated as Partner Manager + 30-40% for director level. [Glassdoor](https://www.glassdoor.com/Salaries/partner-manager-salary-SRCH_KO0,15.htm) reports Partner Manager avg $157K.

---

### 2.7 Partner Success Manager (6-12 hires)

**Why Critical**: Scale partner network (target 120 partners by Month 18). Each PSM supports 10-15 partners through onboarding and first client deployments.

**Responsibilities**:
- Onboard new partners (training, certification)
- Support first 5 client deployments per partner (hands-on)
- Conduct quarterly business reviews (QBRs)
- Share best practices across partners
- Identify expansion opportunities (upsell, new verticals)

**When to Hire**: Month 3-18 (2 in Month 3-5, +4 in Month 6-12, +6 in Month 13-18)

**Profile**:
- 3-5 years customer success or partner management
- Technical enough to demo product and troubleshoot
- B2B SaaS experience
- Consultative approach (partner advisor, not just support)
- Comfortable with ambiguity (program is new)

**Comp Range**: $85,000 - $120,000 base + 0.1-0.3% equity
*Benchmark*: [Glassdoor](https://www.glassdoor.com/Salaries/partner-success-manager-salary-SRCH_KO0,23.htm) reports $149K avg, range $117K-$195K. Lower end for early-stage PSMs, higher end for senior PSMs managing more partners.

**Capacity Planning**:
- **Onboarding phase** (Month 3-12): 10 partners per PSM (high-touch, co-development)
- **Scale phase** (Month 13-18): 15-20 partners per PSM (post-onboarding support)
- **Benchmark**: CSMs manage 10-25 customers in Enterprise ([Vitally](https://www.vitally.io/post/what-is-the-golden-ratio-of-customer-success-managers-to-customers)), $2-5M ARR per CSM ([Tomasz Tunguz](https://tomtunguz.com/how-much-arr-can-a-csm-manage/)). PSMs manage fewer partners but higher complexity (each partner = 20-200 end customers).

---

### 2.8 Marketing Lead

**Why Critical**: Partner recruitment requires marketing (content, events, website). Needed by Month 6-7 as partner recruitment scales.

**Responsibilities**:
- Partner recruitment marketing (content, SEO, ads)
- Event strategy (conferences, webinars)
- Website and brand (messaging, positioning)
- Content creation (case studies, blog, whitepapers)
- Lead generation for direct sales (secondary)

**When to Hire**: Month 6-7

**Profile**:
- 4-6 years B2B SaaS marketing
- Partner/channel marketing experience (preferred)
- Content marketing skills (writing, editing)
- Event planning and execution
- Comfortable wearing multiple hats (early-stage)

**Comp Range**: $110,000 - $140,000 base + 0.2-0.5% equity
*Benchmark*: Marketing Lead (manager level) in SaaS startup. Estimated from industry benchmarks.

---

### 2.9 VP GTM (Month 10-12)

**Why Critical**: Unify partner success, marketing, and direct sales as GTM org scales (10+ headcount).

**Responsibilities**:
- Own GTM strategy and execution
- Manage Head of Partner Success, Marketing Lead, Sales Manager
- Partner with CEO on fundraising and investor relations
- Own revenue targets and forecasting
- Build GTM playbooks and processes

**When to Hire**: Month 10-12 (once GTM team is 8-10 people)

**Profile**:
- 10+ years B2B SaaS GTM experience
- VP or Director level at previous company
- Partner-led GTM experience (preferred)
- Revenue leadership ($5M-$20M ARR scale)
- Strong executive presence (board presentations, investor meetings)

**Comp Range**: $180,000 - $220,000 base + 1.0-2.0% equity
*Benchmark*: VP GTM at early-stage SaaS. Estimated from VP-level benchmarks.

---

## 3. Hiring Plan

### 3.1 Month-by-Month Schedule

**Constraints**:
- **Time to hire**: 35 days (junior engineers) to 70 days (senior roles, VPs) ([Paraform](https://www.paraform.com/blog/average-time-to-hire-software-engineer), [Huntly](https://huntly.ai/blog/time-to-hire-in-tech/))
- **Onboarding**: 4-8 weeks to full productivity
- **Stagger hires**: Avoid onboarding 3+ people simultaneously

| Month | Role | Hire Date | Start Date | Full Productivity | Notes |
|-------|------|-----------|------------|-------------------|-------|
| **0** | Engineering Manager | Week 1 | Week 5 | Week 9 | Post immediately, start by Month 1 |
| **0** | Full-stack Engineer #1 | Week 2 | Week 6 | Week 10 | Critical for Sprint 2 start |
| **1** | Product Designer | Week 5 | Week 9 | Week 13 | Visual direction for Sprint 2 |
| **1** | Full-stack Engineer #2 | Week 6 | Week 10 | Week 14 | Ramp for Sprint 3 |
| **2** | Product Manager | Week 8 | Week 12 | Week 16 | Own roadmap Sprint 3-7 |
| **2** | Full-stack Engineer #3 | Week 10 | Week 14 | Week 18 | Scale for Sprint 3 |
| **3** | Head of Partner Success | Week 12 | Week 16 | Week 20 | Before Beta (Month 4) |
| **3** | PSM #1 | Week 13 | Week 17 | Week 21 | Support first 5 partners |
| **4** | Backend Engineer | Week 16 | Week 20 | Week 24 | Performance/scaling focus |
| **4** | Full-stack Engineer #4 | Week 17 | Week 21 | Week 25 | Board MVP (Sprint 5) |
| **5** | PSM #2 | Week 20 | Week 24 | Week 28 | Support 10 partners (Beta) |
| **6** | Marketing Lead | Week 24 | Week 28 | Week 32 | Partner recruitment |
| **7** | PSM #3 | Week 28 | Week 32 | Week 36 | Scale to 15 partners |
| **7** | Sales Rep (Direct) | Week 29 | Week 33 | Week 37 | Direct sales channel |
| **8** | PSM #4 | Week 32 | Week 36 | Week 40 | Scale to 20 partners |
| **8** | Full-stack Engineer #5 | Week 33 | Week 37 | Week 41 | Post-GA features |
| **9** | PSM #5 | Week 36 | Week 40 | Week 44 | Scale to 30 partners |
| **10** | Backend Engineer #2 | Week 40 | Week 44 | Week 48 | Scaling/infrastructure |
| **10** | VP GTM | Week 41 | Week 45 | Week 49 | GTM org reaches 10 people |
| **11** | PSM #6 | Week 44 | Week 48 | Week 52 | Scale to 40 partners |
| **12** | Operations Manager | Week 48 | Week 52 | Week 56 | Ops professionalization |

**Cumulative Headcount**:
- Month 0: 2 (CEO + CTO existing)
- Month 3: 6
- Month 6: 12 (GA)
- Month 9: 17
- Month 12: 23
- Month 18: 38 (full build-out)

### 3.2 Critical Path Analysis

**Sprint 2 Start (Week 1)**: Must have Engineering Manager + 1-2 engineers. Risk: Hiring slips → sprint delay.

**Beta Partners (Month 3-4)**: Must have Head of Partner Success by Week 16. Risk: Can't enable partners → Beta fails.

**GA Launch (Month 6)**: Must have 8-10 people (6 eng/product, 2-3 GTM). Risk: Under-staffed → quality suffers.

**Partner Scaling (Month 7-12)**: Must hire 1 PSM every 6-8 weeks. Risk: PSMs overloaded → partner churn.

### 3.3 Hiring Velocity

**Month 0-6**: 1-2 hires per month (10 total)
**Month 7-12**: 1-2 hires per month (11 total)
**Month 13-18**: 2-3 hires per month (15 total)

**Risk**: Hiring velocity assumes 80% offer acceptance. If lower, extend timeline or use recruiting agencies.

---

## 4. Budget (6-Month)

### 4.1 Revenue (Month 0-6)

| Month | Direct Sales | Partner Sales | Total Revenue | Notes |
|-------|-------------|---------------|---------------|-------|
| 0 | $0 | $0 | $0 | Alpha (free) |
| 1 | $0 | $0 | $0 | Alpha (free) |
| 2 | $0 | $0 | $0 | Alpha (free) |
| 3 | $2,000 | $0 | $2,000 | Beta starts, 3-5 paid pilots |
| 4 | $5,000 | $3,000 | $8,000 | Beta expands |
| 5 | $8,000 | $10,000 | $18,000 | Beta mature, 10 partners signed |
| **Total** | **$15,000** | **$13,000** | **$28,000** | Pre-GA revenue |

**Assumptions**:
- Direct: 5-10 pilot customers at $149/month/board (avg 2 boards per customer = $300/month)
- Partner: 10 partners signed by Month 5, 20% deploy pilots ($149 × 2 boards × 10 customers × 20% = $3K/month)

### 4.2 Expenses (Month 0-6)

#### Payroll

| Role | Count | Monthly Salary | Benefits (30%) | Total Monthly | 6-Month Total |
|------|-------|----------------|----------------|---------------|---------------|
| **Month 0-1** | | | | | |
| Engineering Manager | 1 | $16,000 | $4,800 | $20,800 | $41,600 (2 mo) |
| Full-stack Engineer #1 | 1 | $11,000 | $3,300 | $14,300 | $28,600 (2 mo) |
| **Month 1-2** | | | | | |
| Product Designer | 1 | $9,000 | $2,700 | $11,700 | $58,500 (5 mo) |
| Full-stack Engineer #2 | 1 | $11,000 | $3,300 | $14,300 | $71,500 (5 mo) |
| **Month 2-3** | | | | | |
| Product Manager | 1 | $14,000 | $4,200 | $18,200 | $72,800 (4 mo) |
| Full-stack Engineer #3 | 1 | $11,000 | $3,300 | $14,300 | $57,200 (4 mo) |
| **Month 3-4** | | | | | |
| Head of Partner Success | 1 | $14,000 | $4,200 | $18,200 | $54,600 (3 mo) |
| PSM #1 | 1 | $8,500 | $2,550 | $11,050 | $33,150 (3 mo) |
| **Month 4-5** | | | | | |
| Backend Engineer | 1 | $13,500 | $4,050 | $17,550 | $35,100 (2 mo) |
| Full-stack Engineer #4 | 1 | $11,000 | $3,300 | $14,300 | $28,600 (2 mo) |
| **Month 5-6** | | | | | |
| PSM #2 | 1 | $8,500 | $2,550 | $11,050 | $22,100 (2 mo) |
| Marketing Lead | 1 | $11,000 | $3,300 | $14,300 | $14,300 (1 mo) |
| **Subtotal** | | | | | **$517,650** |

**CEO/CTO**: Assumed existing (not in budget). If need to hire CTO, add $200K+ annually.

**Fractional COO/Ops**: $5,000/month × 6 months = $30,000

**Total Payroll (6 months)**: $547,650

#### R&D (Non-Payroll)

| Item | Monthly Cost | 6-Month Total | Notes |
|------|--------------|---------------|-------|
| Cloud Infrastructure | $500 | $3,000 | Supabase Pro ($125) + overages, hosting |
| LLM API Costs | $2,000 | $12,000 | 1,000 users × $30-50/user/month (Alpha/Beta) |
| Dev Tools | $500 | $3,000 | GitHub, CI/CD, monitoring, Vercel, etc. |
| **Subtotal** | **$3,000** | **$18,000** | |

**LLM Costs Assumptions**:
- Claude Sonnet 4.5: $3 input / $15 output per million tokens ([ScreenApp](https://screenapp.io/blog/claude-ai-pricing))
- Avg 100K tokens per user per month (10 deep dives × 10K tokens each)
- 100K tokens = $0.30 input + $1.50 output = $1.80/user/month
- With overhead (context assembly, re-runs), estimate $30-50/user/month
- Alpha/Beta: 50-100 active users × $40 avg = $2K-4K/month

#### Sales & Marketing

| Item | Monthly Cost | 6-Month Total | Notes |
|------|--------------|---------------|-------|
| Partner Events | $2,000 | $12,000 | Conferences, partner dinners |
| Website/Marketing | $1,000 | $6,000 | Hosting, ads, content tools |
| Sales Tools | $500 | $3,000 | CRM (HubSpot/Notion), email |
| **Subtotal** | **$3,500** | **$21,000** | |

#### G&A (General & Administrative)

| Item | Monthly Cost | 6-Month Total | Notes |
|------|--------------|---------------|-------|
| Legal | $2,000 | $12,000 | Contracts, compliance, incorporation |
| Accounting | $1,000 | $6,000 | Bookkeeping, tax prep |
| Insurance | $500 | $3,000 | D&O, general liability |
| Office/Tools | $1,000 | $6,000 | Slack, Notion, Zoom, etc. |
| **Subtotal** | **$4,500** | **$27,000** | |

#### One-Time Costs

| Item | Count | Cost per Hire | Total Cost | Notes |
|------|-------|---------------|------------|-------|
| Recruiting Fees | 10 hires | $18,000 | $180,000 | 20% of first-year salary ([Dover](https://www.dover.com/blog/tech-recruiter-fees-2025-cost-guide)) |
| Onboarding Costs | 10 hires | $2,000 | $20,000 | Laptop, software, training |
| **Subtotal** | | | **$200,000** | |

**Recruiting Fee Calculation**:
- Engineering Manager: $190K × 20% = $38K
- Full-stack Engineers (4): $135K × 20% × 4 = $108K
- Backend Engineer: $160K × 20% = $32K
- Product Manager: $165K × 20% = $33K
- Product Designer: $110K × 20% = $22K
- Head of Partner Success: $165K × 20% = $33K
- PSMs (2): $100K × 20% × 2 = $40K
- **Total**: $306K (round down to $180K assuming mix of agency/internal recruiting)

### 4.3 Total Budget (Month 0-6)

| Category | 6-Month Total | % of Total |
|----------|---------------|------------|
| Payroll | $547,650 | 66% |
| R&D (non-payroll) | $18,000 | 2% |
| S&M (non-payroll) | $21,000 | 3% |
| G&A | $27,000 | 3% |
| One-Time (recruiting, onboarding) | $200,000 | 24% |
| **Total Expenses** | **$813,650** | **98%** |
| Revenue | $28,000 | 2% |
| **Net Burn** | **$785,650** | **100%** |

**Average Monthly Burn**: $131K (Month 0-6)

### 4.4 Monthly P&L (Month 0-6)

| Month | Revenue | Payroll | R&D | S&M | G&A | One-Time | Total Expenses | Net Burn | Cumulative Burn |
|-------|---------|---------|-----|-----|-----|----------|----------------|----------|-----------------|
| 0 | $0 | $35,100 | $2,000 | $2,000 | $4,500 | $76,000 | $119,600 | ($119,600) | ($119,600) |
| 1 | $0 | $64,100 | $2,500 | $3,000 | $4,500 | $44,000 | $118,100 | ($118,100) | ($237,700) |
| 2 | $0 | $96,800 | $3,000 | $3,500 | $4,500 | $36,000 | $143,800 | ($143,800) | ($381,500) |
| 3 | $2,000 | $129,250 | $3,000 | $4,000 | $4,500 | $44,000 | $184,750 | ($182,750) | ($564,250) |
| 4 | $8,000 | $161,100 | $3,000 | $4,000 | $4,500 | $0 | $172,600 | ($164,600) | ($728,850) |
| 5 | $18,000 | $181,300 | $3,000 | $4,500 | $4,500 | $0 | $193,300 | ($175,300) | ($904,150) |
| **Total** | **$28,000** | **$667,650** | **$16,500** | **$21,000** | **$27,000** | **$200,000** | **$932,150** | **($904,150)** | |

**Note**: Payroll includes benefits (30%). One-time costs front-loaded (recruiting fees paid upon hire).

### 4.5 Assumptions

**Salaries**:
- Based on market benchmarks for SaaS startups (Wellfound, Glassdoor, etc.)
- San Francisco Bay Area / Seattle market rates
- Equity not included in cash burn (options/RSUs vest over 4 years)

**Benefits**:
- 30% of base salary ([Kruze Consulting](https://kruzeconsulting.com/blog/how-do-you-calculate-the-true-cost-of-a-startup-employee/), [BIBSMA](https://bibsma.com/how-much-do-employee-benefits-cost-per-employee-for-a-young-startup/))
- Health insurance: $500-1,800/month per employee (average $800)
- Dental, vision, 401k, PTO, payroll taxes

**LLM Costs**:
- Conservative estimate: $30-50/user/month during Alpha/Beta
- Post-GA: $20-30/user/month at scale (batch API, caching, optimization)

**Recruiting Fees**:
- 20% of first-year salary for agency hires ([Dover](https://www.dover.com/blog/tech-recruiter-fees-2025-cost-guide))
- Mix of agency (50%) and internal recruiting (50%) → effective 10-15% avg

### 4.6 Sensitivity Analysis

| Scenario | Hiring Speed | LLM Costs | Recruiting | Total 6-Mo Burn | Notes |
|----------|--------------|-----------|------------|-----------------|-------|
| **Best Case** | -1 month delay | -50% | Internal only | $650K | Hiring slower, frugal |
| **Base Case** | On schedule | As planned | 20% agency | $905K | Current plan |
| **Worst Case** | +1 month accelerated | +50% | 30% agency | $1,150K | Aggressive hiring, high churn |

**Key Variables**:
- **Hiring speed**: ±1 month per hire = ±$100K (payroll timing)
- **LLM costs**: ±50% = ±$6K (Alpha/Beta usage variance)
- **Recruiting**: 10-30% fees = ±$60K (agency vs internal mix)

---

## 5. Burn Rate & Runway

### 5.1 Monthly Burn (Month 0-18)

| Phase | Months | Avg Monthly Burn | Notes |
|-------|--------|------------------|-------|
| **Foundation** | 0-2 | $127K | Small team (2-6 people) |
| **Build** | 3-5 | $174K | Team scaling (6-12 people) |
| **GA Launch** | 6 | $175K | Full team in place (12 people) |
| **Scale** | 7-12 | $225K | Partner Success scaling (12-23 people) |
| **Maturity** | 13-18 | $315K | Full build-out (23-38 people) |

**Monthly Burn Calculation**:
- Payroll: Headcount × avg salary × 1.3 (benefits)
- R&D: $3K-5K/month (cloud, LLM, tools)
- S&M: $5K-15K/month (events, marketing, sales tools)
- G&A: $5K-10K/month (legal, accounting, insurance, office)
- One-time: Amortized over 6 months ($200K recruiting / 6 = $33K/month)

### 5.2 Cumulative Cash Position

| Month | Revenue | Expenses | Net Burn | Cumulative Burn |
|-------|---------|----------|----------|-----------------|
| 0 | $0 | $120K | ($120K) | ($120K) |
| 3 | $2K | $185K | ($183K) | ($564K) |
| 6 | $18K | $193K | ($175K) | ($1,890K) |
| 9 | $45K | $230K | ($185K) | ($2,445K) |
| 12 | $120K | $265K | ($145K) | ($3,280K) |
| 15 | $320K | $340K | ($20K) | ($3,340K) |
| 18 | $680K | $385K | +$295K | ($3,045K) |

**Revenue Growth**:
- Month 6: $18K (10 partners signed, 20% deploying)
- Month 12: $120K (40 partners, 50% deploying, 20 direct customers)
- Month 18: $680K (120 partners, 80% deploying, 100 direct customers)

**Key Insight**: Burn peaks Month 13-15 ($3.34M cumulative) as Partner Success team scales before revenue catches up. Positive cash flow projected Month 17-18 as partner deployments mature.

### 5.3 Funding Recommendation

**Amount**: $10-12M (Seed + Series A, or combined round)

**Rationale**:
- $3.34M peak cumulative burn (Month 15)
- $3M additional buffer for runway extension, unforeseen costs
- $2-4M for acceleration (hiring faster, more partners, board R&D)

**Runway**:
- $10M → 30 months runway (through Month 30, 12 months past break-even)
- $12M → 36 months runway (through Month 36, 18 months past break-even)

**Milestones Before Next Raise**:
- Month 6: GA launch, 10 partners signed
- Month 12: 40 partners, $1.5M ARR run rate ($120K MRR)
- Month 18: 120 partners, $8M ARR run rate ($680K MRR)

**Valuation Implication**:
- Seed: $3-5M at $15-25M post-money (20% dilution)
- Series A: $7-9M at $40-60M post-money (15-20% dilution)
- Combined: $10-12M at $30-40M post-money (25-30% dilution)

**Risk**: If hiring slips or partner recruitment is slower, extend runway with bridge financing or reduce burn (freeze hiring, reduce S&M spend).

### 5.4 Runway Scenarios

| Funding | Burn Rate | Runway | Break-Even Month | Buffer After Break-Even |
|---------|-----------|--------|------------------|------------------------|
| $8M | $265K avg | 24 months | Month 17 | 7 months |
| $10M | $265K avg | 30 months | Month 17 | 13 months |
| $12M | $265K avg | 36 months | Month 17 | 19 months |

**Recommendation**: Raise $10-12M for 30-36 months runway. Sufficient buffer to:
- Hit $8M ARR by Month 18 (Series A traction)
- Navigate slower partner adoption (extend runway)
- Invest in board R&D or additional verticals

---

## 6. Resource Allocation

### 6.1 Headcount Mix (By Function)

**Month 6 (GA)**:
```
Total: 12
├─ Engineering & Product: 8 (67%)
│  ├─ Engineering: 6 (50%)
│  └─ Product/Design: 2 (17%)
├─ GTM: 3 (25%)
│  └─ Partner Success: 3 (25%)
└─ Operations: 1 (8%)
```

**Month 12 (Scale)**:
```
Total: 23
├─ Engineering & Product: 11 (48%)
│  ├─ Engineering: 9 (39%)
│  └─ Product/Design: 2 (9%)
├─ GTM: 10 (43%)
│  ├─ Partner Success: 7 (30%)
│  ├─ Marketing: 1 (4%)
│  ├─ Sales: 1 (4%)
│  └─ VP GTM: 1 (4%)
└─ Operations: 2 (9%)
```

**Month 18 (Maturity)**:
```
Total: 38
├─ Engineering & Product: 17 (45%)
│  ├─ Engineering: 13 (34%)
│  └─ Product/Design: 4 (11%)
├─ GTM: 17 (45%)
│  ├─ Partner Success: 13 (34%)
│  ├─ Marketing: 3 (8%)
│  ├─ Sales: 3 (8%)
│  └─ VP GTM: 1 (3%)
└─ Operations: 4 (10%)
```

**Evolution**:
- **Engineering**: 67% → 48% → 45% (decreases as % but grows in absolute numbers)
- **GTM**: 25% → 43% → 45% (doubles as % to support partner scaling)
- **Operations**: 8% → 9% → 10% (steady, scales with company)

**Insight**: Partner-led GTM model requires **GTM headcount parity with Engineering** by Month 18 (17 GTM, 17 Eng+Product). Contrast with direct sales SaaS (typically 3:1 eng:sales ratio).

### 6.2 Budget Mix (By Category)

**Month 0-6 (Foundation)**:
```
Total Expenses: $932K
├─ Payroll: $668K (72%)
├─ R&D: $17K (2%)
├─ S&M: $21K (2%)
├─ G&A: $27K (3%)
└─ One-Time: $200K (21%)
```

**Month 7-12 (Scale)**:
```
Total Expenses: $1.62M
├─ Payroll: $1.35M (83%)
├─ R&D: $36K (2%)
├─ S&M: $60K (4%)
├─ G&A: $54K (3%)
└─ One-Time: $120K (7%)
```

**Month 13-18 (Maturity)**:
```
Total Expenses: $2.31M
├─ Payroll: $1.98M (86%)
├─ R&D: $54K (2%)
├─ S&M: $108K (5%)
├─ G&A: $90K (4%)
└─ One-Time: $80K (3%)
```

**Payroll Dominance**: 72-86% of expenses (standard for early-stage SaaS). Non-payroll costs remain lean (R&D 2%, S&M 4-5%, G&A 3-4%).

### 6.3 Engineering Allocation (Within Engineering)

Per [STRATEGY.md](./STRATEGY.md), engineering allocation:
- **Core/Web**: 70% (4-5 engineers at Month 6, 6-8 at Month 12)
- **Board**: 20% (1-2 engineers at Month 6, 2-3 at Month 12)
- **Connectors**: 10% (0.5-1 engineer at Month 6, 1-2 at Month 12)

**Month 6** (6 engineers total):
- Core/Web: 4 engineers (agents, feedback, memory, web workspace)
- Board: 1 engineer (firmware, SDK, board UI)
- Connectors: 1 engineer (Slack, GitHub, Google Calendar integrations)

**Month 12** (9 engineers total):
- Core/Web: 6 engineers (proactive agents, knowledge base, search, performance)
- Board: 2 engineers (meeting summary, real-time features, board admin)
- Connectors: 1 engineer (Slack write-back, email, CRM integrations)

**Rationale**: "Never less than 70% on core" (Strategy doc). Board is consumption surface; value created in async work (core/web). Connectors enable partnerships but don't create core value.

### 6.4 Partner Success Capacity Planning

**Capacity Model**:
- **Onboarding phase** (Month 3-12): 10 partners per PSM
- **Scale phase** (Month 13-18): 15-20 partners per PSM

**Partner Growth**:
- Month 6: 10 partners → 2 PSMs (1:5 ratio, co-development)
- Month 12: 40 partners → 6 PSMs (1:7 ratio, active onboarding)
- Month 18: 120 partners → 12 PSMs (1:10 ratio, post-onboarding support)

**Comparison to CSM Benchmarks**:
- CSMs manage 10-25 Enterprise customers ([Vitally](https://www.vitally.io/post/what-is-the-golden-ratio-of-customer-success-managers-to-customers))
- CSMs manage $2-5M ARR ([Tomasz Tunguz](https://tomtunguz.com/how-much-arr-can-a-csm-manage/))
- PSMs manage fewer partners but higher complexity (each partner = 20-200 end customers)

**PSM Workload**:
- Partner onboarding: 20-30 hours per partner (training, certification, first deployment)
- QBRs: 4 hours per quarter per partner (16 hours/year)
- Support/troubleshooting: 5-10 hours per month per partner
- Best practice sharing: 10 hours per month across portfolio

**Total Capacity**: ~120-150 hours/month per PSM → 10-15 partners sustainable.

### 6.5 Allocation Rationale

**Why 45% Engineering, 45% GTM?**

Traditional SaaS: 60-70% eng, 20-30% GTM (direct sales).

OpenVibe: 45% eng, 45% GTM (partner-led).

**Reason**: Partner GTM is labor-intensive. Each partner requires:
- Hands-on enablement (training, certification)
- First 5 client deployments support
- Ongoing QBRs and best practice sharing
- Relationship management (not transactional)

**Benchmark**: HubSpot scaled through agency partners. Each Partner Development Manager (PDM) supported 40-60 partners ([HubSpot Partners](https://www.hubspot.com/partners/faqs)). Similar ratio to OpenVibe PSMs (10-15 partners per PSM during high-growth phase).

**Trade-off**: Higher GTM headcount → higher burn, but faster distribution. Partner-sourced revenue = 93% by Month 24 (Strategy doc). ROI: Each PSM generates $1.5-2M ARR through partners.

---

## 7. Key Insights

### 7.1 Team Structure Insights

1. **Monolith enables lean engineering**: 5-6 engineers through GA, 8-10 through Month 18. Benchmark: Teams <10 developers should build monoliths ([Binary Republik](https://blog.binaryrepublik.com/2026/02/modular-monolith-vs-microservices.html)).

2. **Partner Success is the bottleneck**: Scaling to 120 partners requires 12 PSMs (1:10 ratio). Under-staffing PSMs → partner churn → thesis failure. GTM headcount must match engineering by Month 18.

3. **Front-load designer**: Visual direction needed early (PROGRESS.md open question #2). Hire Month 0-1, not Month 6.

4. **VP GTM at Month 10-12**: Needed once GTM team reaches 8-10 people. Too early (Month 6) → unnecessary overhead. Too late (Month 15) → lack of leadership.

### 7.2 Budget Insights

1. **Burn is 72-86% payroll**: Early-stage SaaS is people-intensive. Non-payroll costs remain lean (R&D 2%, S&M 4-5%, G&A 3-4%).

2. **Recruiting fees are material**: $180K-$300K over 18 months (10-15% of total burn). Optimize with mix of agency (20%) and internal recruiting (80%).

3. **LLM costs are manageable**: $30-50/user/month during Alpha/Beta, $20-30/user/month at scale. Not a major cost driver (<2% of expenses).

4. **Partner GTM is capital-efficient**: Partner-sourced revenue = 93% by Month 24, but requires 45% GTM headcount. Trade-off: Higher burn short-term, faster revenue long-term.

### 7.3 Hiring Insights

1. **Hiring lead time is critical**: 35-70 days to hire + 4-8 weeks onboarding = 3-4 months total. Must start hiring Month 0 for Sprint 2 (Month 1).

2. **Stagger hires to avoid onboarding overload**: Never onboard 3+ people simultaneously. Spread hires across 2-4 week intervals.

3. **Critical path: Partner Success hiring**: Must hire 1 PSM every 6-8 weeks (Month 7-18) to support partner scaling. Slippage → partner churn.

4. **San Francisco / Seattle market**: Salary benchmarks assume Bay Area / Seattle. If hiring remote (lower-cost markets), reduce salaries 20-30% → extend runway.

### 7.4 Runway Insights

1. **Peak burn Month 13-15**: $3.34M cumulative burn before revenue catches up. Need $10-12M for 30-36 months runway.

2. **Break-even Month 17-18**: Projected based on 120 partners × 80% deploying × $149/board/month. Risk: If partner adoption slower, extend break-even to Month 24.

3. **Buffer is insurance**: 12-18 months buffer after break-even allows for:
   - Slower partner adoption
   - Additional verticals (accounting firms, MSPs)
   - Board R&D investment
   - Series A fundraising without pressure

4. **Rule of 40 trajectory**: Month 18 ARR ($8M) / Burn ($4.8M cumulative) = 167% burn multiple. Strong for Series A (benchmark <2.0x burn multiple).

---

## 8. Recommendations

### 8.1 Strategic Recommendations

1. **Hire Engineering Manager Month 0**: Non-negotiable. Without eng manager, sprints won't execute. Start recruiting immediately.

2. **Hire Designer Month 0-1**: Visual direction is a known gap (PROGRESS.md). Don't wait until Month 6.

3. **Front-load Partner Success hiring**: Hire Head of Partner Success Month 2-3 (before Beta), not Month 6. Partner enablement takes 2-3 months → must start early.

4. **Raise $10-12M, not $8M**: $8M = 24 months runway, only 7 months buffer after break-even. Too tight. $10-12M = 30-36 months runway, comfortable buffer.

5. **Use fractional ops until Month 12**: Don't hire full-time COO until GTM team is 10+ people. Fractional ops ($5K/month) sufficient for Month 0-12.

### 8.2 Hiring Recommendations

1. **Optimize recruiting mix**: 80% internal recruiting (job boards, referrals), 20% agency (hard-to-fill roles like eng manager, VP GTM). Saves $120K in recruiting fees.

2. **Stagger full-stack hires**: Hire 1 every 4-6 weeks (Month 0, 1, 2, 4) to avoid onboarding overload.

3. **Prioritize PSM hiring velocity**: Budget for 1 PSM every 6-8 weeks (Month 7-18). If hiring slips, partner churn → thesis fails.

4. **Consider remote hiring**: If talent scarce in Bay Area, hire remote engineers (lower-cost markets). Salary savings: 20-30% → extend runway 3-6 months.

### 8.3 Budget Recommendations

1. **LLM cost optimization**: Use batch API (50% discount), caching, and prompt optimization to reduce costs from $50/user/month to $20-30/user/month at scale. Benchmark: [Claude API](https://screenapp.io/blog/claude-ai-pricing) batch pricing.

2. **Recruiting cost control**: Negotiate flat-fee recruiting ($10-15K per hire) vs percentage-based (20-30% of salary). Saves $60-100K over 18 months.

3. **S&M spend discipline**: Partner events and marketing should not exceed $10K/month until Month 12. Scale S&M spend with revenue (target 40-50% of revenue by Month 18).

4. **Cash flow timing**: Align hiring with funding milestones. If fundraising delays, freeze hiring Month 6-9 to preserve runway.

### 8.4 Risk Mitigation Recommendations

1. **Hiring risk**: If hiring slips (offer declines, long lead times), extend hiring timeline by 1-2 months. Don't compromise on quality to hit timeline.

2. **Partner adoption risk**: If partner deployments <50% by Month 12 (vs 80% target), adjust PSM hiring (freeze 2-3 PSMs) to preserve runway.

3. **LLM cost risk**: If LLM costs 2x projected ($100/user/month), implement aggressive caching and prompt optimization. Budget $50K emergency fund for LLM overages.

4. **Burn rate risk**: If burn exceeds $350K/month (vs $315K planned), implement hiring freeze and reduce S&M spend to extend runway.

---

## Appendix A: Salary Benchmarks (Sources)

| Role | Avg Salary | Range | Source |
|------|-----------|-------|--------|
| Engineering Manager | $196K | $150K-$316K | [Wellfound SaaS](https://wellfound.com/hiring-data/r/engineering-manager-1/i/saas) |
| Full-Stack Engineer | $126K | $96K-$168K | [Glassdoor](https://www.glassdoor.com/Salaries/full-stack-engineer-salary-SRCH_KO0,19.htm) |
| Backend Engineer | $174K | $135K-$227K | [Glassdoor](https://www.glassdoor.com/Salaries/backend-engineer-salary-SRCH_KO0,16.htm) |
| Product Manager | $167K | $80K-$253K | [Wellfound SaaS](https://wellfound.com/hiring-data/r/product_manager/i/saas) |
| Product Designer | $85K | $1K-$225K | [Wellfound SaaS](https://wellfound.com/hiring-data/r/ui-ux-designer/i/saas) |
| Partner Success Manager | $149K | $117K-$195K | [Glassdoor](https://www.glassdoor.com/Salaries/partner-success-manager-salary-SRCH_KO0,23.htm) |

## Appendix B: Capacity Benchmarks (Sources)

| Metric | Benchmark | Source |
|--------|-----------|--------|
| CSM Capacity (Enterprise) | 10-50 customers | [Vitally](https://www.vitally.io/post/what-is-the-golden-ratio-of-customer-success-managers-to-customers) |
| CSM Capacity (ARR) | $2-5M ARR | [Tomasz Tunguz](https://tomtunguz.com/how-much-arr-can-a-csm-manage/) |
| PSM Capacity (Partners) | 10-20 partners | Derived from CSM benchmarks |
| Time to Hire (Engineer) | 35-70 days | [Paraform](https://www.paraform.com/blog/average-time-to-hire-software-engineer), [Huntly](https://huntly.ai/blog/time-to-hire-in-tech/) |
| Recruiting Fees | 20-30% salary | [Dover](https://www.dover.com/blog/tech-recruiter-fees-2025-cost-guide) |
| Benefits Cost | 20-30% salary | [Kruze](https://kruzeconsulting.com/blog/how-do-you-calculate-the-true-cost-of-a-startup-employee/), [BIBSMA](https://bibsma.com/how-much-do-employee-benefits-cost-per-employee-for-a-young-startup/) |

## Appendix C: SaaS Benchmarks (Sources)

| Metric | Benchmark | Source |
|--------|-----------|--------|
| Monolith Team Size | <10 engineers | [Binary Republik](https://blog.binaryrepublik.com/2026/02/modular-monolith-vs-microservices.html), [Software Seni](https://www.softwareseni.com/what-is-a-modular-monolith-and-how-does-it-combine-the-best-of-both-architectural-worlds/) |
| PM:Eng Ratio | 1:6-10 | [Sharebird](https://sharebird.com/h/product-management/q/what-is-the-right-pm-to-eng-ratio-im-the-first-pm-and-we-have-8-engineers-and-1-designer) |
| CAC Payback (Seed) | <12 months | [First Page Sage](https://firstpagesage.com/reports/saas-cac-payback-benchmarks/) |
| LTV:CAC Ratio | 3:1 (Seed), 4:1 (Series A+) | [Averi](https://www.averi.ai/blog/15-essential-saas-metrics-every-founder-must-track-in-2026-(with-benchmarks)) |
| Rule of 40 | Growth + Profit ≥ 40% | [Abacum](https://www.abacum.ai/blog/the-rule-of-40-redefined-framework-for-saas-finance) |
| Burn Multiple | <2.0x (good), <1.0x (great) | [Phoenix Strategy](https://www.phoenixstrategy.group/blog/burn-rate-trends-investors-expect-2025) |

---

**Next Steps**:
1. User review: Does team structure make sense? Are role definitions clear?
2. Budget validation: Are salary ranges realistic? LLM cost assumptions correct?
3. Hiring plan: Is 35-70 day lead time achievable? Should we use more agencies?
4. Funding: Is $10-12M the right amount? Series A timing (Month 18)?

---

*This document is part of the OpenVibe V2 validation phase. See also: [THESIS.md](../THESIS.md), [STRATEGY.md](../STRATEGY.md), [DESIGN-SYNTHESIS.md](../DESIGN-SYNTHESIS.md)*
