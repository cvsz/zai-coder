# ROADMAPS.md

## Overview
This roadmap outlines the remaining work to transition the **zai-coder** repository to a **Master Advanced Professional Enterprise‑grade Production‑Ready** state. It consolidates identified bugs, missing features, and planned upgrades across all subsystems, and defines the release cadence through **v0.5.0**.

---

### 📌 Current Status
| Release | Phase | Description | Status |
|---|---|---|---|
| **v0.3.0** | 1‑3 | SSO Identity, Compliance, Reporting & Governance | ✅ Completed |
| **v0.4.0** | 1 | Observability Suite – live metrics (psutil) | ✅ Completed |
| **v0.4.0** | 2‑4 | **Pending** – Operations Control Center, Production API Gateway, Final Release | ⏳ In progress |

---

## 1️⃣ Bugs / Defects (Open)
| Subsystem | File | Issue | Priority |
|---|---|---|---|
| **Observability Suite** | `health_trends.py` | Default health trend store falls back silently on any exception – may hide real telemetry failures. | Medium |
| **Operations Control Center** | `service_status.py` | `default_service_statuses` does not handle missing system services gracefully (subprocess may raise). | Low |
| **Production API Gateway** | *none yet* | No live‑routing implementation – currently a mock stub. | High |
| **General** | Multiple files | Missing type‑checking for `execute` flag pathways (e.g., returning wrong datatypes). | Low |

---

## 2️⃣ Features / Enhancements (Planned)
| Subsystem | Feature | Description | Target Release |
|---|---|---|---|
| **Observability Suite** | Alert Saturation Control | Add rate‑limiting & deduplication for high‑frequency alerts. | v0.5.0 |
| **Operations Control Center** | Live Service Dashboard | UI page that polls `default_service_statuses(execute=True)` and visualises health with color‑coded tiles. | v0.5.0 |
| **Production API Gateway** | Dynamic Routing Engine | Replace static config with a router that inspects live service registry and forwards traffic accordingly. | v0.5.0 |
| **Compliance** | Automated Policy Audits | Export compliance reports to SPDX JSON format for downstream tooling. | v0.5.0 |
| **Enterprise Reporting** | KPI Historical Store | Persist KPI snapshots to a lightweight SQLite DB for trend analysis. | v0.5.0 |

---

## 3️⃣ Missing / Technical Debt (To Implement)
| Area | Missing Piece | Reason | Plan |
|---|---|---|---|
| **Observability Suite** | Central `MetricsRegistry` persistence | Currently in‑memory only; loses data on restart. | Implement optional SQLite backend behind `execute=True` flag. |
| **Operations Control Center** | Configurable backup strategies | Backup dashboard exists but lacks execution logic. | Add `backup_dashboard.py` hooks to schedule and verify backups. |
| **Production API Gateway** | TLS termination & rate limiting | No security hardening yet. | Integrate `uvicorn` TLS config and `slowapi` middleware. |
| **CI/CD** | GitHub Actions workflow for automated release tagging | Manual tagging used so far. | Add workflow that runs tests, builds, and tags `vX.Y.0` on PR merge. |

---

## 4️⃣ Implementation Roadmap
### Phase 2 – **Operations Control Center (OCC)**
1. **Live Service Status** – finalize `default_service_statuses(execute=True)` (already merged) and add unit tests.  
2. **Dashboard UI** – create `/ops/status` endpoint rendering `render_health_dashboard` with live data.  
3. **Backup Automation** – implement `backup_dashboard` execution hooks, schedule via systemd timers.  
4. **Tests & Regression** – run full pytest suite, reach 100 % coverage for OCC.

### Phase 3 – **Production API Gateway (PAG)**
1. **Router Refactor** – replace static stub with `LiveRouter` that queries the service registry (from OCC).  
2. **Security Harden** – add TLS, OAuth2 token validation, and rate‑limiting middleware.  
3. **Observability Hooks** – instrument request latency and error counters via `MetricsRegistry`.  
4. **End‑to‑End Tests** – spin up a local Docker compose stack and run integration tests.

### Phase 4 – **Final Release & Governance**
1. **Full Documentation** – generate Sphinx site, embed live diagrams (Mermaid) for architecture.  
2. **Road‑to‑Production Checklist** – create `V0.5.0_TASK_CHECKLIST.md` with all required approvals.  
3. **Release Automation** – GitHub Actions pipeline to publish wheels, Docker images, and signed Git tags.  
4. **Post‑Release Monitoring** – enable alerting on KPI thresholds via the Observability Suite.

---

## 5️⃣ Milestones & Timeline (Assuming 1‑week sprints)
| Milestone | Date (approx.) | Deliverable |
|---|---|---|
| **M1 – OCC Live Dashboard** | 2026‑07‑05 | PR #72 merged, tests passed |
| **M2 – PAG Dynamic Router** | 2026‑07‑19 | PR #73 merged, integration tests |
| **M3 – Security Hardening** | 2026‑07‑26 | TLS & auth enabled, audit logs |
| **M4 – v0.5.0 Release Candidate** | 2026‑08‑02 | Full suite green, docs generated |
| **M5 – Production‑Ready GA** | 2026‑08‑09 | Signed tag `v0.5.0`, Docker images pushed |

---

## 📄 How to Use This Roadmap
- **Developers**: Pull the latest `V0.5.0_TASK_CHECKLIST.md` into your sprint board.  
- **Product Owners**: Review milestones and adjust dates based on capacity.  
- **Ops**: Prepare CI/CD runners for the upcoming GitHub Actions workflow.

*This document will be kept up‑to‑date in the repo’s `docs/` folder.*
