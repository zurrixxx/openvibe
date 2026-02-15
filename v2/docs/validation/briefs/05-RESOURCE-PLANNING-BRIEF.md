# Research Brief: Resource Planning Agent

**Agent ID**: Resource Planning Agent
**Phase**: Phase 4 (Day 4-5)
**Priority**: P1 - Important

---

## Mission

Define the team, budget, and resources needed to execute the strategy.

**Output**: Team structure, role definitions, hiring plan, budget model

---

## Context

**What we know**:
- 7 sprints over 24 weeks (6 months to GA)
- Engineering allocation: 70% core/web, 20% board, 10% connectors
- Target: $61M ARR by Month 18
- GTM is partner-led (requires partner success team)

**What we DON'T know** (your job):
1. How many people do we need? (By function, by stage)
2. What roles are critical? (Hire first vs hire later)
3. What's the hiring timeline?
4. What's the 6-month budget?
5. What's the burn rate and runway?

**Dependencies**:
- Unit Economics Agent: Cost structure, margins
- GTM Operations Agent: Sales process, marketing strategy
- Growth Strategy Agent: Growth model, stage-based needs

---

## Research Objectives

### 1. Team Structure (6, 12, 18 Months)

**Objective**: Define org chart at each milestone

**What to design**:

**Month 6 (GA Launch) - Target Team Size**:

**Engineering & Product**:
- Engineering Manager: 1
- Full-stack Engineers: ?
- Frontend Engineers: ?
- Backend Engineers: ?
- Product Manager: ?
- Designer: ?

**Go-to-Market**:
- Head of GTM: 1
- Partner Success Managers (PSMs): ?
- Sales (direct): ?
- Marketing: ?

**Operations**:
- Operations Manager: ?
- Customer Support: ?

**Leadership**:
- CEO: 1 (existing)
- CTO: ? (existing or hire?)
- Head of Product: ?

**Total headcount at Month 6**: ?

**Month 12 (Scale Phase)**:
- How does the team grow from Month 6?
- Which functions scale fastest? (PSMs? Engineering?)

**Month 18 (Maturity Phase)**:
- Target team size to support 11,500 customers?
- Span of control: How many customers per PSM?

**Research sources**:
- Early-stage SaaS team benchmarks (OpenView)
- AI product team structures
- B2B2B partner success team sizing (HubSpot, Zapier)
- Engineering team sizing for monolith architecture

**Deliverable**: 3 org charts (Month 6, 12, 18) with:
- Headcount by function
- Reporting structure
- Key hires vs backfills

---

### 2. Key Role Definitions

**Objective**: Define must-have roles and responsibilities

**What to define**:

**Critical Roles** (hire first):

1. **Engineering Manager**
   - Why critical: Lead 7 sprints to GA
   - Responsibilities: Team leadership, sprint planning, technical decisions
   - When to hire: Month 0 (immediately)
   - Profile: Experience with AI products, monolith → microservices, 5-10 years

2. **Full-stack Engineers (N)**
   - Why critical: Build core product
   - Responsibilities: Web app, agents, integrations
   - When to hire: Month 0-2 (stagger)
   - Profile: Next.js, tRPC, Supabase, AI/LLM experience

3. **Product Manager**
   - Why critical: Define and prioritize features
   - Responsibilities: Roadmap, specs, user research
   - When to hire: Month 1-2
   - Profile: B2B SaaS, AI product experience, technical

4. **Head of Partner Success**
   - Why critical: Partner GTM is the strategy
   - Responsibilities: Partner recruitment, enablement, success
   - When to hire: Month 2-3 (before Beta)
   - Profile: Channel sales experience, B2B2B, consultative selling

5. **Partner Success Managers (PSMs)**
   - Why critical: Scale partner network
   - Responsibilities: Onboard partners, train, support deployments
   - When to hire: Month 3-6 (as partners sign up)
   - Profile: Customer success + technical, partner management

