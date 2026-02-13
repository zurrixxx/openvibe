# Research Brief: Customer Intelligence Agent

**Agent ID**: Customer Intelligence Agent
**Phase**: Phase 1 (Day 1-2)
**Priority**: P0 - Critical

---

## Mission

Develop a complete understanding of WHO buys OpenVibe, WHY they buy, and HOW they make the decision.

**Output**: End customer ICP, purchase decision chain, use case stories, market size model

---

## Context

**What we know**:
- GTM is partner-led (consulting, accounting, MSPs)
- Partners deploy to 50-200 end customers each
- Pricing: $149/month/board
- Product: AI workspace for human+agent collaboration
- Competition: Anthropic Cowork, Microsoft Copilot, Slack AI

**What we DON'T know** (your job):
1. Who is the end customer? (Beyond "professional services firms")
2. Who actually signs the contract?
3. What pain are they trying to solve?
4. How do they make the buying decision?
5. What are the specific use cases that drive adoption?

---

## Research Objectives

### 1. End Customer ICP (3-tier)

**Objective**: Define personas for 3 key stakeholders

**What to research**:
- **Economic Buyer** (signs the contract)
  - Title? Role? Department?
  - What budget line does this come from?
  - What are their success metrics?
  - What are their fears/objections?

- **Champion** (advocates internally)
  - Title? Role?
  - Why do they care?
  - What do they gain if this succeeds?
  - What tools do they use today?

- **End User** (uses the product daily)
  - Title? Role?
  - Daily workflow?
  - Current pain points?
  - What would make them love this?

**Research sources**:
- Professional services firm org structures
- AI adoption case studies (McKinsey, BCG reports)
- Competitive customer profiles (Cowork, Copilot early adopters)
- V1 Slack pain data (1,097 threads) - what patterns exist?

**Deliverable**: 3 detailed persona cards with:
- Demographics (title, role, company size)
- Goals & success metrics
- Pain points (current state)
- Buying criteria (what they evaluate)
- Objections & fears

---

### 2. Purchase Decision Chain

**Objective**: Map the decision process for BOTH partner and end customer

**What to research**:

**Partner decision** (consulting firm decides to resell OpenVibe):
- Who evaluates? (Partner leadership? Practice lead?)
- What's the decision criteria?
- How long does it take?
- What proof do they need?

**End customer decision** (client decides to adopt):
- Who initiates? (Partner recommends, or client requests?)
- Who evaluates? (Champion, IT, procurement?)
- Who has veto power?
- What's the approval process?
- How long from first demo to contract signed?

**Research sources**:
- HubSpot partner-led sales case studies
- B2B SaaS buying process research (Gartner, Forrester)
- Professional services procurement processes
- GitLab channel sales playbook

**Deliverable**: 2 decision flowcharts:
1. Partner sign-up decision flow (lead → evaluation → contract)
2. End customer adoption decision flow (recommendation → trial → purchase)

Include: stakeholders, timeline, decision criteria, common blockers

---

### 3. Core Use Case Stories

**Objective**: Develop 5 specific "day in the life" scenarios

**What to create**:
Each story should include:
- Persona (from ICP above)
- Situation (what triggers the need?)
- Current state (painful manual process)
- With OpenVibe (how it helps)
- Outcome (measurable value)

**5 scenarios to develop**:
1. **Consulting engagement** - Strategy team using AI for client work
2. **Internal collaboration** - Accounting firm using AI for internal projects
3. **Client service** - MSP using AI for customer support
4. **Remote team** - Distributed team async collaboration
5. **Board meeting** - Leadership using physical board + AI workspace

**Research sources**:
- Professional services workflow documentation
- Knowledge work case studies
- AI productivity case studies (McKinsey, Bain)
- Vibe board customer stories

**Deliverable**: 5 detailed use case stories (300-500 words each) following this format:
```
## Use Case: [Name]
**Persona**: [Which ICP?]
**Frequency**: [Daily/Weekly/Monthly]

### Before OpenVibe
[Current painful state - specific details]

### With OpenVibe
[Step-by-step walkthrough]

### Outcome
[Quantified value - time saved, quality improved, etc.]
```

