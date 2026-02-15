# Unit Economics Spreadsheet Model — Specification

> Instructions for building the OpenVibe unit economics spreadsheet
> Companion to `UNIT-ECONOMICS-MODEL.md`

---

## Overview

This spreadsheet provides an interactive model for OpenVibe's unit economics with editable assumptions and automatic calculations.

**Recommended tool**: Google Sheets (for collaboration) or Excel

---

## Sheet Structure

### Sheet 1: Dashboard

**Purpose**: One-page overview of key metrics

**Layout**:

```
A | B | C | D | E
---|---|---|---|---
OPENVIBE UNIT ECONOMICS | | | |
 | | | |
Metric | Partner | Direct | Blended | Target
CAC | =$450 | =$1,500 | =$523 | <$1,000
LTV | =$1,536 | =$2,736 | =$1,464 | >$1,500
LTV/CAC | =3.41x | =1.82x | =2.80x | >3.0x
Gross Margin | =64.6% | =76.5% | =63.5% | >70%
CAC Payback | =7 mo | =13 mo | =9 mo | <12 mo
Break-even Boards | | | =4,506 | <5,000
Break-even Month | | | =14-15 | <18
 | | | |
Status | =IF(C5>=E5,"✅","⚠️") | | |
```

**Conditional Formatting**:
- Green if metric meets target
- Yellow if within 10% of target
- Red if below target

---

### Sheet 2: Assumptions (Inputs)

**Purpose**: All editable inputs in one place

**Sections**:

#### A. Pricing

| Parameter | Value | Notes |
|-----------|-------|-------|
| Retail Price (/month/board) | $149 | List price |
| Partner Wholesale (/month/board) | $99 | Partner buys at this |
| Partner Retail Markup | $50 | Partner margin if sell at $149 |

#### B. Costs

| Parameter | Value | Notes |
|-----------|-------|-------|
| LLM Cost (/month/board) | $28 | Claude Sonnet 4.5, with caching |
| Infrastructure (/month/board) | $7.50 | Supabase, CDN, compute |
| **Total COGS** | **=SUM(above)** | **$35.50** |

#### C. Churn & Retention

| Parameter | Value | Notes |
|-----------|-------|-------|
| Monthly Churn Rate | 4.2% | Hardware bundling effect |
| **Customer Lifetime (months)** | **=1/B9** | **24 months** |
| Annual Retention | =(1-B9)^12 | 61% |

#### D. CAC - Partner Channel

| Parameter | Value | Notes |
|-----------|-------|-------|
| Partner Recruitment Cost | $25,000 | Sales cycle + onboarding |
| Partner Enablement Cost | $15,000 | Training, materials |
| Co-marketing (/year) | $5,000 | Joint campaigns |
| Partner Support (/year) | $8,000 | Ongoing support |
| **Total Partner Investment (Year 1)** | **=SUM(above)** | **$53,000** |
| Boards per Partner | 100 | Year 1 average |
| **Partner CAC** | **=B18/B19** | **$450** |

#### E. CAC - Direct Channel

| Parameter | Value | Notes |
|-----------|-------|-------|
| Marketing Spend (/year) | $300,000 | Digital, content, events |
| Sales Team Cost (/year) | $420,000 | 2 AE, 1 SDR fully loaded |
| Trial Support (/year) | $180,000 | CS team |
| **Total Direct Cost** | **=SUM(above)** | **$900,000** |
| Boards Acquired (/year) | 600 | Direct channel |
| **Direct CAC** | **=B26/B27** | **$1,500** |

#### F. Channel Mix

| Parameter | Value | Notes |
|-----------|-------|-------|
| Partner % of Boards | 93% | From STRATEGY.md |
| Direct % of Boards | 7% | Minority channel |
| **Blended CAC** | **=(B20*B32)+(B28*B33)** | **$523** |

#### G. Free Trial

