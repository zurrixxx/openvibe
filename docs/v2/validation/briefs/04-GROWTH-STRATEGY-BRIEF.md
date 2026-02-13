# Research Brief: Growth Strategy Agent

**Agent ID**: Growth Strategy Agent
**Phase**: Phase 4 (Day 4-5)
**Priority**: P1 - Important

---

## Mission

Define the growth engine and expansion strategy beyond initial partner GTM.

**Output**: Growth assumptions, growth levers, viral mechanics, network effects, geographic expansion plan

---

## Context

**What we know**:
- 18-month target: 120 partners → 11,500 customers → 34,500 boards → $61M ARR
- Growth rate: Month 1-2 (10 customers) → Month 6 (100-200) → Month 18 (11,500)
- That's 100x growth in 16 months
- Primary driver: Partner network exponential distribution

**What we DON'T know** (your job):
1. What are the explicit assumptions behind this growth model?
2. What growth levers can we pull to accelerate?
3. Is there viral/organic growth potential?
4. What network effects exist?
5. How do we expand beyond initial markets?

**Dependencies**:
- GTM Operations Agent: Acquisition tactics and sales process
- Unit Economics Agent: CAC, LTV, and margin constraints

---

## Research Objectives

### 1. Growth Assumptions (Make Explicit)

**Objective**: Document all implicit assumptions in the 18-month growth model

**What to clarify**:

**Partner Growth Assumptions**:
- Month 1-6: 10 partners (alpha)
- Month 7-12: 40 partners (beta)
- Month 13-18: 70 partners (GA)
- **Assumption checks**:
  - Partner recruitment rate: X partners/month
  - Partner onboarding time: Y days
  - Partner ramp time: Z months to full productivity
  - Partner capacity: Average boards deployed per partner

**End Customer Growth Assumptions**:
- Average boards per customer (from ICP)
- Customer acquisition rate per partner
- Conversion rate (trial → paid)
- Time to first revenue (free trial + sales cycle)

**Churn Assumptions**:
- Monthly churn rate (from Unit Economics)
- Impact on net growth

**Expansion Assumptions**:
- Board expansion within customers (1 → 3 → 5+ boards)
- Expansion revenue contribution

**Research sources**:
- SaaS growth model benchmarks (SaaStr, OpenView)
- Partner-led growth curves (HubSpot trajectory)
- B2B2B expansion patterns

**Deliverable**: Growth assumptions doc with:
- Every assumption listed explicitly
- Source/justification for each
- Sensitivity: "If this assumption is wrong by 50%, what happens?"

---

### 2. Growth Levers (Ranked by Impact)

**Objective**: Identify levers that can accelerate or amplify growth

**What to identify**:

**Primary Levers** (highest impact):
1. **Partner recruitment velocity**: More partners = more distribution
   - Current: X partners/month
   - If 2x: What's the constraint? (Onboarding capacity? Partner supply?)

2. **Partner productivity**: Boards deployed per partner
   - Current: Y boards/partner (average)
   - If 2x: What's the constraint? (Partner capacity? Customer demand?)

3. **Conversion rate**: Trial → paid
   - Current: Z% (assumption)
   - If +10 points: What would it take? (Better onboarding? Feature? Pricing?)

4. **Expansion rate**: Boards per customer over time
   - Current: Start with 1-3, expand to ?
   - If 2x: What drives expansion? (Use case expansion? Team growth?)

**Secondary Levers** (lower impact but worth exploring):
5. **Viral/referral**: Customers refer new customers
6. **Community**: Open source contributors → customers
7. **Product-led growth**: Self-serve sign-up (web)
8. **Geographic expansion**: New markets

**Research sources**:
- SaaS growth lever frameworks (Reforge, First Round)
- Partner ecosystem leverage studies
- PLG + SLG hybrid models

**Deliverable**: Growth levers ranked by:
- Impact potential (high/medium/low)
- Feasibility (easy/medium/hard)
- Timeline (0-6 months / 6-12 months / 12-18 months)

---

### 3. Viral Coefficient

**Objective**: Model word-of-mouth and referral growth potential

**What to calculate**:

**Viral coefficient formula**:
```
Viral Coefficient (k) = (% users who refer) × (avg referrals per user) × (% referred who sign up)

k > 1: Viral growth (each user brings >1 new user)
k < 1: Word-of-mouth but not viral
```

**For OpenVibe**:
- **Scenario 1: Partner referrals**
  - Partners refer other partners (consulting firms talk to each other)
  - Estimate: X% of partners refer, Y referrals each, Z% convert
  - k = ?

- **Scenario 2: End customer referrals**
  - Customers refer other customers (within industry)
  - Estimate: A% of customers refer, B referrals each, C% convert
  - k = ?

- **Scenario 3: User-to-customer** (individual users advocate)
  - End users love it, convince their org to buy more boards
  - Contribution to expansion revenue

**Research sources**:
- Viral growth case studies (Dropbox, Slack, Notion)
- B2B viral coefficient research (typically k < 1, but valuable)
- Referral program best practices

**Deliverable**: Viral model with:
- k calculation for each scenario
- Referral program recommendations (if k > 0.5)
- Impact on growth projections

---

### 4. Network Effects

**Objective**: Identify and quantify network effects

**What to analyze**:

**Types of network effects**:

1. **Direct network effects** (same-side):
   - More users in a workspace → more value for each user
   - Mechanism: More context, more knowledge, better agent
   - Strength: High (core to product thesis)

2. **Cross-side network effects** (multi-sided):
   - More end customers → more partners attracted
   - More partners → more end customers reached
   - Mechanism: Ecosystem reinforcement
   - Strength: Medium

