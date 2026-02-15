# GitHub Organization Setup

> Date: 2026-02-10
> Status: Ready to implement

---

## Organization Details

**GitHub Org Name**: `openvibeorg`
**Display Name**: OpenVibe
**Website**: https://open-vibe.org
**Description**: Open infrastructure for human+agent collaboration

---

## Repository Structure

```
openvibeorg/
├── .github                     # Org-level configs, community health files
│   ├── profile/
│   │   └── README.md          # Org profile shown on github.com/openvibeorg
│   ├── CONTRIBUTING.md
│   ├── CODE_OF_CONDUCT.md
│   └── SECURITY.md
│
├── openvibe                    # Core platform repo
├── openvibe-docs               # Documentation site (open-vibe.org)
├── openvibe-agents             # Agent library & templates
├── openvibe-plugins            # Plugin ecosystem
├── vibeorg-site                # Movement site (vibeorg.com) source
└── community                   # Community discussions, RFCs
```

---

## Initial Repositories

### 1. openvibe (Core Platform)

**Description**: The workspace for human+agent collaboration
**Visibility**: Public
**License**: MIT or Apache 2.0

**Initial Structure**:
```
openvibe/
├── README.md                   # Main project README
├── CONTRIBUTING.md
├── LICENSE
├── ROADMAP.md
├── docs/                       # High-level docs (detailed docs in openvibe-docs)
├── packages/
│   ├── core/                   # Core platform code
│   ├── web/                    # Web client
│   ├── mobile/                 # Mobile apps
│   └── board/                  # Vibe board integration
├── examples/                   # Example implementations
└── scripts/                    # Development scripts
```

**Topics**: `ai`, `agents`, `collaboration`, `workspace`, `open-source`

---

### 2. openvibe-docs (Documentation Site)

**Description**: Documentation for OpenVibe
**Visibility**: Public
**License**: MIT
**Hosted**: https://open-vibe.org (GitHub Pages or Vercel)

**Initial Structure**:
```
openvibe-docs/
├── README.md
├── docs/
│   ├── getting-started/
│   ├── architecture/
│   ├── deployment/
│   ├── agents/
│   ├── api/
│   └── contributing/
├── static/
└── docusaurus.config.js        # Or similar docs framework
```

**Topics**: `documentation`, `docs`, `openvibe`

---

### 3. openvibe-agents (Agent Library)

**Description**: Agent templates and examples for OpenVibe
**Visibility**: Public
**License**: MIT

**Initial Structure**:
```
openvibe-agents/
├── README.md
├── templates/
│   ├── analyst/                # Data analyst agent
│   ├── writer/                 # Content writer agent
│   ├── coder/                  # Code assistant agent
│   └── researcher/             # Research agent
├── examples/
└── docs/
```

**Topics**: `ai-agents`, `templates`, `openvibe`

---

### 4. openvibe-plugins (Plugin Ecosystem)

**Description**: Plugin system for extending OpenVibe
**Visibility**: Public
**License**: MIT

**Initial Structure**:
```
openvibe-plugins/
├── README.md
├── core/                       # Plugin SDK
├── official/                   # Official plugins
│   ├── github/
│   ├── slack/
│   ├── notion/
│   └── ...
├── community/                  # Community plugins
└── docs/
```

**Topics**: `plugins`, `integrations`, `openvibe`

---

### 5. .github (Org-level configs)

**Description**: Organization-level community health files
**Visibility**: Public

**Structure**:
```
.github/
├── profile/
│   └── README.md              # Org profile
├── CONTRIBUTING.md            # How to contribute
├── CODE_OF_CONDUCT.md        # Community standards
├── SECURITY.md                # Security policy
└── SUPPORT.md                 # How to get help
```

---

### 6. community (Discussions)

**Description**: Community discussions, RFCs, and governance
**Visibility**: Public
**Features**: Enable GitHub Discussions

**Structure**:
```
community/
├── README.md
├── discussions/               # (via GitHub Discussions feature)
├── rfcs/                      # Request for Comments
│   ├── template.md
│   └── 0001-example.md
└── governance/
    └── GOVERNANCE.md
```

---

## Organization Profile README

Location: `openvibeorg/.github/profile/README.md`

See `BRAND-ARCHITECTURE.md` for full content. Key sections:
- What is OpenVibe?
- Get Started links
- Key Repositories
- Community links

---

## Main Repository README

Location: `openvibeorg/openvibe/README.md`

