# OpenVibe V2: Unit Economics — Quick Reference

> One-page summary of unit economics model
> Full model: `UNIT-ECONOMICS-MODEL.md`

---

## The Bottom Line

**OpenVibe is a viable business.** Partner-led GTM delivers healthy economics (3.41x LTV/CAC). Direct channel doesn't work (1.82x). Blended is marginal (2.80x) but acceptable given 93% partner mix.

---

## Key Metrics

| Metric | Partner | Direct | Blended | Assessment |
|--------|---------|--------|---------|------------|
| **CAC** | $450 | $1,500 | $523 | Partner is 70% cheaper |
| **LTV** | $1,536 | $2,736 | $1,464 | 24-month lifetime, 4.2% churn |
| **LTV/CAC** | **3.41x** | 1.82x | 2.80x | Partner beats 3x target |
| **Gross Margin** | 64.6% | 76.5% | 63.5% | Wholesale discount compresses |
| **CAC Payback** | 7 mo | 13 mo | 9 mo | Fast for partner channel |

---

## CAC Breakdown

**Partner Channel** ($450/board):
- Partner recruitment: $25K per partner
- Enablement: $15K per partner
- Co-marketing: $5K/year
- Support: $8K/year
- **Total**: $53K → 100 boards = $450 CAC

**Direct Channel** ($1,500/board):
- Marketing: $300K/year
- Sales team: $420K/year
- Support: $180K/year
- **Total**: $900K → 600 boards = $1,500 CAC

**Why partner wins**: 1 partner = 100 boards. 1 direct customer = 1 board. Economics favor partner 3:1.

---

## LTV Model

**Revenue**:
- Retail: $149/month/board
- Partner wholesale: $99/month/board
- Blended: $96/month (93% partner mix)

**COGS** ($35/board/month):
- LLM (Claude Sonnet 4.5): $28
- Infrastructure (Supabase): $3
- CDN/Storage: $2
- Compute: $2

**Gross Profit**:
- Partner: $99 - $35 = $64/month (64.6% margin)
- Direct: $149 - $35 = $114/month (76.5% margin)

**Churn**: 4.2% monthly (24-month lifetime)
- Lower than 7.1% software-only benchmark
- Hardware bundling = lock-in

**LTV Calculation**:
- Partner: $64 × 24 months = $1,536
- Direct: $114 × 24 months = $2,736

---

## Break-even

**Target**: 4,506 boards
- Contribution margin: $67.50/board/month
- Fixed costs: $304K/month
- Revenue at break-even: $433K/month ($5.2M ARR)

**Timeline**: Month 14-15 (11-12 months post-GA)
- Cumulative burn: $4.25M
- Includes 90-day free trial burn ($1.33M)

---

## 90-Day Free Trial Impact

**Assumptions**:
- 40K boards eligible at GA
- 10% activate trial = 4,000 boards
- 25% convert = 1,000 paying boards

**Cash Flow**:
- Month 6-8: -$444K/month (COGS + OpEx, zero revenue)
- Month 9: -$243K/month (first conversions)
- **Trial burn**: $1.33M over 3 months

**Kill signal**: <20% conversion → Trial model broken

---

## Cost Structure (Month 18)

**Revenue**: $3.7M/month ($44.4M ARR)
- 34,500 boards × $96 blended = $3.31M
- Partner: 93% ($3.08M)
- Direct: 7% ($0.23M)

**COGS**: $1.26M/month (34%)
- 34,500 boards × $35 = $1.21M

**Gross Profit**: $2.44M/month (66%)

**OpEx**: $304K/month
- R&D: $123K (Engineering + Product)
- S&M: $131K (Sales + Marketing + Partner)
- G&A: $50K

**Operating Income**: $2.1M/month (57% margin)

---

## Critical Assumptions to Validate

**Pre-Launch** (Alpha):
1. LLM cost <$1.00 per @mention
2. Partner wholesale at $99 acceptable
3. Churn <5% monthly

**Post-Launch** (First 90 days):
4. Trial activation: 10%
5. Trial conversion: 25%
6. Partner boards: 20+ per partner in 6 months

**Kill Signals**:
- LLM cost >$40/month → Pricing broken
- Churn >7% monthly → PMF issue
- Trial conversion <15% → Model broken
- Partner boards <20 → Wrong partners

---

## Strategic Decisions

**1. Partner wholesale: $99/month** (not $89)
- Partners earn $50 margin at $149 retail
- OpenVibe gets $99 revenue
- Trade-off: Lower margin for distribution leverage

**2. LLM cost target: $28/month** (not $35)
- Prompt caching (90% savings on cache hits)
- Use Haiku for simple queries
- Batch API for background (50% discount)

**3. Churn target: 4.2% monthly** (not 5%)
- Hardware bundling effect
- 24-month lifetime defensible
- Monitor cohorts by Month 3

**4. De-prioritize direct channel**
- 1.82x LTV/CAC is not viable
- Keep for learning only
- 90% resources to partner recruitment

---

## Pricing Scenarios

| Price | Impact | Boards (M18) | Revenue | Profit | Assessment |
|-------|--------|--------------|---------|--------|------------|
| $129 | +15% adoption | 39,715 | $5.12M | $3.73M | Compromise |
| **$149** | **Baseline** | **34,500** | **$5.14M** | **$3.77M** | **Base case** |
| $179 | -20% adoption | 27,600 | $4.94M | $3.97M | Premium risk |

**Recommendation**: Hold at $149
- Below $2K/year expense threshold
- Anchors vs Copilot ($30/user × 5 = $150)
- ROI: "Less than 1 hour saved per week"

---

## What Works

1. Partner channel economics (3.41x) beat target
2. Gross margins (76.5% direct) exceed AI SaaS benchmarks (50-65%)
3. Operating leverage strong (57% margin at Month 18)
4. Hardware bundling reduces churn 30%

## What's Risky

1. Direct channel doesn't work (1.82x)
2. LLM costs are volatile (19-23% of revenue)
3. Trial conversion is critical (<20% = broken)
4. Partner wholesale discount limits upside

## Immediate Actions

1. Lock partner price at $99 (test with first 5 partners)
2. Instrument LLM cost tracking (alert if >$1.50/@mention)
3. Optimize trial conversion (credit card, 60-day, nudges)
4. De-prioritize direct (learning only, not revenue)

---

**Full model**: `UNIT-ECONOMICS-MODEL.md` (37 pages, detailed calculations)
**Sources**: 12 industry benchmarks (OpenView, ProfitWell, Anthropic, Supabase)
