# Skills Catalog — Available Skills for All Agents

This catalog lists every skill available in this environment.
When a task matches a skill, use it — skills have deep workflows, validation checklists, and reference docs baked in.

**To activate a skill:** mention its name or trigger phrase in a task, or brijesh-dev can invoke one by name.

---

## 🔴 Always-Active (No Trigger Needed)

| Skill | What It Does |
|---|---|
| **lessworks** | Smallest safe diff, no over-engineering, standard-library-first. ACTIVE BY DEFAULT on all coding tasks. Levels: lite / full / strict / intense / audit / off. |

---

## ⚙️ Engineering — Use When Writing or Reviewing Code

| Skill | Folder | Best For |
|---|---|---|
| **senior-architect** | `senior-architect/` | System design, ADRs, architecture decisions, tech trade-offs |
| **senior-backend** | `senior-backend/` | FastAPI, REST APIs, database design, backend patterns |
| **senior-devops** | `senior-devops/` | CI/CD pipelines, infrastructure as code, Terraform |
| **senior-qa** | `senior-qa/` | Test strategy, test suites, coverage analysis |
| **senior-data-engineer** | `senior-data-engineer/` | ETL pipelines, data models, DataOps, pipeline orchestration |
| **senior-data-scientist** | `senior-data-scientist/` | ML experiments, feature engineering, model evaluation |
| **senior-computer-vision** | `senior-computer-vision/` | CV models, inference optimization, dataset pipelines |
| **senior-prompt-engineer** | `senior-prompt-engineer/` | Prompt design, RAG, agentic system design, LLM evaluation |
| **python-engineer** | `python-engineer/` | Python best practices, idiomatic patterns |
| **backend-api-engineer** | `backend-api-engineer/` | API-focused backend work |
| **fullstack-feature-builder** | `fullstack-feature-builder/` | End-to-end feature: frontend + backend + tests |
| **automation-engineer** | `automation-engineer/` | Scripting, automation pipelines, idempotent operations |
| **sql-database-assistant** | `sql-database-assistant/` | Query optimization, schema design, ORM patterns, migrations |
| **playwright-pro** | `playwright-pro/` | E2E test generation, Playwright best practices, BrowserStack integration |
| **api-design-reviewer** | `api-design-reviewer/` | REST design review, breaking change detection, API linting |
| **api-test-suite-builder** | `api-test-suite-builder/` | Full API test suite from endpoint spec |
| **test-qa-engineer** | `test-qa-engineer/` | QA test generation, validation, regression coverage |
| **tech-stack-evaluator** | `tech-stack-evaluator/` | Compare tech stacks, TCO, migration analysis |
| **devops-observability-engineer** | `devops-observability-engineer/` | Monitoring, alerting, observability pipelines |
| **frontend-engineer** | `frontend-engineer/` | Frontend components, UI patterns, accessibility |

---

## 🔒 Security — Use When Touching Auth, Secrets, or Threat Surfaces

| Skill | Folder | Best For |
|---|---|---|
| **ai-security** | `ai-security/` | LLM threat models, OWASP LLM Top 10, prompt injection defense |
| **security-reviewer** | `security-reviewer/` | Code security review, vulnerability scanning |
| **threat-detection** | `threat-detection/` | Threat signal analysis, attack surface mapping |
| **prompt-governance** | `prompt-governance/` | Prompt safety, guardrails, governance for LLM outputs |

---

## 🤖 AI / Agent Skills — Use When Building or Improving AI Systems

| Skill | Folder | Best For |
|---|---|---|
| **senior-ml-engineer** ⚠️ | `senior-ml-engineer/` | MLOps, RAG systems, model deployment *(DISABLED.md present — verify before use)* |
| **self-improving-agent** | `self-improving-agent/` | Agent memory, skill extraction, self-improvement loops |
| **behuman** | `behuman/` | Making AI outputs sound authentically human |

---

## 🧪 Meta / Quality Skills — Use When Evaluating Skills or Agents

| Skill | Folder | Best For |
|---|---|---|
| **self-eval** | `self-eval/` | Agent self-assessment, output quality checks |
| **skill-tester** ⚠️ | `skill-tester/` | Test skill quality and validate skill outputs *(DISABLED.md present)* |
| **skill-security-auditor** ⚠️ | `skill-security-auditor/` | Audit skill files for security issues *(DISABLED.md present)* |

---

## 📦 Pre-Built Patterns (Always Loaded)

| File | What It Provides |
|---|---|
| `fastapi_crud.md` | Full FastAPI CRUD scaffold: models, schemas, crud, router, tests, conftest |
| `nvidia_api.md` | NVIDIA API async client, streaming, error handling, model table |

---

## Notes for Agents

- Skills marked **⚠️** have a `DISABLED.md` file — read that file before using them; they may require specific setup
- `playwright-pro` has integration support for BrowserStack and TestRail — check `playwright-pro/integrations/` when those are needed
- `senior-prompt-engineer` has agentic system design reference docs — use it when designing new agent workflows
- `self-improving-agent` has memory architecture patterns — use it when brijesh-dev needs to improve its own knowledge accumulation
- All skills follow LessWorks by default — never suggest a skill as a reason to write more code than needed