Key sections:
1. **Hero**: Project name, tagline, badges
2. **What is OpenVibe**: Quick overview
3. **Architecture**: High-level diagram
4. **Key Features**: Bullet points
5. **Quick Start**: Cloud vs Self-hosted
6. **Documentation**: Links
7. **Community**: How to engage
8. **Contributing**: How to contribute
9. **Roadmap**: Current status
10. **License**: License info
11. **Commercial**: Link to vibe.us

See `BRAND-ARCHITECTURE.md` for full draft.

---

## Community Health Files

### CONTRIBUTING.md

Key sections:
- Code of Conduct
- How to contribute (code, docs, issues, discussions)
- Development setup
- PR process
- Style guide
- Testing requirements

### CODE_OF_CONDUCT.md

Use standard Contributor Covenant or similar.

### SECURITY.md

- How to report security vulnerabilities
- Security disclosure policy
- Supported versions

### SUPPORT.md

- Where to get help (Discussions, Discord, Stack Overflow)
- How to file issues
- Paid support options (via partners)

---

## Issue & PR Templates

### Issue Templates

`.github/ISSUE_TEMPLATE/`:
- `bug_report.md` - Bug report template
- `feature_request.md` - Feature request template
- `documentation.md` - Documentation improvement
- `question.md` - Questions (redirect to Discussions)

### PR Template

`.github/PULL_REQUEST_TEMPLATE.md`:
- What changed
- Why (issue reference)
- Testing done
- Screenshots (if UI change)
- Checklist (tests, docs, etc.)

---

## GitHub Features to Enable

### On Organization
- [x] Discussions (on `community` repo)
- [x] Projects (for roadmap tracking)
- [x] Sponsors (if accepting sponsorships)

### On Main Repo (`openvibe`)
- [x] Issues
- [x] Discussions (or centralize in `community`)
- [x] Projects (link to org project)
- [x] Wiki (or use docs repo)
- [x] Actions (CI/CD)
- [x] Security (Dependabot, code scanning)

---

## Topics & Discoverability

### Org-level Topics
Add to openvibeorg repos:
- `openvibe`
- `ai-workspace`
- `human-agent-collaboration`
- `open-source`
- `multi-model-ai`

### SEO Keywords
- "open source ai workspace"
- "human agent collaboration"
- "multi-model ai platform"
- "self-hosted ai workspace"
- "agent collaboration platform"

---

## Branch Protection Rules

For `openvibe` main branch:
- [x] Require PR reviews (1+ reviewer)
- [x] Require status checks to pass
- [x] Require branches to be up to date
- [x] Include administrators (strict)
- [ ] Restrict pushes (optional, based on team size)

---

## CI/CD Setup

### GitHub Actions Workflows

`.github/workflows/`:
- `ci.yml` - Run tests on every PR
- `deploy-docs.yml` - Deploy docs to open-vibe.org
- `publish.yml` - Publish releases
- `security.yml` - Security scanning

---

## Migration from vibeaios

If migrating existing repos from `vibeaios`:

### Transfer vs Fork

**Transfer** (recommended):
- Preserves all history, issues, stars
- Changes org ownership
- Breaks existing forks (they become forks of new location)

**Fork** (alternative):
- Keep original in vibeaios (private)
- Public fork in openvibeorg
- Can sync changes

### Migration Checklist

- [ ] Transfer `vibeaios/openvibe` → `openvibeorg/openvibe`
- [ ] Update all README links
- [ ] Update CI/CD configs
- [ ] Update contributor list
- [ ] Notify existing contributors
- [ ] Update external links (docs, website)

---

## Launch Checklist

### Pre-Launch
- [ ] Create GitHub org `openvibeorg`
- [ ] Set up org profile and README
- [ ] Create initial repos
- [ ] Add community health files
- [ ] Configure branch protections
- [ ] Set up CI/CD
- [ ] Write initial documentation

### Launch
- [ ] Transfer/create `openvibe` repo
- [ ] Publish org profile
- [ ] Announce on socials/blog
- [ ] Submit to directories (Awesome lists, etc.)

### Post-Launch
- [ ] Monitor community engagement
- [ ] Respond to issues/PRs
- [ ] Regular updates and releases
- [ ] Build contributor community

---

## Related Documents

- `BRAND-ARCHITECTURE.md` - Brand strategy and messaging
- `../THESIS.md` - Core vision
- `../STRATEGY.md` - Overall strategy