---

### 4. Market Size (TAM/SAM/SOM)

**Objective**: Calculate addressable market in DOLLARS (not just user counts)

**What to calculate**:

**TAM (Total Addressable Market)**:
- Global professional services firms with 50+ employees
- Number of firms × average boards per firm × $149/mo × 12
- Research sources: IBISWorld, Statista, industry reports

**SAM (Serviceable Addressable Market)**:
- Firms in English-speaking markets (US, UK, AU, CA)
- With existing Vibe board install base (40K boards)
- Partner-reachable firms (consulting, accounting, MSPs)

**SOM (Serviceable Obtainable Market)**:
- Realistic market share in 18 months
- Based on: 120 partners × 96 boards avg × $149/mo
- Validate against: partner capacity, competitive share

**Research sources**:
- Professional services industry reports
- Vibe board install base data
- Competitive market share (Slack, Teams, Notion market share as proxy)
- SaaS market penetration benchmarks

**Deliverable**: Market size model with:
- TAM/SAM/SOM in $ (annual)
- Assumptions documented
- Competitive share estimates
- Sensitivity analysis

---

## Research Methodology

### Primary Research
- [ ] Analyze V1 Slack pain data (what patterns exist?)
- [ ] Review Vibe board customer profiles (who bought boards?)
- [ ] Study Anthropic Cowork early customer profiles

### Secondary Research
- [ ] Professional services industry reports (McKinsey, BCG, Gartner)
- [ ] AI adoption case studies
- [ ] B2B SaaS buying process research
- [ ] Partner-led GTM case studies (HubSpot, GitLab)
- [ ] Market size reports (IBISWorld, Statista)

### Validation
- [ ] Cross-check ICP against V1 data
- [ ] Validate decision chain with partner GTM experience
- [ ] Validate use cases against Slack pain points
- [ ] Sanity-check market size against industry benchmarks

---

## Output Format

**Deliverable**: `docs/v2/validation/CUSTOMER-FOUNDATION.md`

**Structure**:
```markdown
# OpenVibe V2: Customer Foundation

## 1. End Customer ICP
### 1.1 Economic Buyer
[Detailed persona]

### 1.2 Champion
[Detailed persona]

### 1.3 End User
[Detailed persona]

## 2. Purchase Decision Chain
### 2.1 Partner Decision Process
[Flowchart + narrative]

### 2.2 End Customer Decision Process
[Flowchart + narrative]

## 3. Core Use Case Stories
### 3.1 Consulting Engagement
[Story]

[... 4 more stories]

## 4. Market Size Model
### 4.1 TAM
[Calculation + assumptions]

### 4.2 SAM
[Calculation + assumptions]

### 4.3 SOM
[Calculation + assumptions]

## 5. Key Insights
[Summary of findings]

## 6. Recommendations
[Strategic implications]
```

---

## Success Criteria

- [ ] ICP feels REAL (not generic personas)
- [ ] Decision chain has specific timeline and stakeholders
- [ ] Use case stories are concrete and measurable
- [ ] Market size is credible (validated against benchmarks)
- [ ] User says: "This matches reality"

---

## Timeline

- **Hour 1-2**: Secondary research (industry reports, case studies)
- **Hour 3-4**: ICP development
- **Hour 5-6**: Decision chain mapping
- **Hour 7-8**: Use case story writing
- **Hour 9-10**: Market size calculation
- **Hour 11-12**: Draft document compilation
- **Day 2**: User review → iteration → finalization

---

## Handoff to User

**Review questions for user**:
1. Do these personas match your mental model of the customer?
2. Is the decision chain realistic based on your GTM experience?
3. Do the use case stories resonate? Are they specific enough?
4. Does the market size feel credible?
5. What's missing?

**Next phase dependency**: Unit Economics Agent needs your ICP and market size to model CAC/LTV
