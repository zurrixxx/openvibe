# OpenVibe V2: Risk & Controls

> Created: 2026-02-10
> Status: Active
> Prerequisites: Read `THESIS.md` and `STRATEGY.md` first

---

## Executive Summary

This document defines OpenVibe's risk management framework and decision-making protocols for V2 execution.

**Risk Posture**: Medium-High technical risk, High competitive risk, Medium GTM risk.

**Critical Controls**:
1. **Agent Output Quality** - Default passive, human-in-loop for all L1-L2 trust actions
2. **Cost Management** - Token usage budgets per board ($30-50/month ceiling)
3. **Competitive Speed** - 6-month GA timeline (before Anthropic ships team features)
4. **Partner Deployment** - First 5 client deployments hands-on per partner

**Decision Authority**: RACI matrix defines who decides what at each stage gate.

---

## 1. Technical Risk Register

### Infrastructure Risks

#### R1: LLM API Reliability
**Description**: Anthropic/OpenAI API downtime renders product unusable.

**Impact**: Very High (product breaks, customers cannot work)

**Likelihood**: Low-Medium (major providers have 99.9%+ uptime, but outages happen)

**Mitigation**:
- Multi-model fallback: If Anthropic API down → route to OpenAI → route to Google
- Graceful degradation: Agent features temporarily disabled, human workspace still functional
- Caching: Recent responses cached 5 minutes (reduces API dependency for repeated queries)
- SLA monitoring: Real-time API health dashboard, auto-failover within 30 seconds

**Owner**: Engineering Manager

**Review Frequency**: Weekly (during build), Monthly (post-GA)

