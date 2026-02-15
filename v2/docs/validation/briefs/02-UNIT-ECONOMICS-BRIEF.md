# Research Brief: Unit Economics Agent

**Agent ID**: Unit Economics Agent
**Phase**: Phase 2 (Day 2-3)
**Priority**: P0 - Critical

---

## Mission

Build a comprehensive unit economics model that proves OpenVibe is a viable business.

**Output**: CAC, LTV, margins, cost structure, break-even analysis, cash flow model

---

## Context

**What we know**:
- Pricing: $149/month/board
- 90-day free trial (all 40K boards at GA)
- Partner wholesale: $79-99 (partners sell at $149-199)
- LLM cost estimate: $30-50/board/month
- Target: 11,500 workspaces (34,500 boards) at Month 18 = $61M ARR

**What we DON'T know** (your job):
1. What does it cost to acquire a board? (CAC)
2. How long does a board stay? (LTV)
3. Is LTV/CAC healthy? (>3x target)
4. What's the full cost structure beyond LLM?
5. When do we break even?
6. What's the cash flow impact of 90-day free trial?

**Dependencies**:
- Wait for Customer Intelligence Agent to deliver ICP and market size
- Need those inputs to model CAC and LTV accurately

---

## Research Objectives

### 1. Customer Acquisition Cost (CAC)

**Objective**: Calculate cost to acquire one board (both channels)

**What to model**:

**Partner-sourced CAC**:
- Partner recruitment cost (sales, onboarding, training)
- Partner enablement cost (materials, support)
- Co-marketing cost
- Partner support cost
- Amortized over: how many boards per partner?

**Direct-sourced CAC**:
- Marketing spend (digital, content, events)
- Sales cost (SDR, AE, SE)
- Trial conversion cost (support, onboarding)
- Directly attributed to: board count

**Research sources**:
- SaaS CAC benchmarks (OpenView, ProfitWell)
- Partner-led CAC vs direct CAC ratios (HubSpot case study)
- B2B SaaS sales cost structures
- Professional services vertical CAC data

**Deliverable**: CAC model with:
```
Partner CAC:
- Partner recruitment: $X per partner
- Partner enablement: $Y per partner
- Average boards per partner: Z
- CAC per board (partner): $X+Y / Z

Direct CAC:
- Marketing: $A per board
- Sales: $B per board
- Onboarding: $C per board
- CAC per board (direct): $A+B+C

Blended CAC (weighted by channel mix)
```

---

### 2. Lifetime Value (LTV)

**Objective**: Calculate lifetime value of one board

**What to model**:

**Revenue per board**:
- Monthly: $149 (or wholesale $79-99 for partner channel)
- Annual: $1,788 (or $948-1,188)

**Churn assumptions**:
- Monthly churn rate: X% (research benchmark)
- Annual retention: (1 - X)^12
- Customer lifetime: 1 / monthly churn

**Gross margin**:
- Revenue per board per month: $149
- COGS per board per month: $Y (calculate below)
- Gross margin: ($149 - $Y) / $149

**LTV formula**:
```
LTV = (Monthly Revenue - Monthly COGS) × Avg Lifetime (months)
```

**Research sources**:
- SaaS churn benchmarks by price point
- B2B vs B2B2B churn differences
- Retention curves (cohort analysis)
- Hardware + software bundled churn (lower than software-only)

**Deliverable**: LTV model with:
- Monthly churn assumption (+ source)
- Average lifetime in months
- Gross margin per board
- LTV per board (partner vs direct)

---

### 3. LTV/CAC Ratio

**Objective**: Validate business viability

**What to calculate**:
```
LTV/CAC Ratio = LTV / CAC

Target: >3x (healthy SaaS business)
Warning: <3x (unit economics don't work)
```

**By channel**:
- Partner channel: LTV/CAC = ?
- Direct channel: LTV/CAC = ?
- Blended: LTV/CAC = ?

**Sensitivity analysis**:
- What if churn is 2x higher?
- What if CAC is 1.5x higher?
- What if LLM costs spike 50%?

**Deliverable**: LTV/CAC analysis with sensitivity scenarios

---

### 4. Gross Margin

**Objective**: Calculate true gross margin (not just LLM cost)

**What to include in COGS**:

**LLM costs**:
- Tokens per @mention (estimate)
- @mentions per board per month (estimate)
- Cost per token (Anthropic pricing)
- Total LLM cost per board per month

**Infrastructure costs**:
- Supabase (database + realtime + storage)
- Compute (serverless functions, API)
- CDN, assets
- Cost per board per month

**Support costs** (if included in COGS):
- Customer success headcount
- Allocated to boards

**Research sources**:
- Anthropic API pricing
- Supabase pricing calculator
- SaaS infrastructure cost benchmarks
- LLM cost optimization strategies

**Deliverable**: Detailed COGS breakdown:
```
COGS per board per month:
- LLM: $X
- Infrastructure: $Y
- Support: $Z (if COGS)
Total COGS: $X + $Y + $Z

Gross Margin: ($149 - Total COGS) / $149 = ?%
Target: >70%
```

---

### 5. Full Cost Structure

**Objective**: Break down ALL costs (not just COGS)

**What to model**:

**COGS** (per board):
- [From above]

**R&D**:
- Engineering team (headcount × salary)
- Product team
- Design team
- Not allocated per board (fixed cost)

**Sales & Marketing**:
- Partner team
- Direct sales team
- Marketing team
- Campaigns, events
- Partially variable (CAC) + partially fixed