| Parameter | Value | Notes |
|-----------|-------|-------|
| Total Boards at GA | 40,000 | Existing installed base |
| Trial Activation Rate | 10% | % that activate trial |
| Active Trial Boards | =B38*B39 | 4,000 |
| Trial Conversion Rate | 25% | % that convert to paid |
| Converted Boards | =B40*B41 | 1,000 |
| Trial Duration (days) | 90 | Free period |

#### H. Fixed Costs (Monthly)

| Department | Headcount | Avg Salary | Monthly Cost |
|------------|-----------|------------|--------------|
| Engineering | 8 | $150,000 | =B47*C47/12 | $100,000 |
| Product/Design | 2 | $140,000 | =B48*C48/12 | $23,333 |
| Sales | 3 | $140,000 | =B49*C49/12 | $35,000 |
| Partner Team | 2 | $130,000 | =B50*C50/12 | $21,667 |
| Marketing | 2 | $120,000 | =B51*C51/12 | $20,000 |
| Customer Success | 2 | $110,000 | =B52*C52/12 | $18,333 |
| G&A | 2 | $125,000 | =B53*C53/12 | $20,833 |
| **Total Headcount** | **=SUM(B47:B53)** | | **=SUM(D47:D53)** | **21** | | **$239,166** |
| | | | |
| Non-Personnel | | | $65,000 |
| **Total Fixed Costs** | | | **=D54+D56** | **$304,166** |

---

### Sheet 3: LTV Calculation

**Purpose**: Calculate lifetime value by channel

**Layout**:

| Metric | Partner | Direct | Blended | Formula |
|--------|---------|--------|---------|---------|
| **Revenue** | | | | |
| Monthly Revenue | $99 | $149 | =(B3*Assumptions!B32)+(C3*Assumptions!B33) | From Assumptions |
| Annual Revenue | =B3*12 | =C3*12 | =D3*12 | |
| | | | | |
| **Costs** | | | | |
| Monthly COGS | $35 | $35 | $35 | From Assumptions!B10 |
| Annual COGS | =B7*12 | =C7*12 | =D7*12 | |
| | | | | |
| **Gross Profit** | | | | |
| Monthly Gross Profit | =B3-B7 | =C3-C7 | =D3-D7 | Revenue - COGS |
| Gross Margin % | =B11/B3 | =C11/C3 | =D11/D3 | Profit / Revenue |
| | | | | |
| **Lifetime Value** | | | | |
| Customer Lifetime (months) | =Assumptions!B10 | =Assumptions!B10 | =Assumptions!B10 | From churn |
| **LTV** | =B11*B15 | =C11*C15 | =D11*D15 | Monthly Profit × Lifetime |
| | | | | |
| **Unit Economics** | | | | |
| CAC | =Assumptions!B20 | =Assumptions!B28 | =Assumptions!B35 | From Assumptions |
| **LTV/CAC Ratio** | =B17/B20 | =C17/C20 | =D17/D20 | Key metric |
| CAC Payback (months) | =B20/B11 | =C20/C11 | =D20/D11 | Months to recover CAC |

**Conditional Formatting**:
- LTV/CAC row: Green if ≥3.0, Yellow if 2.5-3.0, Red if <2.5
- Gross Margin row: Green if ≥70%, Yellow if 60-70%, Red if <60%

---

### Sheet 4: Break-even Analysis

**Purpose**: Calculate break-even point and timeline

**Section A: Break-even Point**

| Metric | Value | Formula |
|--------|-------|---------|
| **Contribution Margin** | | |
| Blended Revenue (/month/board) | ='LTV Calculation'!D3 | From LTV sheet |
| Blended COGS (/month/board) | ='LTV Calculation'!D7 | From LTV sheet |
| **Contribution Margin** | =B4-B5 | $64.50 |
| | | |
| **Fixed Costs** | | |
| Monthly Fixed Costs | =Assumptions!D57 | $304,166 |
| | | |
| **Break-even** | | |
| Break-even Boards | =B9/B6 | 4,716 boards |
| Break-even Monthly Revenue | =B11*B4 | $433K |
| Break-even ARR | =B12*12 | $5.2M |