3. **Data network effects**:
   - More workspaces → more data → better agent training
   - Mechanism: Cross-workspace learning (respecting privacy)
   - Strength: Medium-High (long-term moat)

4. **Vertical network effects**:
   - Consulting firms using OpenVibe for clients → clients adopt
   - Mechanism: Industry-specific flywheel
   - Strength: Medium

**Research sources**:
- Network effects frameworks (NFX, Andreessen Horowitz)
- Marketplace network effects (even though OpenVibe isn't a marketplace)
- Data moat case studies (Waze, Google Maps)

**Deliverable**: Network effects analysis with:
- Each type identified
- Mechanism explained
- Strength estimated
- Timeline to activation (when does it kick in?)
- Strategic implications

---

### 5. Geographic Expansion

**Objective**: Plan expansion beyond initial English-speaking markets

**What to define**:

**Phase 1: English-speaking markets** (Year 1)
- US (primary)
- UK, Canada, Australia (secondary)

**Phase 2: Western Europe** (Year 2)
- Germany, France, Netherlands
- Partner network expansion
- Localization requirements (language, compliance)

**Phase 3: APAC** (Year 2-3)
- Singapore, Hong Kong, Japan
- Different partner ecosystems
- Data residency requirements

**Expansion strategy**:
- When to expand? (Metric-driven: X% market share in US before expanding)
- How to expand? (Partner-led in each market)
- What changes? (Localization, compliance, payment)

**Research sources**:
- SaaS international expansion playbooks
- B2B2B cross-border strategies
- Data sovereignty & compliance by region

**Deliverable**: Geographic expansion plan with:
- Market prioritization (which countries first)
- Timeline (when to enter each)
- Partner strategy by region
- Localization requirements
- Regulatory considerations (GDPR, data residency)

---

### 6. Growth Stage Playbooks

**Objective**: Define what changes at each growth stage

**What to define**:

**Alpha (Month 1-2): 10 customers**
- Focus: Product-market fit validation
- Growth lever: Partner co-development
- Metric: Acceptance rate, room return rate

**Beta (Month 3-5): 100-200 customers**
- Focus: Partner network launch
- Growth lever: Partner recruitment
- Metric: Partner sign-ups, first deployments

**GA (Month 6): 500-1,000 customers**
- Focus: Firmware push + self-serve
- Growth lever: 40K board activation + direct web sign-up
- Metric: Trial conversion, churn

**Scale (Month 7-12): 1,000-5,000 customers**
- Focus: Partner productivity + expansion revenue
- Growth lever: Partner enablement + upsell
- Metric: Boards per partner, expansion rate

**Maturity (Month 13-18): 5,000-11,500 customers**
- Focus: Efficiency + new verticals
- Growth lever: Marketing + new partner verticals
- Metric: CAC payback, LTV/CAC

**Research sources**:
- Stage-based growth strategies (Reforge)
- 0-1 vs 1-10 vs 10-100 playbooks

**Deliverable**: Playbook by stage with:
- Focus for that stage
- Primary growth lever
- Key metric
- What changes vs previous stage

---

## Output Format

**Deliverable**: `docs/v2/validation/GROWTH-STRATEGY.md`

**Structure**:
```markdown
# OpenVibe V2: Growth Strategy

## Executive Summary
[Growth model, key levers, timeline]

## 1. Growth Assumptions
### 1.1 Explicit Assumptions
[Every assumption documented]

### 1.2 Sensitivity Analysis
[What if assumptions are wrong?]

## 2. Growth Levers
### 2.1 Primary Levers
[Top 4, ranked by impact]

### 2.2 Secondary Levers
[Next 4, for later stages]

## 3. Viral Mechanics
### 3.1 Viral Coefficient
[k calculation]

### 3.2 Referral Programs
[Recommendations]

## 4. Network Effects
### 4.1 Direct Network Effects
[Analysis]

### 4.2 Cross-side Network Effects
[Analysis]

### 4.3 Data Network Effects
[Analysis]

### 4.4 Vertical Network Effects
[Analysis]

## 5. Geographic Expansion
### 5.1 Phase 1: English Markets
[US, UK, CA, AU]

### 5.2 Phase 2: Europe
[Timeline, partners, localization]

### 5.3 Phase 3: APAC
[Timeline, partners, compliance]

## 6. Growth Stage Playbooks
### 6.1 Alpha (Month 1-2)
[Focus, lever, metric]

[... all stages]

## 7. Key Insights
[Summary]

## 8. Recommendations
[Strategic implications]
```

---

## Success Criteria

- [ ] Growth assumptions are explicit (no hidden assumptions)
- [ ] Growth levers are ranked and actionable
- [ ] Viral coefficient is calculated (even if <1)
- [ ] Network effects are identified and explained
- [ ] Geographic expansion is phased and realistic
- [ ] User says: "I understand how we grow"

---

## Timeline

- **Hour 1-2**: Research growth frameworks and case studies
- **Hour 3-5**: Document explicit assumptions + sensitivity
- **Hour 6-8**: Identify and rank growth levers
- **Hour 9-11**: Model viral coefficient and network effects
- **Hour 12-14**: Geographic expansion plan
- **Hour 15-16**: Growth stage playbooks
- **Day 5**: User review → iteration → finalization

---

## Handoff to User

**Review questions**:
1. Are all growth assumptions explicit and justified?
2. Do the growth levers make sense? (Any missing?)
3. Is the viral coefficient calculation realistic?
4. Do the network effects analyses resonate?
5. Is the geographic expansion timeline appropriate?
6. Are the stage-based playbooks actionable?

**Next phase dependency**: Resource Planning Agent needs growth model to plan hiring and budget