**G&A**:
- Finance, legal, HR
- Office, tools
- Fixed cost

**Research sources**:
- Early-stage SaaS cost structure benchmarks (OpenView)
- AI product cost structures
- Headcount-based expense modeling

**Deliverable**: Full P&L structure:
```
Revenue (per board per month): $149
- COGS: $X
= Gross Profit: $Y (Gross Margin: Z%)

- R&D: $A (fixed)
- S&M: $B (CAC + fixed)
- G&A: $C (fixed)
= Operating Income: $Y - A - B - C
```

---

### 6. Break-even Analysis

**Objective**: How many boards to break even?

**What to calculate**:

**Monthly break-even**:
```
Fixed costs per month = R&D + S&M (fixed) + G&A
Contribution margin per board = $149 - COGS - CAC (amortized)
Break-even boards = Fixed costs / Contribution margin
```

**Cumulative break-even**:
- When does cumulative revenue > cumulative costs?
- Accounts for: 90-day free trial, upfront CAC

**Research sources**:
- SaaS break-even timeline benchmarks
- Startup runway analysis

**Deliverable**: Break-even model:
- Monthly break-even: X boards
- Timeline to break-even: Y months
- Sensitivity to CAC, churn, pricing

---

### 7. Cash Flow Impact (90-day Free Trial)

**Objective**: Model cash flow during free trial period

**What to model**:

**Scenario**: GA launch (Month 6), 40K boards get 90-day free trial

**Cash flow**:
- Month 6: 0 revenue, but COGS + fixed costs
- Month 7-8: Still 0 revenue
- Month 9: First revenue from converted trials
- Churn during trial: X% don't convert

**Worst case**:
- High trial adoption (40K boards)
- Low conversion (50%)
- 3 months of negative cash flow

**Research sources**:
- Freemium conversion rate benchmarks
- Long free trial conversion rates (Slack, Notion)
- Cash flow management for free trials

**Deliverable**: Cash flow model:
- Month-by-month cash flow (Month 6-12)
- Cumulative cash position
- Conversion rate assumptions
- Mitigation strategies (if needed)

---

### 8. Price Elasticity (Phase 5)

**Objective**: Understand pricing sensitivity

**What to model**:

**Scenarios**:
- $99/month: +20% adoption, -33% revenue per board
- $149/month: Baseline
- $199/month: -15% adoption, +33% revenue per board

**Impact on**:
- Total revenue
- CAC efficiency (lower price = more volume = lower CAC?)
- LTV/CAC ratio

**Research sources**:
- SaaS pricing elasticity studies
- B2B vs B2C price sensitivity
- Professional services buying behavior

**Deliverable**: Sensitivity table + recommendation

---

## Output Format

**Primary Deliverable**: `docs/v2/validation/UNIT-ECONOMICS-MODEL.md`

**Structure**:
```markdown
# OpenVibe V2: Unit Economics Model

## Executive Summary
- LTV/CAC: X (target: >3)
- Gross Margin: Y% (target: >70%)
- Break-even: Z boards (Month N)
- Assessment: [Viable / Needs work]

## 1. Customer Acquisition Cost (CAC)
### Partner Channel
[Model + assumptions]

### Direct Channel
[Model + assumptions]

### Blended CAC
[Weighted average]

## 2. Lifetime Value (LTV)
### Churn Assumptions
[Benchmark research]

### Revenue Model
[Calculation]

### LTV Calculation
[Result]

## 3. LTV/CAC Analysis
[Ratio + sensitivity]

## 4. Gross Margin
[COGS breakdown]

## 5. Full Cost Structure
[P&L model]

## 6. Break-even Analysis
[Board count + timeline]

## 7. Cash Flow Impact
[90-day trial model]

## 8. Price Elasticity
[Sensitivity analysis]

## 9. Key Insights
[Summary]

## 10. Recommendations
[Strategic implications]
```

**Secondary Deliverable**: Excel/Google Sheets model with:
- Input assumptions (editable)
- Calculation logic
- Output dashboards
- Sensitivity tables

---

## Success Criteria

- [ ] LTV/CAC > 3x (healthy business)
- [ ] Gross margin > 70%
- [ ] Break-even within 18 months
- [ ] Cash flow model shows survival path
- [ ] All assumptions sourced and credible
- [ ] User says: "I trust these numbers"

---

## Timeline

- **Hour 1-2**: Research benchmarks (CAC, LTV, churn, costs)
- **Hour 3-5**: Build CAC model (partner + direct)
- **Hour 6-8**: Build LTV model (churn, revenue, margin)
- **Hour 9-10**: Cost structure and break-even
- **Hour 11-12**: Cash flow model (90-day trial)
- **Hour 13-14**: Sensitivity analysis
- **Hour 15-16**: Document + spreadsheet compilation
- **Day 3**: User review → iteration → finalization

---

## Handoff to User

**Review questions**:
1. Do the CAC assumptions match your GTM plan?
2. Are the churn assumptions realistic? (Too optimistic? Too pessimistic?)
3. Is the COGS breakdown complete? (Any missing costs?)
4. Does the break-even timeline feel achievable?
5. Is the cash flow impact of 90-day free trial manageable?
6. Overall: Is this a viable business?

**Red flags to surface**:
- LTV/CAC < 3x → Unit economics don't work
- Gross margin < 70% → COGS too high
- Break-even > 24 months → Takes too long
- Cash flow negative for >6 months → Funding risk

**Next phase dependency**: GTM Operations needs your CAC model to plan acquisition strategy