**Section B: Timeline to Break-even**

| Month | New Boards | Total Boards | Revenue | COGS | Gross Profit | Fixed Costs | Net Income | Cumulative |
|-------|------------|--------------|---------|------|--------------|-------------|------------|------------|
| 1-6 | 0 | 0 | $0 | $0 | $0 | $304K | -$304K | -$1.82M |
| 6 (Trial) | 4,000 | 4,000 | $0 | $140K | -$140K | $304K | -$444K | -$2.27M |
| 7 | 0 | 4,000 | $0 | $140K | -$140K | $304K | -$444K | -$2.71M |
| 8 | 0 | 4,000 | $0 | $140K | -$140K | $304K | -$444K | -$3.16M |
| 9 | 0 | 1,000 | $96K | $35K | $61K | $304K | -$243K | -$3.40M |
| 10 | 250 | 1,250 | $120K | $44K | $76K | $304K | -$228K | -$3.63M |
| 11 | 500 | 1,750 | $168K | $61K | $107K | $304K | -$197K | -$3.83M |
| 12 | 750 | 2,500 | $240K | $88K | $152K | $304K | -$152K | -$3.98M |
| 13 | 1,000 | 3,500 | $336K | $122K | $214K | $304K | -$90K | -$4.07M |
| 14 | 1,250 | 4,750 | $456K | $166K | $290K | $304K | **-$14K** | -$4.09M |
| 15 | 1,500 | 6,250 | $600K | $219K | $381K | $304K | **+$77K** | **-$4.01M** |

**Chart**: Line graph showing cumulative cash position over time, highlighting break-even point

---

### Sheet 5: Sensitivity Analysis

**Purpose**: Show how key metrics change with different assumptions

**Section A: LTV/CAC Sensitivity**

| | **Churn Rate** | | | | |
|---|---|---|---|---|---|
| **Partner Wholesale** | 3.5% | 4.0% | 4.2% | 4.5% | 5.0% |
| $89 | 2.89x | 2.51x | 2.41x | 2.28x | 2.08x |
| $94 | 3.26x | 2.83x | 2.72x | 2.57x | 2.35x |
| **$99** | **3.63x** | **3.15x** | **3.03x** | **2.86x** | **2.61x** |
| $104 | 4.01x | 3.48x | 3.34x | 3.16x | 2.88x |
| $109 | 4.38x | 3.80x | 3.65x | 3.45x | 3.14x |

Color scale: Red <2.5, Yellow 2.5-3.0, Green >3.0

**Section B: LLM Cost Impact**

| LLM Cost/Month | COGS | Gross Margin | LTV (Partner) | LTV/CAC |
|----------------|------|--------------|---------------|---------|
| $20 | $27.50 | 72.2% | $1,714 | 3.81x |
| $25 | $32.50 | 67.2% | $1,596 | 3.55x |
| **$28** | **$35.50** | **64.1%** | **$1,524** | **3.39x** |
| $30 | $37.50 | 62.1% | $1,476 | 3.28x |
| $35 | $42.50 | 57.1% | $1,356 | 3.01x |
| $40 | $47.50 | 52.0% | $1,236 | 2.75x |

**Section C: Trial Conversion Impact**

| Conversion Rate | Paying Boards (Month 9) | Monthly Revenue | Net Income | Assessment |
|-----------------|-------------------------|-----------------|------------|------------|
| 15% | 600 | $58K | -$281K | ⚠️ Slow |
| 20% | 800 | $77K | -$262K | ⚠️ Marginal |
| **25%** | **1,000** | **$96K** | **-$243K** | ✅ Base |
| 30% | 1,200 | $115K | -$224K | ✅ Good |
| 35% | 1,400 | $134K | -$205K | ✅ Strong |