6. **Designer**
   - Why critical: Visual direction needed (PROGRESS.md open question #2)
   - Responsibilities: UI/UX, agent message styling, design system
   - When to hire: Month 0-1
   - Profile: Product design, AI/conversational UI experience

**Research sources**:
- SaaS role definitions (First Round, a16z)
- AI product team structures (Jasper, Copy.ai)
- Partner success team structures

**Deliverable**: Role definition cards:
- Role title
- Why critical (strategic importance)
- Responsibilities (5-7 bullets)
- When to hire (timeline)
- Profile (experience, skills, background)
- Comp range (based on market data)

---

### 3. Hiring Plan

**Objective**: Month-by-month hiring schedule

**What to plan**:

**Month 0-2 (Foundation)**:
- [ ] Engineering Manager (Month 0)
- [ ] Full-stack Engineers x2 (Month 0-1)
- [ ] Designer (Month 1)
- [ ] Product Manager (Month 2)

**Month 3-5 (Beta)**:
- [ ] Head of Partner Success (Month 3)
- [ ] PSM x1 (Month 3)
- [ ] Full-stack Engineer x1 (Month 4)
- [ ] PSM x2 (Month 5)

**Month 6-9 (GA + Scale)**:
- [ ] Marketing Lead (Month 6)
- [ ] PSM x3 (Month 6-8)
- [ ] Sales Rep (direct) (Month 7)
- [ ] Backend Engineer (Month 8)

**Month 10-18 (Scaling)**:
- [ ] PSM x5-10 (as partners grow)
- [ ] Engineering x2-3 (as product expands)
- [ ] Customer Support x2 (as customers grow)

**Constraints**:
- Time to hire: 1-3 months per role
- Onboarding: 1-2 months to full productivity
- Budget: From Unit Economics Agent

**Research sources**:
- SaaS hiring timeline benchmarks
- Technical hiring lead times

**Deliverable**: Hiring Gantt chart:
- Role by month (when posted, when hired)
- Cumulative headcount
- Onboarding periods
- Key milestones (e.g., "Need 3 PSMs before 10-partner launch")

---

### 4. Budget (6-Month)

**Objective**: Detailed budget from Month 0-6

**What to model**:

**Revenue** (Month 0-6):
- Month 0-2: $0 (alpha, free)
- Month 3-5: $X (beta, some paid)
- Month 6: $Y (GA launch, free trial starts)

**Expenses**:

**Payroll** (largest expense):
- Salaries (by role, by month)
- Benefits (30% of salary)
- Payroll taxes

**R&D**:
- Cloud infrastructure (Supabase, hosting)
- LLM costs (API usage)
- Dev tools (GitHub, CI/CD, monitoring)

**Sales & Marketing**:
- Partner recruitment (events, outreach)
- Marketing (website, content, ads)
- Sales tools (CRM, email)

**G&A**:
- Legal (contracts, compliance)
- Accounting
- Insurance
- Office/tools (Slack, Notion, etc.)

**One-time**:
- Recruiting fees (20-30% of first-year salary per hire)
- Onboarding costs

**Research sources**:
- Early-stage SaaS budget templates (SaaStr)
- Startup burn rate benchmarks
- Compensation data (Levels.fyi, Pave, Carta)

**Deliverable**: 6-month budget spreadsheet:
- Monthly P&L (revenue, expenses, burn)
- Cumulative cash position
- Key assumptions (salaries, headcount, LLM costs)
- Sensitivity analysis (what if hiring is faster/slower?)

---

### 5. Burn Rate & Runway

**Objective**: Calculate monthly burn and funding needs

**What to calculate**:

**Monthly burn rate**:
```
Burn = Total Expenses - Revenue
```

**Cumulative cash need**:
- Month 0-6: Total burn
- Buffer: 3-6 months additional runway
- Total funding needed: ?

**Scenarios**:
- **Best case**: Revenue ramps faster, burn is lower
- **Base case**: Plan as budgeted
- **Worst case**: Revenue slower, burn higher (hiring ahead of revenue)

**Funding implications**:
- How much to raise?
- When do we need it?
- What milestones to hit before next raise?

**Research sources**:
- Startup runway benchmarks (Y Combinator, First Round)
- SaaS burn rate by stage
- Funding round sizing (Seed, Series A)

**Deliverable**: Cash flow model:
- Monthly burn (by month)
- Cumulative cash position
- Runway calculation (months of cash remaining)
- Funding recommendation

---

### 6. Resource Allocation

**Objective**: How resources are distributed across functions

**What to allocate**:

**Headcount**:
- Engineering: X% of team
- GTM (partners + sales + marketing): Y%
- Operations: Z%

**Budget**:
- Payroll: A% of expenses
- R&D (non-payroll): B%
- S&M (non-payroll): C%
- G&A: D%

**Engineering allocation** (within engineering):
- Core/web: 70%
- Board: 20%
- Connectors: 10%

**PSM allocation** (within GTM):
- Partners per PSM: ? (capacity)
- Need X PSMs to support Y partners

**Research sources**:
- SaaS resource allocation benchmarks (OpenView)
- Rule of 40 (growth + profit margin benchmark)
- Engineering efficiency metrics

**Deliverable**: Resource allocation model:
- Headcount by function (pie chart)
- Budget by category (pie chart)
- Allocation rationale (why this mix?)
- Adjustments by stage (how it changes over time)

---

## Output Format

**Deliverable**: `docs/v2/validation/RESOURCES-AND-BUDGET.md`

**Structure**:
```markdown
# OpenVibe V2: Resources & Budget

## Executive Summary
- Team size: X (Month 6) → Y (Month 18)
- 6-month burn: $Z
- Funding need: $A

## 1. Team Structure
### 1.1 Month 6 Org Chart
[Visual + headcount]

### 1.2 Month 12 Org Chart
[Visual + headcount]

### 1.3 Month 18 Org Chart
[Visual + headcount]

## 2. Key Role Definitions
[Role cards for critical hires]

## 3. Hiring Plan
### 3.1 Month-by-Month Schedule
[Gantt chart]

### 3.2 Hiring Priorities
[Critical path roles]

## 4. Budget
### 4.1 6-Month Budget
[P&L by month]

### 4.2 Assumptions
[Salaries, headcount, costs]

### 4.3 Sensitivity Analysis
[Best/base/worst case]

## 5. Burn Rate & Runway
### 5.1 Monthly Burn
[Chart]

### 5.2 Cumulative Cash Position
[Chart]

### 5.3 Funding Recommendation
[How much, when, why]

## 6. Resource Allocation
### 6.1 Headcount Mix
[By function]

### 6.2 Budget Mix
[By category]

### 6.3 Allocation Rationale
[Why this mix]

## 7. Key Insights
[Summary]

## 8. Recommendations
[Strategic implications]
```

**Secondary Deliverable**: Spreadsheet with:
- Hiring plan (Gantt)
- Budget model (P&L by month)
- Cash flow model
- Sensitivity tables

---

## Success Criteria

- [ ] Team structure is realistic (not over/under-staffed)
- [ ] Key roles are justified (why these hires first?)
- [ ] Hiring plan is feasible (accounting for lead times)
- [ ] Budget is detailed and credible
- [ ] Burn rate is sustainable (runway >6 months)
- [ ] Resource allocation is balanced
- [ ] User says: "This is fundable and executable"

---

## Timeline

- **Hour 1-2**: Research benchmarks (team size, salaries, burn)
- **Hour 3-5**: Design team structure (3 org charts)
- **Hour 6-8**: Define key roles and hiring plan
- **Hour 9-12**: Build budget model
- **Hour 13-14**: Calculate burn and runway
- **Hour 15-16**: Resource allocation analysis
- **Day 5**: User review → iteration → finalization

---

## Handoff to User

**Review questions**:
1. Is the team structure realistic?
2. Are the key roles correct? (Hire order makes sense?)
3. Is the hiring timeline feasible?
4. Does the budget match reality? (Salaries, costs)
5. Is the burn rate sustainable?
6. Is this a fundable plan?

**Red flags to surface**:
- Burn rate too high (unsustainable)
- Hiring too fast (can't onboard)
- Hiring too slow (can't execute strategy)
- Budget missing key costs

**Next phase dependency**: Risk & Controls Agent needs your burn rate and runway to assess funding risk
