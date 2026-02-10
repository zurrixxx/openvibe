# OpenVibe

> The first workspace designed for human+agent collaboration.

## V2 Design

**Read first:** `docs/v2/THESIS.md` (mother thesis)
**Then:** `docs/v2/DESIGN-SYNTHESIS.md` (thesis -> design decisions)

**Mother thesis:** AI is transitioning from tool to colleague. Human+Agent collaboration needs a new medium. OpenVibe is that medium.

**Three layers:**
1. Protocol (for agents): identity, trust, memory, tool access
2. Interface (for humans): familiar UX, progressive disclosure, feedback
3. Space (shared): persistent context, knowledge accumulation, compound value

## Key Docs

| Document | Content |
|----------|---------|
| `docs/v2/THESIS.md` | Mother thesis — start here |
| `docs/v2/DESIGN-SYNTHESIS.md` | Design decisions + MVP roadmap |
| `docs/v2/design/AGENT-IN-CONVERSATION.md` | How agents participate in conversations |
| `docs/v2/design/PERSISTENT-CONTEXT.md` | Memory & knowledge accumulation |
| `docs/v2/design/FEEDBACK-LOOP.md` | Human judgment -> agent behavior |
| `docs/v2/reference/V1-INSIGHT-AUDIT.md` | What survived from V1 |
| `docs/v2/reference/AGENT-ORCHESTRATION-REFERENCE.md` | External references (Voxyz, KSimback, Yangyi) |
| `docs/v1/INTENT.md` | Current goals (V1) |
| `docs/v1/CLAUDE-CODE-INSTRUCTIONS.md` | Workflow guide (V1) |

## V1 (Archived)

V1 docs at `docs/v1/`. Thesis: "AI Deep Dive amplifies human cognition in team conversations."
Archived because: too derivative (Slack replacement), too narrow (deep dive is a feature, not a product).
V1 research/validation data is still valuable — see `docs/v2/reference/V1-INSIGHT-AUDIT.md`.

## Session Resume Protocol

1. Read `docs/v2/THESIS.md` — understand the "why"
2. Read `docs/v2/DESIGN-SYNTHESIS.md` — understand the "what"
3. Read `PROGRESS.md` — understand current sprint state
4. Each Sprint completed -> pause for user confirmation

## Constraints

- Only submit complete implementations (no partial work)
- Do not leave TODOs
- New features must have tests
- Two teammates should not edit the same file simultaneously

## Design Principles

1. **Agent in the conversation** — AI is a participant, not a sidebar tool
2. **Progressive Disclosure** — Headline / summary / full for all agent output
3. **Workspace gets smarter** — Context, memory, knowledge compound over time
4. **Feedback is the moat** — Agent shaped by team feedback > smarter model without context
5. **Configuration over Code** — SOUL + config-driven agents, not hardcoded behavior