**Section D: Price Elasticity**

| Price | Adoption Impact | Boards (M18) | Revenue/Month | Gross Profit | LTV/CAC |
|-------|-----------------|--------------|---------------|--------------|---------|
| $99 | +30% | 44,850 | $4.44M | $2.87M | 2.12x |
| $129 | +15% | 39,715 | $5.12M | $3.73M | 2.65x |
| **$149** | **Baseline** | **34,500** | **$5.14M** | **$3.77M** | **2.80x** |
| $179 | -20% | 27,600 | $4.94M | $3.97M | 3.01x |
| $199 | -30% | 24,150 | $4.81M | $3.96M | 3.12x |

---

### Sheet 6: Monthly Projections

**Purpose**: Full 24-month revenue and cash flow model

**Columns**:
- Month
- Partner Boards Added
- Direct Boards Added
- Total Boards (cumulative)
- Partner Revenue
- Direct Revenue
- Total Revenue
- COGS
- Gross Profit
- Fixed Costs
- Net Income
- Cumulative Cash

**Assumptions**:
- Month 1-6: Build phase, no revenue
- Month 6-9: Free trial (COGS but no revenue)
- Month 9+: Conversions + new sales ramp

**Chart**:
1. Stacked area chart: Revenue, COGS, Fixed Costs
2. Line chart: Cumulative cash burn/profit

---

### Sheet 7: Cohort Analysis

**Purpose**: Track retention by customer cohort

**Layout**:

| Cohort | M0 | M1 | M2 | M3 | M6 | M12 | M18 | M24 |
|--------|----|----|----|----|----|----|-----|-----|
| Month 9 | 100% | 95.8% | 91.8% | 87.9% | 76.8% | 59.0% | 45.3% | 34.8% |
| Month 10 | 100% | 95.8% | 91.8% | 87.9% | 76.8% | 59.0% | 45.3% | |
| Month 11 | 100% | 95.8% | 91.8% | 87.9% | 76.8% | 59.0% | | |

Formula: Retention = (1 - 0.042)^months

**Chart**: Line chart showing retention curves by cohort

---

## How to Use This Spreadsheet

### Step 1: Set Up Assumptions
1. Go to "Assumptions" sheet
2. Review all inputs (pricing, costs, churn, CAC)
3. Edit yellow highlighted cells only
4. All other cells auto-calculate

### Step 2: Review Dashboard
1. Check Dashboard sheet
2. Verify key metrics meet targets
3. Conditional formatting shows status

### Step 3: Run Sensitivity Analysis
1. Go to "Sensitivity Analysis" sheet
2. Adjust scenarios (pricing, churn, costs)
3. See impact on LTV/CAC

### Step 4: Model Timeline
1. Review "Monthly Projections"
2. Identify break-even point
3. Calculate cumulative burn

### Step 5: Export for Presentation
1. Copy Dashboard to slides
2. Export key charts
3. Share summary metrics

---

## Validation Checklist

After building the spreadsheet, verify:

- [ ] All formulas reference "Assumptions" sheet (no hardcoded values)
- [ ] Dashboard auto-updates when assumptions change
- [ ] LTV/CAC calculation matches document ($3.41x partner, $2.80x blended)
- [ ] Break-even calculation matches (~4,500 boards, Month 14-15)
- [ ] Sensitivity tables show reasonable ranges
- [ ] Monthly projections sum correctly (revenue = boards × price)
- [ ] Cohort retention curves decay at 4.2% monthly
- [ ] Charts are clear and properly labeled

---

## Notes

This specification can be implemented in:
- **Google Sheets**: Best for collaboration, sharing with investors
- **Excel**: More powerful for large datasets, complex models
- **Airtable**: If you want database-style filtering

Estimated build time: 2-3 hours for someone comfortable with spreadsheets.

**Next Step**: Build this spreadsheet and share link in validation folder.