**Sources**: [LLM Security Risks 2026](https://sombrainc.com/blog/llm-security-risks-2026), [MLOps Roadmap 2026](https://medium.com/@sanjeebmeister/the-complete-mlops-llmops-roadmap-for-2026-building-production-grade-ai-systems-bdcca5ed2771)

---

#### R2: LLM Cost Spike
**Description**: Token costs increase 2-5x due to pricing changes, usage spike, or extended thinking overuse.

**Impact**: Very High (margins evaporate, $149/board pricing becomes unprofitable)

**Likelihood**: Medium (Anthropic Sonnet 4.5 currently $3/$15 per million tokens; historical trend shows price increases for new model versions)

**Mitigation**:
- **Usage limits per board**: Hard cap at 2M tokens/month per board (~$60 cost at Sonnet rates)
- **Model routing**: Haiku ($1/$5) for summaries, Sonnet for @mentions, Opus only for deep dives
- **Token budgeting dashboard**: Real-time per-board consumption tracking, alerts at 80% threshold
- **Pricing hedge**: $149 price point includes 100% margin buffer ($30-50 estimated → $60 cap → $89 margin)
- **Annual contract option**: Lock in LLM pricing via OpenAI/Anthropic reseller agreements

**Cost Breakdown** (per board, per month):
- Baseline (Sonnet): ~$30-50 (20 @mentions/day × 50K tokens avg × 30 days)
- Spike scenario (Opus overuse): ~$80-120 (if users exclusively use deep dives)
- Hard cap: $60 enforced at application layer

**Owner**: CTO + Finance

**Review Frequency**: Weekly (monitor actuals vs estimates)

**Sources**: [Anthropic API Pricing 2026](https://www.nops.io/blog/anthropic-api-pricing/), [LLM Cost Per Token Guide](https://www.silicondata.com/blog/llm-cost-per-token), [Complete LLM Pricing Comparison](https://www.cloudidr.com/blog/llm-pricing-comparison-2026)

---

#### R3: Supabase Scaling Limits
**Description**: Supabase Realtime cannot scale to 34,500 boards (GA scenario) with acceptable performance.

**Impact**: Medium-High (latency increases, messages delayed, poor UX)

**Likelihood**: Low (Supabase benchmarks show capability for millions of concurrent connections; OpenVibe's 34,500 boards = ~100K peak concurrent users at 3 users/board avg)

**Mitigation**:
- **Load testing Sprint 4**: Simulate 50K concurrent users, 100 boards/sec message rate
- **Supabase Pro tier**: Dedicated compute instance (not shared), supports 500 concurrent DB connections
- **Connection pooling**: PgBouncer (Supavisor) handles 1M+ connections with connection reuse
- **Fallback plan**: If Realtime bottlenecks, migrate to self-hosted Supabase (open source) on AWS/GCP with horizontal scaling
- **Read replicas**: For read-heavy queries (context assembly, message history), use Postgres read replicas

**Performance Targets**:
- Message latency: <200ms p50, <500ms p99
- Connection success rate: >99.5%
- Peak concurrent users: 100K (3× buffer over 34,500 board scenario)

**Owner**: Engineering Manager

**Review Frequency**: Sprint 4 (load test), Monthly post-GA

**Sources**: [Supabase Realtime Benchmarks](https://supabase.com/docs/guides/realtime/benchmarks), [Supavisor: Scaling to 1M Connections](https://supabase.com/blog/supavisor-1-million)

---

#### R4: Board SDK Constraints
**Description**: Vibe board SDK cannot support required features (live-updating agent cards, touch interaction, real-time rendering).

**Impact**: Medium (board features delayed to Year 2, web-only launch acceptable)

**Likelihood**: Medium (SDK is new, capabilities unproven for agent UI patterns)

**Mitigation**:
- **Sprint 3 feasibility spike** (already planned): 2 engineers, 1 week
  - Validate: Live-updating cards (agent response streaming)
  - Validate: Touch interaction (tap card → expand, swipe → dismiss)
  - Validate: Performance (<500ms card render, 60fps scrolling)
- **Go/No-Go Gate**: If spike fails → defer board to Sprint 8+ (Month 7+), web-only GA acceptable
- **Fallback design**: Static agent cards (no live updates), tap → open web view in browser

**Decision Criteria** (Sprint 3 Gate):
- [ ] Live-updating cards confirmed (Yes/No)
- [ ] Touch interaction confirmed (Yes/No)
- [ ] Performance acceptable (<500ms)
- **If 2+ No → Web-only GA, defer board**

**Owner**: CTO + Engineering Manager

**Review Frequency**: Sprint 3 (spike results), revisit Sprint 7 if deferred

**Sources**: [Stage-Gate Model Overview](https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/)

---

### Security Risks

#### R5: Agent Output Vulnerabilities
**Description**: Agent generates harmful, incorrect, or inappropriate output (hallucinations, biased responses, confidential data leaks).

**Impact**: Very High (trust violation → customer churn → reputational damage)

**Likelihood**: Medium (AI outputs inherently unpredictable; prompt injection and jailbreaks are common attacks)

**Mitigation**:
- **Default passive**: Agents listen and prepare, do NOT post to channels unless explicitly @mentioned
- **Human-in-loop (L1-L2)**: Trust Level 1-2 actions require human approval (no autonomous posting, editing, deleting)
- **Output validation**: Regex filters for patterns (API keys, passwords, PII), redact before display
- **SOUL constraints**: Agent SOUL includes explicit prohibitions (no financial advice, no medical advice, no legal advice)
- **Streaming w/ progressive disclosure**: Human sees headline/summary before full output, can cancel mid-stream
- **Monitoring**: Log all agent outputs, flag anomalies (profanity, sensitive keywords), daily review in Alpha/Beta
- **Feedback loop**: Thumbs down → human review → update SOUL/prompts if pattern detected

**Monitoring Metrics**:
- Unhelpful rating >40% → Kill signal (existential risk)
- User cancellations >25% → Output quality issue
- Redacted outputs >5% → PII leakage pattern

**Owner**: Head of Product + Engineering Manager

**Review Frequency**: Daily (Alpha/Beta), Weekly (GA)

**Sources**: [OWASP AI Agent Security](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html), [LLM Security Risks 2026](https://www.uscsinstitute.org/cybersecurity-insights/blog/what-are-llm-security-risks-and-mitigation-plan-for-2026)

---

#### R6: Data Breach
**Description**: Customer data leaked (conversation history, SOUL configs, knowledge bases, API keys).

**Impact**: Existential (company-ending reputational damage, regulatory penalties, customer exodus)

**Likelihood**: Low (with proper security controls)

**Mitigation**:
- **Encryption**: All data encrypted at rest (AES-256) and in transit (TLS 1.3)
- **Access controls**: Row-level security (RLS) in Supabase, users only access own workspace data
- **API key storage**: Encrypted in database, decrypted only at runtime in memory, never logged
- **SOC 2 Type II**: Target Month 12 (required for enterprise sales)
- **Penetration testing**: Annual external audit (start Month 9)
- **GDPR/CCPA compliance**: Data deletion endpoints, export functionality, consent management
- **Incident response plan**: CTO owns response, 24-hour breach notification SLA, customer communication templates pre-written

**Compliance Timeline**:
- Month 6 (GA): GDPR-compliant (data export, deletion)
- Month 9: Penetration test #1
- Month 12: SOC 2 Type II audit begins
- Month 18: SOC 2 certification complete

**Owner**: CTO

**Review Frequency**: Quarterly (security audit), Annual (pen test)

**Sources**: [AI Governance & Emerging Risks 2026](https://www.corporatecomplianceinsights.com/2026-operational-guide-cybersecurity-ai-governance-emerging-risks/)

---

#### R7: Prompt Injection
**Description**: User crafts malicious prompt that hijacks agent behavior (data exfiltration, unauthorized actions, jailbreak constraints).

**Impact**: Medium-High (agent misbehaves, leaks data from other users' contexts)

**Likelihood**: Medium-High (prompt injection is #1 OWASP risk for LLMs, no foolproof prevention exists)

**Mitigation**:
- **Input sanitization**: Strip/escape special characters, detect jailbreak patterns ("ignore previous instructions")
- **SOUL constraints hardened**: System prompt explicitly prohibits data disclosure, unauthorized tool use
- **Context isolation**: Agent sees only current workspace data (RLS enforced), cannot access other workspaces
- **Trust levels**: L1-L2 agents cannot execute tools autonomously (read-only), L3-L4 require explicit user configuration
- **Monitoring**: Log all tool calls, flag anomalies (unusual API calls, data volume), auto-block suspicious patterns
- **Rate limiting**: Max 50 @mentions/hour per user (prevents brute-force jailbreak attempts)

**Known Attack Vectors**:
- Indirect injection via external data (user pastes malicious text from web → agent processes)
- Tool poisoning (user adds malicious tool, agent executes)
- Memory poisoning (user provides false info, agent remembers, affects future sessions)

**Mitigation for Each**:
- External data: Prefix with "The following is untrusted user input: [...]" in prompt
- Tool poisoning: Admin-only tool configuration (non-admins cannot add tools)
- Memory poisoning: Episodic memory includes source attribution, admin can delete memories

**Owner**: Engineering Manager + Security Lead (hire Month 9)

**Review Frequency**: Weekly (Alpha/Beta), Monthly (GA), Quarterly (red team exercises)

**Sources**: [OWASP Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), [Prompt Injection: Most Common AI Exploit 2025](https://www.obsidiansecurity.com/blog/prompt-injection)

---

### Technical Debt Risks

#### R8: Monolith Migration Pressure
**Description**: Monolith architecture cannot scale beyond 50K boards, forced microservices migration mid-growth disrupts engineering.

**Impact**: Medium (6-12 month engineering distraction, velocity drops 50%)

**Likelihood**: Low (monolith proven to 100K+ users for similar apps; Instagram served 100M users on Django monolith)

**Mitigation**:
- **Design for modularity**: Nx monorepo with clear package boundaries (core, web, board, connectors)
- **Defer until proven need**: No preemptive microservices. Migrate only if >50K boards AND performance issues proven
- **Migration path**: If needed, extract high-load services first (agent inference, context assembly) → AWS Lambda/GCP Cloud Run
- **Do not optimize prematurely**: 5-10 engineers can maintain monolith comfortably for 12-18 months

**Decision Criteria** (future):
- IF boards >50K AND p99 latency >2s AND scaling attempts exhausted → Consider migration
- ELSE → Stay monolith

**Owner**: CTO

**Review Frequency**: Quarterly (Month 9+)

**Sources**: [MLOps Roadmap 2026](https://medium.com/@sanjeebmeister/the-complete-mlops-llmops-roadmap-for-2026-building-production-grade-ai-systems-bdcca5ed2771)

---

#### R9: Context Window Overflow
**Description**: Context assembly exceeds model limits (200K tokens for Claude Sonnet 4.5), agent cannot process full context.

**Impact**: Low (graceful degradation designed into system)

**Likelihood**: Very High (will happen regularly for long conversations, large knowledge bases)

**Mitigation**:
- **Priority stack** (already designed in `PERSISTENT-CONTEXT.md`):
  - Tier 1: SOUL + current message + conversation (last 50 msgs) → Always included
  - Tier 2: Episodic memory (recent corrections, preferences) → Included if space
  - Tier 3: Knowledge base (search results) → Included if space
  - Tier 4: Deep dive history → Included if space
- **Sliding window**: For conversations >50 messages, keep most recent 25 + conversation summary + oldest 25
- **Summarization**: Every 100 messages, LLM generates conversation summary (500 tokens), replaces old messages
- **Vector search**: Knowledge base uses semantic search (top 5 relevant docs), not full corpus
- **Token budgeting**: Pre-calculate context size before LLM call, truncate Tier 3-4 if needed

**Operational Strategy**: Accept that context will be incomplete for very long threads. Users can explicitly reference past messages ("see message from Feb 3") → agent fetches specific message.

**Owner**: Engineering Manager

**Review Frequency**: Sprint 4 (implement), Monthly (monitor truncation rates)

**Sources**: [Context Window Management Strategies](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/), [Fix AI Agents Missing Critical Details](https://datagrid.com/blog/optimize-ai-agent-context-windows-attention)

---

## 2. Decision Gates

Decision gates define "proceed or pivot" moments in the roadmap.

### Gate 1: After Alpha (Month 2)

**Key Question**: Do we have product-market fit signal?

**Go Criteria**:
- [ ] @mention rate >2 per person per day (indicates usefulness)
- [ ] Agent acceptance rate ≥60% (indicates output quality)
- [ ] Deep dives created ≥5 per week (indicates feature valued)
- [ ] "Would miss it if gone" ≥60% (indicates product essential)
- [ ] Zero critical bugs (P0 blockers)

**Go Decision**: Proceed to Beta (recruit 10 partners, plan GA)

**No-Go Decision**: Extend Alpha 4 weeks, iterate on:
- Output quality (if acceptance rate <60%)
- Agent UX (if @mention rate <2/day)
- Feature value (if deep dives <5/week)

**Who Decides**: CEO + CTO + Head of Product (unanimous)

**Timeline**: Week 8 review

**Sources**: [Stage-Gate Process Guide](https://www.intellectsoft.net/blog/stage-gate-process/), [Go/No-Go Decision Framework](https://www.summitstrategywins.com/blog-posts/its-called-a-go-no-go-process-for-a-reason-five-areas-to-evaluate-before-pursuing-your-next-project)

---

### Gate 2: After Beta (Month 5)

**Key Question**: Is partner GTM working?

**Go Criteria**:
- [ ] 10+ partners signed (validated demand)
- [ ] 50+ client deployments (partners actually deploying)
- [ ] Partner NPS >50 (partners satisfied)
- [ ] Average boards/partner ≥20 (economics work for partners)
- [ ] Trial conversion ≥20% (product converts)
- [ ] Churn <10% monthly (product retains)

**Go Decision**: Proceed to GA (firmware push to 40K boards, open partner recruitment)

**No-Go Decision**: Delay GA 8 weeks, fix:
- Partner onboarding (if <5 deployments/partner)
- Product-market fit (if trial conversion <20% or churn >10%)
- Partner economics (if boards/partner <20)

**Who Decides**: CEO + Head of GTM (CEO has final say)

**Timeline**: Week 20 review

**Sources**: [Stage-Gate Model Applications](https://www.launchnotes.com/glossary/stage-gate-model-in-product-management-and-operations)

---

### Gate 3: After Board SDK Spike (Sprint 3, Week 8)

**Key Question**: Is board integration technically feasible?

**Go Criteria**:
- [ ] Live-updating agent cards confirmed (streaming response updates card in real-time)
- [ ] Touch interaction confirmed (tap to expand, swipe to dismiss, pinch to zoom)
- [ ] Performance acceptable (card render <500ms, 60fps scrolling, no jank)

**Go Decision**: Proceed with board features Sprint 5 (70% engineering on web, 20% on board, 10% connectors)

**No-Go Decision**: Web-only GA (defer board to Year 2 or never). Acceptable fallback.

**Alternative**: Partial board features (static cards, no live updates), revisit Sprint 7.

**Who Decides**: CTO + Engineering Manager (technical decision, no CEO needed)

**Timeline**: Week 8 (Sprint 3 end)

**Sources**: [Phase-Gate Process Guide](https://lucid.co/blog/phase-gate-process)

---

### Gate 4: After GA (Month 9)

**Key Question**: Are we hitting growth targets?

**Go Criteria**:
- [ ] **Acceptance rate improved** (M9 > M3) → Most critical metric (thesis validation)
- [ ] Trial conversion ≥30% (product converts at scale)
- [ ] Churn <5% monthly (product retains)
- [ ] 500+ paying customers (demand validated)
- [ ] Partner-sourced revenue >40% (GTM model working)

**Go Decision**: Scale aggressively (hire 20 more people, increase marketing spend 3x)

**No-Go Decision**: Diagnose issues, slow hiring:
- If acceptance rate flat → Feedback loop broken (existential)
- If conversion <30% → Pricing or value prop issue
- If churn >5% → Product not sticky enough
- If partner revenue <40% → GTM model failing

**Who Decides**: CEO + Board (CEO recommends, Board approves budget)

**Timeline**: Month 9 board meeting

**Sources**: [SaaS Go/No-Go Criteria](https://www.summitstrategywins.com/blog-posts/its-called-a-go-no-go-process-for-a-reason-five-areas-to-evaluate-before-pursuing-your-next-project)

---

### Gate 5: After 12 Months

**Key Question**: Is this a venture-scale business?

**Go Criteria**:
- [ ] $10M+ ARR run-rate (venture scale)
- [ ] LTV/CAC >3x (unit economics healthy)
- [ ] Partner channel >50% of revenue (GTM moat proven)
- [ ] Net Revenue Retention (NRR) >100% (customers expanding)
- [ ] Acceptance rate M12 > M6 (workspace getting smarter over time)

**Go Decision**: Raise Series A ($20-40M), scale internationally, hire 50-100 people, build purpose-built AI board

**No-Go Decision**: Operate profitably (burn <$100K/month), revisit strategy in 6 months. Options:
- Niche down (vertical-specific: consulting firms only)
- Pivot (different customer segment)
- Acquihire (team + technology acquisition)

**Who Decides**: CEO + Board (Board has final say on fundraising)

**Timeline**: Month 12 board meeting

**Sources**: [Stage-Gate Tools & Techniques](https://www.bpminstitute.org/resources/articles/stage-gate-process-tools-techniques-within-enterprise-excellence/)

---

## 3. Decision Authority Matrix (RACI)

**Legend**:
- **R** (Responsible): Does the work
- **A** (Accountable): Final decision, approves
- **C** (Consulted): Provides input before decision
- **I** (Informed): Told after decision

### Product Decisions

| Decision | CEO | CTO | Head of Product | Eng Manager | PM | Designer |
|----------|-----|-----|-----------------|-------------|----|----|
| Feature prioritization | C | C | **A** | C | **R** | I |
| Design direction | C | - | A | - | C | **R** |
| Technical architecture | C | **A** | - | **R** | - | - |
| Trust level defaults | **A** | C | R | - | - | - |
| Agent SOUL templates | C | C | **A** | - | R | - |
| Sprint scope | I | C | **A** | R | R | I |

### GTM Decisions

| Decision | CEO | Head of GTM | PSM | Marketing Lead |
|----------|-----|-------------|-----|----------------|
| Partner pricing | **A** | **R** | C | I |
| Partner selection | C | **A** | **R** | I |
| Marketing budget allocation | **A** | C | - | **R** |
| Sales collateral | I | C | R | **A** |
| Partner certification criteria | C | **A** | **R** | I |
| Event sponsorships >$10K | **A** | R | - | C |

### Financial Decisions

| Decision | CEO | CFO/Finance | Dept Head |
|----------|-----|-------------|-----------|
| Hiring (budget approved) | C | I | **A** (within budget) |
| Hiring (off-budget) | **A** | C | R |
| Spending <$10K | I | - | **A** |
| Spending $10K-$50K | **A** | C | R |
| Spending >$50K | **A** (recommends) | C | R (Board approves) |
| Annual budget | **A** (recommends) | **R** | C (Board approves) |

### Strategic Decisions

| Decision | CEO | CTO | Board |
|----------|-----|-----|-------|
| Pricing changes | **A** | C | I |
| Pivot/persevere at gates | **A** (recommends) | C | **A** (final) |
| Fundraising | **A** (leads) | C | **A** (approves) |
| Acquisition offers | R | C | **A** |
| Kill signal response | **A** | C | I |

### Risk & Operations

| Decision | CEO | CTO | Head of GTM | Eng Manager |
|----------|-----|-----|-------------|-------------|
| Security incident response | I | **A** | - | **R** |
| API provider change | C | **A** | - | R |
| Customer data deletion | I | **A** | C | R |
| Service outage communication | C | **A** | C | R |

### Key Principles

1. **Single Accountable**: Only one "A" per decision (prevents diffusion of responsibility)
2. **Default to Dept Head**: Department heads are Accountable for decisions within their domain
3. **CEO Override**: CEO can override any decision but should rarely do so (trust your leaders)
4. **Board for Scale**: Board approves decisions with >$50K spend or strategic impact
5. **Weekly Review**: If decisions are slow, review RACI assignments (may need rebalancing)

**Sources**: [RACI Matrix Guide](https://project-management.com/understanding-responsibility-assignment-matrix-raci-matrix/), [RACI for Startups](https://www.meegle.com/en_us/topics/raci-matrix/raci-matrix-for-startups), [Using RACI for Decision Authority](https://www.onpointconsultingllc.com/blog/raci-matrix-decision-authority-in-a-team)

---

## 4. Cross-Validation

**Status**: ⚠️ Pending other validation documents

This section validates consistency across all agent outputs from the strategy validation exercise.

### Required Dependencies

To complete cross-validation, the following documents must exist:
1. ❌ `CUSTOMER-FOUNDATION.md` (Customer Intelligence Agent)
2. ❌ `UNIT-ECONOMICS-MODEL.md` (Unit Economics Agent)
3. ❌ `GTM-EXECUTION-PLAN.md` (GTM Operations Agent)
4. ❌ `GROWTH-STRATEGY.md` (Growth Strategy Agent)
5. ❌ `RESOURCES-AND-BUDGET.md` (Resource Planning Agent)

### Planned Cross-Checks

Once dependencies complete, validate:

#### Customer Intelligence ↔ Unit Economics
- [ ] ICP (Ideal Customer Profile) matches CAC assumptions
  - **What to check**: If ICP is "management consulting firms with 20-200 clients", CAC model should reflect partner acquisition costs, not end-customer acquisition
- [ ] Market size (5K-15K orgs in Q1 2026) matches revenue projections

#### Unit Economics ↔ GTM Operations
- [ ] CAC model matches acquisition strategy
  - **What to check**: If GTM is partner-led, CAC should include partner commission, training costs, not direct sales salaries
- [ ] Marketing budget matches CAC targets
  - **What to check**: If CAC target is $5K/partner, marketing spend should support partner recruitment funnel

#### GTM Operations ↔ Growth Strategy
- [ ] Acquisition tactics match growth levers
  - **What to check**: If growth strategy assumes viral coefficient of 1.2 (partners refer partners), GTM should include partner referral program
- [ ] Sales cycle matches growth assumptions
  - **What to check**: If growth model assumes 30-day partner onboarding, GTM should define how to achieve this timeline

#### Growth Strategy ↔ Resource Planning
- [ ] Growth model matches hiring plan
  - **What to check**: If growth projects 120 partners by Month 18, hiring should include enough Partner Success Managers (1 PSM per 20-30 partners = 4-6 PSMs needed)
- [ ] Partner growth matches PSM capacity

#### Resource Planning ↔ Unit Economics
- [ ] Budget matches cost structure
  - **What to check**: If unit economics assumes 60% gross margin, cost structure should show corresponding OpEx
- [ ] Burn rate sustainable given revenue ramp
  - **What to check**: If revenue hits $1M ARR Month 12, burn should be <$500K/month by then (or runway runs out)

#### All Agents ↔ Kill Signals (THESIS.md)
- [ ] If any kill signal triggers, strategy fails
  - **What to check**: Ensure mitigation plans exist for each kill signal
- [ ] Kill Signal #1: No agents deployed after 4 weeks → Mitigated by Alpha co-development
- [ ] Kill Signal #2: >40% outputs rated unhelpful → Mitigated by default passive, output monitoring
- [ ] Kill Signal #3: Users prefer ChatGPT tab → Mitigated by progressive disclosure, in-context agents
- [ ] Kill Signal #4: Acceptance rate doesn't improve → THIS IS THE MOST CRITICAL METRIC (M3 → M6 → M9 trend)
- [ ] Kill Signal #5: Anthropic ships team workspace → Mitigated by 6-month GA timeline (vs 9-12 month estimate for Anthropic)

### Issues Identified

**To be completed after dependency documents exist.**

Potential issues to watch for:
- **ICP mismatch**: If customer intel says "tech startups" but GTM says "consulting firms" → Strategy incoherent
- **CAC explosion**: If partner acquisition costs >$10K but unit economics assumes $5K → Unprofitable
- **Hiring lag**: If growth projects 1,000 boards Month 9 but only 2 engineers hired → Capacity constraint
- **Burn rate unsustainable**: If burn is $300K/month but revenue only $50K Month 6 → Runway runs out Month 10

### Recommendations

**To be completed after cross-validation.**

Example recommendations:
- If partner CAC >$8K → Rethink partner selection criteria or pricing
- If hiring lags growth → Front-load engineering hires (Sprints 2-3, not Sprint 5)
- If burn unsustainable → Cut scope (web-only, defer board) or raise bridge round

---

## 5. Key Insights

### Risk Hierarchy

**Tier 1: Existential Risks** (if these fail, company dies)
1. Agent output quality (R5) → Default passive, human-in-loop, daily monitoring in Alpha/Beta
2. LLM cost spike (R2) → Hard usage caps, model routing, pricing buffer
3. Anthropic ships team Cowork before us (external) → 6-month GA timeline non-negotiable

**Tier 2: High-Impact Risks** (significant damage, but recoverable)
1. Data breach (R6) → Encryption, access controls, SOC 2 by Month 12
2. Partner deployment failure (external, in STRATEGY.md) → Hands-on support for first 5 clients/partner

**Tier 3: Operational Risks** (manageable with planning)
1. LLM API reliability (R1) → Multi-model fallback
2. Supabase scaling (R3) → Load testing Sprint 4, migration plan ready
3. Board SDK constraints (R4) → Spike Sprint 3, web-only fallback acceptable
4. Prompt injection (R7) → Input sanitization, SOUL hardening, monitoring

**Tier 4: Low Priority** (accept or defer)
1. Monolith migration (R8) → Defer until >50K boards
2. Context window overflow (R9) → Graceful degradation designed in

### Decision-Making Patterns

**Speed Matters**:
- Alpha Gate (Month 2): 1-week decision window (Week 8 review → Week 9 decision)
- Beta Gate (Month 5): 2-week decision window (allows partner interviews)
- Board SDK Gate (Sprint 3): 48-hour decision (technical feasibility, no debate)

**Clear Criteria**:
- All gates have measurable, binary criteria (>60% acceptance = pass, <60% = fail)
- No subjective gates ("team feels good about it") → Data-driven only

**Authority Matching Impact**:
- Technical decisions (Board SDK) → CTO decides, no CEO needed (faster)
- Strategic decisions (Scale vs Slow) → CEO recommends, Board approves (appropriate oversight)
- Financial decisions (spending >$50K) → Board involved (fiduciary duty)

### Risk Mitigation Themes

**Multi-Layer Defense**:
- LLM costs: Usage caps + model routing + pricing buffer (3 layers)
- Agent output: Default passive + human-in-loop + output validation + monitoring (4 layers)
- Data breach: Encryption + access controls + SOC 2 + pen testing (4 layers)

**Graceful Degradation**:
- API down → Fallback to secondary provider → Graceful degradation (read-only workspace)
- Context overflow → Priority stack → Truncate low-priority context (not error)
- Board SDK fails → Web-only launch (not blocked)

**Monitoring Over Prevention**:
- Cannot prevent prompt injection (no foolproof method) → Monitor and respond
- Cannot prevent context overflow (will happen) → Design for it
- Cannot prevent cost spikes (usage varies) → Cap and alert

---

## 6. Recommendations

### Immediate Actions (Pre-Sprint 2)

1. **Implement cost monitoring** (Week 1):
   - Token usage tracking per board
   - Alerts at 80% of $60 monthly cap
   - Dashboard for CTO/Finance review

2. **Define output monitoring protocol** (Week 1):
   - Daily review of all agent outputs (first 2 weeks)
   - Flag patterns: unhelpful rate >40%, PII detected, profanity
   - Weekly review meeting: Head of Product + Engineering Manager

3. **Schedule Board SDK spike** (Sprint 3, Week 8):
   - Assign 2 engineers, 1 week
   - Deliverable: Go/No-Go recommendation with evidence

4. **Draft security incident response plan** (Week 2):
   - CTO owns response
   - 24-hour breach notification SLA
   - Customer communication templates

### Sprint 4 (Weeks 9-12)

1. **Load testing**:
   - Simulate 50K concurrent users
   - Validate Supabase Realtime performance
   - Document migration path to self-hosted if needed

2. **Implement context overflow mitigation**:
   - Priority stack (Tiers 1-4)
   - Sliding window for conversations >50 messages
   - Token budgeting pre-calculation

### Month 6 (GA)

1. **Cost review**:
   - Compare actual vs estimated token costs
   - Adjust model routing if needed
   - Revisit $149 pricing if costs >$50/board

2. **Security hardening**:
   - GDPR compliance (data export, deletion)
   - Penetration test (external audit)

### Month 9 (Post-GA)

1. **Hire Security Lead** (if not already hired):
   - Own prompt injection monitoring
   - Quarterly red team exercises
   - SOC 2 audit preparation

2. **Gate 4 Review**:
   - Validate acceptance rate improved (M9 > M3)
   - If not → Existential crisis, feedback loop broken

### Month 12

1. **SOC 2 audit begins**:
   - Required for enterprise sales Year 2
   - 6-month process → start Month 12 for Month 18 certification

2. **Gate 5 Review**:
   - Decide: Scale (Series A) vs Operate Profitably vs Pivot

---

## Summary

**We have a complete risk framework.**

**What we know**:
- 9 technical risks identified, assessed, mitigated
- 5 decision gates defined with measurable criteria
- Decision authority clear (RACI matrix)
- Risk hierarchy: Agent output quality + LLM costs = existential tier

**What we're monitoring**:
- Agent acceptance rate trend (M3 → M6 → M9) = THE metric
- Token costs per board (target <$60/month)
- Partner deployment rate (>5 clients/partner by Month 6)

**Who decides what**:
- Technical: CTO/Eng Manager decide (Board SDK, architecture)
- GTM: CEO + Head of GTM decide (partners, pricing)
- Strategic: CEO recommends, Board approves (fundraising, pivot)

**What we'll do if things go wrong**:
- Gate 1 fail → Extend Alpha, fix output quality
- Gate 2 fail → Delay GA, fix partner GTM
- Gate 3 fail → Web-only launch (acceptable)
- Gate 4 fail → Diagnose (acceptance rate flat = existential)
- Gate 5 fail → Operate profitably or pivot

**Cross-validation pending**: Once other agent documents exist, validate consistency across customer intel, unit economics, GTM, growth, and resources.

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `THESIS.md` | Mother thesis, kill signals |
| `STRATEGY.md` | Market, competitive, GTM, build sequence |
| `DESIGN-SYNTHESIS.md` | Design decisions, MVP roadmap |
| `validation/CUSTOMER-FOUNDATION.md` | ICP, market sizing, segmentation (pending) |
| `validation/UNIT-ECONOMICS-MODEL.md` | CAC, LTV, margins, breakeven (pending) |
| `validation/GTM-EXECUTION-PLAN.md` | Partner program, sales playbook (pending) |
| `validation/GROWTH-STRATEGY.md` | Acquisition, retention, expansion (pending) |
| `validation/RESOURCES-AND-BUDGET.md` | Hiring, budget, burn rate (pending) |

---

## Sources

**Technical Risks**:
- [The Complete MLOps/LLMOps Roadmap for 2026](https://medium.com/@sanjeebmeister/the-complete-mlops-llmops-roadmap-for-2026-building-production-grade-ai-systems-bdcca5ed2771)
- [AI Challenges Enterprises Face in 2026](https://www.s3corp.com.vn/insights/artificial-intelligence-challenges)
- [LLM Security Risks in 2026](https://sombrainc.com/blog/llm-security-risks-2026)
- [What are LLM Security Risks and Mitigation Plan for 2026](https://www.uscsinstitute.org/cybersecurity-insights/blog/what-are-llm-security-risks-and-mitigation-plan-for-2026)

**API Reliability & Costs**:
- [Understanding LLM Cost Per Token: A 2026 Practical Guide](https://www.silicondata.com/blog/llm-cost-per-token)
- [LLM API Pricing 2026 - Compare 300+ AI Model Costs](https://pricepertoken.com/)
- [Anthropic API Pricing 2026: Complete Cost Breakdown](https://www.metacto.com/blogs/anthropic-api-pricing-a-full-breakdown-of-costs-and-integration)
- [Complete LLM Pricing Comparison 2026](https://www.cloudidr.com/blog/llm-pricing-comparison-2026)
- [Anthropic API Pricing: The 2026 Guide](https://www.nops.io/blog/anthropic-api-pricing/)

**Security**:
- [OWASP AI Agent Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html)
- [LLM01:2025 Prompt Injection - OWASP Gen AI Security Project](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [Prompt Injection Attacks in LLMs: A Comprehensive Review](https://www.mdpi.com/2078-2489/17/1/54)
- [Prompt Injection: The Most Common AI Exploit in 2025](https://www.obsidiansecurity.com/blog/prompt-injection)
- [2026 Operational Guide to Cybersecurity, AI Governance & Emerging Risks](https://www.corporatecomplianceinsights.com/2026-operational-guide-cybersecurity-ai-governance-emerging-risks/)

**Infrastructure**:
- [Supabase Realtime Benchmarks](https://supabase.com/docs/guides/realtime/benchmarks)
- [Supavisor: Scaling Postgres to 1 Million Connections](https://supabase.com/blog/supavisor-1-million)
- [Manage Realtime Peak Connections usage](https://supabase.com/docs/guides/platform/manage-your-usage/realtime-peak-connections)

**Context Window Management**:
- [The Context Window Problem: Scaling Agents Beyond Token Limits](https://factory.ai/news/context-window-problem)
- [Context Window Management: Strategies for Long-Context AI Agents](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- [Top techniques to Manage Context Lengths in LLMs](https://agenta.ai/blog/top-6-techniques-to-manage-context-length-in-llms)
- [Fix AI Agents that Miss Critical Details From Context Windows](https://datagrid.com/blog/optimize-ai-agent-context-windows-attention)

**Decision Frameworks**:
- [The Stage-Gate Model: An Overview](https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/)
- [What Is Stage-Gate (Phase-Gate) Project Management Process?](https://planisware.com/glossary/phase-gate-or-stage-gate)
- [Stage Gate Model: Definition, Examples, and Applications](https://www.launchnotes.com/glossary/stage-gate-model-in-product-management-and-operations)
- [Stage Gate Process: A Comprehensive Guide 2024](https://www.intellectsoft.net/blog/stage-gate-process/)
- [Go/No-Go Decision: 5 Strategic Areas to Consider](https://www.summitstrategywins.com/blog-posts/its-called-a-go-no-go-process-for-a-reason-five-areas-to-evaluate-before-pursuing-your-next-project)

**RACI Matrix**:
- [RACI Matrix: Responsibility Assignment Matrix Guide](https://project-management.com/understanding-responsibility-assignment-matrix-raci-matrix/)
- [Challenges Faced by Startups and the Relevance of RACI Model](https://leantime.io/startups-and-the-relevance-of-raci-model/)
- [RACI Matrix For Startups](https://www.meegle.com/en_us/topics/raci-matrix/raci-matrix-for-startups)
- [Using The RACI Matrix for Clarifying Decision Authority](https://www.onpointconsultingllc.com/blog/raci-matrix-decision-authority-in-a-team)
- [RACI Matrix Guide: Examples, Templates & Best Practices](https://boolkah.com/raci-matrix/)

---

*Last updated: 2026-02-10*
