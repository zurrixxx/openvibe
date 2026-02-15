# OpenVibe V2: Offering Clarification Questions

> Created: 2026-02-10
> Purpose: Critical questions to clarify before finalizing Customer Intelligence validation
> Context: Customer Intelligence Agent analyzed ICP based on incomplete understanding of offering
> Next: Discuss these questions, then re-run validation with correct offering definition

---

## Background

During Customer Intelligence validation review, we discovered a fundamental disconnect:

**Strategy Doc Says**:
- Target = "5K-15K organizations already operate with 'few humans + many agents'"
- Pain = "No workspace where agents are first-class participants"
- Competitors = Anthropic Cowork, OpenAI Frontier (agent workspaces)

**Customer Intelligence Agent Analyzed**:
- Target = "Professional services firms with context loss problem"
- Pain = "Too many meetings, duplicated work, status updates"
- Competitors = Slack, Teams, Notion (human collaboration tools)

**These are completely different ICPs.**

Before we can finalize strategy validation, we need to clarify the core offering definition.

---

## 8 Core Questions

### Q1: What Does "5K-15K Already Operate with Agents" Mean?

**Possible interpretations**:
- A. They use ChatGPT/Claude daily? (But that's 100M+ users, not 5K-15K orgs)
- B. They have "AI team member" concept? (e.g., "Our team has @ResearchBot")
- C. They built agent workflows with CrewAI/LangChain? (Developers only, very niche)
- D. They're trying Anthropic Cowork/OpenAI Frontier? (Bleeding edge)
- E. Something else?

**Why this matters**:
- Different interpretations → completely different ICP
- Determines whether target is "already doing" vs "should be doing"

**Your answer**: ___________

---

### Q2: Is the Market 5K-15K (Small) or 500K+ (Large)?

**Strategy says both**:
- Line 23: "5,000-15,000 organizations worldwide already operate with agents" (today)
- Line 33: "Growth: 50K+ orgs by Q3-Q4 2026, 100K+ by Q1-Q3 2027, mainstream (500K+) by 2028"

**Calculation**:
- If target = 5K-15K orgs × 100 boards = 500K boards × $149 = $890M ARR potential
- But 18-month target = $61M ARR = only 7% of this market

**Questions**:
- Are we targeting the entire 5K-15K? Or just a subset?
- Are we selling to "5K-15K today" or "500K+ eventually"?
- What's the expansion path from 5K to 500K?

**Your answer**: ___________

---

### Q3: Partner and Client - Who Is "5K-15K Already Using Agents"?

**Strategy says**:
- Target = "5K-15K already operate with agents"
- GTM = Partner-led (consulting firms deploy to **their clients**)

**Possible scenarios**:

**Scenario A: Partner = Early Adopter, Client = Early Adopter**
```
Partner: McKinsey (already uses agents)
Client: Fortune 500 (already uses agents)
Partner says: "We both use agents, but in isolation. Let's use OpenVibe."
```
- ICP = Single segment (5K-15K early adopters)
- Partner is just sales channel

**Scenario B: Partner = Early Adopter, Client = Laggard**
```
Partner: McKinsey (already uses agents)
Client: Traditional company (doesn't use agents yet)
Partner says: "Let me help you with AI transformation using OpenVibe."
```
- ICP = Two segments (partner = early adopter, client = laggard)
- Partner is "AI transformation consultant"

**Scenario C: Partner = Laggard, Client = Early Adopter**
```
Partner: Traditional consulting firm (doesn't use agents)
Client: Fortune 500 (already uses agents)
Client pulls Partner to adopt
```
- Client-driven adoption

**Your answer**: Which scenario? ___________

---

### Q4: If Client ≠ "5K-15K Early Adopters", How Does GTM Align with Target Market?

**The contradiction**:
- Strategy Line 35: "The bottleneck is NOT better models. It's **management infrastructure**"
  - This implies target **already uses agents**, just needs infrastructure
  - Not convincing laggards to start using agents

- But if Scenario B is true (partner sells to laggard clients):
  - We're selling to companies who **don't** use agents yet
  - That contradicts "target = 5K-15K already operating with agents"

**Resolution options**:
- Option 1: Target = 5K-15K (direct + partner themselves), clients are secondary market
- Option 2: Target = broader market via partner transformation, "5K-15K" is just early adopter proof
- Option 3: Two separate GTM motions (direct to early adopters + partner to laggards)

**Your answer**: ___________

---

### Q5: Are 40K Existing Boards an Asset or Constraint?

**Asset thinking**:
- 40K captive customers (already bought boards)
- Easy conversion: firmware upgrade → add AI features
- Are these 40K customers part of "5K-15K already using agents"?

**Constraint thinking**:
- Offering = "AI workspace for human+agent teams" (doesn't need board)
- But pricing = $149/month/**board** (implies board required?)
- What if someone wants OpenVibe without board?

**Strategy Line 69**:
> "The aha moment is NOT 'agent in the board meeting.' It's 'the board room got smarter between meetings.'"

This suggests board is **consumption surface** for value created in async work (web).

**Your answer**:
- Board role: A) Required, B) Optional, C) Nice-to-have? ___________
- 40K boards: Asset or constraint? ___________

---

### Q6: If Board Is Optional, Why Pricing = Per Board?

**The puzzle**:
- Product: "Web-first AI workspace" (Strategy Line 13, 65-74)
- Pricing: "$149/month/board" (Strategy Line 102-112)

**Questions**:
- If web-only users exist → What do they pay? $0? $149/workspace?
- If only board users pay → Not "web-first" anymore
- If board = "physical presence of agent" → Why not price per agent? Per workspace?

**Possible explanations**:
- A. Board is actually required (web is just "back office" for board)
- B. Pricing will change (per board is temporary, will be per user/workspace)
- C. Board owners subsidize web development (40K boards pay, web users free trial converts later)

**Your answer**: ___________

---

### Q7: One-Sentence Offering Description?

**If you had to describe OpenVibe in ONE sentence, which is most accurate?**

- A. "Workspace for teams already using agents" (Infrastructure play)
- B. "Bring AI into your team as colleague" (Transformation play)
- C. "Board + AI = smarter meeting rooms" (Hardware upgrade play)
- D. "The place where your agents live and remember" (Memory/context play)
- E. Something else: ___________

**Why this matters**:
Each description → completely different ICP:
- A → 5K-15K already using agents (narrow, early adopter)
- B → Broader market, partner-led transformation (wide, mass market)
- C → 40K board owners (captive, hardware base)
- D → Anyone frustrated with stateless ChatGPT (very wide)

**Your answer**: ___________

---

### Q8: "Few Humans + Many Agents" - Current State or Future Vision?

**Strategy Line 23**:
> "5,000-15,000 organizations worldwide **already operate** with 'few humans + many agents'"

This implies **current state** (they're already doing it).

**But realistically**:
- How many companies truly operate with "3 humans + 5 agents = team"?
- Most likely: They use ChatGPT daily (individual tool), but don't have "agent as team member" operating model

**Two interpretations**:

**Interpretation A: Already Doing**
- 5K-15K orgs literally have "human+agent teams" today
- They use CrewAI, build agents, have agent workflows
- Very niche market

**Interpretation B: Should Be Doing**
- They believe AI should be colleague (vision)
- But haven't achieved "agent workforce" yet (reality)
- Much larger addressable market

**Your answer**: A or B? ___________

---

## Impact on Customer Intelligence Validation

Once these questions are answered, we need to:

1. **Redefine ICP** based on correct offering understanding
2. **Rewrite use cases** (not "save time on meetings", but "operate with agent workforce")
3. **Recalculate market size** (not $13.8B collaboration, but "agent workforce adoption")
4. **Reframe decision chain** (not "partner recommends", but "we need agent infrastructure")
5. **Re-run validation** with correct assumptions

**Status**: BLOCKED until offering is clarified

---

## Recommended Next Steps

### Option A: Discuss These 8 Questions
- Go through each question
- Get your answers
- Build correct offering definition
- Resume Customer Intelligence Agent with correct brief

### Option B: You Define Offering First
- Write one-paragraph offering definition
- Then we validate it against Strategy docs
- Then resume validation with that definition

### Option C: Workshop the Offering
- Use these questions as framework
- Collaborative session to define offering
- Document agreed definition
- Proceed with validation

---

## Related Documents

- `THESIS.md` - Core thesis: "Where does human+agent collaboration happen?"
- `STRATEGY.md` - Market context: "5K-15K already operate with agents"
- `DESIGN-SYNTHESIS.md` - Product design based on thesis
- `CUSTOMER-FOUNDATION.md` - Current ICP (needs revision based on offering clarity)

---

*Save this document and discuss in next session before resuming strategy validation.*
