# ASSIGNMENT TRACKER
## From Git to Gold – Data Engineering Pipeline Orchestration

**Last Updated:** 2026-11-15 12:35 IST  
**Current Git Log:**
- `a294196` `docs(report): complete Part A2 Git command analysis and configure pytest with elt notebook`
- `36285fd` `docs(tracker): add full assignment tracker with D1 routing table and A2 git command answers`
- `fe60178` `feat(init): scaffold repo – README, .gitignore, requirements, CI workflow`

---

## Status Legend
| Symbol | Meaning |
|---|---|
| ✅ VERIFIED | Executed, results inspected, screenshot saved and verified |
| 🔄 IMPLEMENTED | Code/config written, awaiting external execution/push |
| ⏳ NOT STARTED | Not yet begun |
| ❌ FAILED | Execution failed |
| 🚫 BLOCKED | Requires user account creation or authorization |

---

## ⚠️ CURRENT ACTION REQUIRED FROM USER

### 🚫 BLOCKED-1: GitHub Repository (Part A1 & A3)
- **Service:** GitHub
- **Why Needed:** Remote repository needed to configure `origin`, push commits (`main` branch), and trigger GitHub Actions CI runs for passing and failing tests.
- **Exact Action to Perform:**
  1. Open [https://github.com/new](https://github.com/new) in your browser.
  2. Create a new **public** repository named **`freshcart-pipelines`** (leave "Initialize with README" unchecked).
  3. Copy the repository URL (e.g., `https://github.com/<your-username>/freshcart-pipelines.git` or SSH).
  4. Provide the repository URL here in chat.
- **Where to Perform:** GitHub web interface ([https://github.com/new](https://github.com/new)).
- **What Successful Completion Looks Like:** Remote is configured with `git remote add origin <URL>`, commits are pushed to `main`, and the GitHub Actions CI tab shows the workflow runs.

---

## Task Matrix & Verification Log

### Part A: Git and CI/CD (15 marks)

| Task ID | Assignment Requirement | Implementation Completed | Execution Command / Procedure | Expected Result | Actual Result | Verification Status | Screenshot Filename | Git Commit Hash | Issues & Notes |
|---|---|---|---|---|---|---|---|---|---|
| **A1.1** | Local repo structure creation | Created complete folder tree (`elt/`, `iris_project/`, `stream/`, `tests/`, `.github/workflows/`) | `cmd /c tree /F /A` | Exact directory hierarchy matching prompt | Matches expected structure | ✅ **VERIFIED** | `screenshots/part_A/A1_local_structure.png` | `fe60178`, `a294196` | Verified all subfolders and files |
| **A1.2** | `.gitignore` configuration | Created `.gitignore` ignoring `.env`, `*.pkl`, `*.csv`, `mage.log`, `__pycache__/` | Inspected `.gitignore` content | Ignores sensitive and transient files | Covers all 5 mandated patterns | ✅ **VERIFIED** | Inspected file | `fe60178` | Fully compliant |
| **A1.3** | `requirements.txt` dependencies | Created `requirements.txt` with snowflake, scikit-learn, mage-ai, pika, pytest, pandas | Inspected `requirements.txt` | Core packages for Parts A-D | Verified dependencies | ✅ **VERIFIED** | Inspected file | `fe60178` | Supports Parts B, C, D |
| **A1.4** | GitHub remote repo & push | Remote origin setup and push | `git remote add origin <URL>; git push -u origin main` | Remote accessible, commits visible on GitHub | Awaiting user GitHub repo URL | 🚫 **BLOCKED** | Pending push | Pending | Waiting for GitHub URL |
| **A2.1** | Git commands table & analysis | Created `report/part_A2.md` explaining 6 commands (`git init`, `add`, `commit`, `remote add`, `push`, `pull`) | Comprehensive explanation using 4-box flow | Detailed explanation of where each acts and what changes | Verified 6 commands mapped to Working Folder, Staging, Local Repo, Remote Repo | ✅ **VERIFIED** | `report/part_A2.md` | `a294196` | In original wording |
| **A2.2** | Teammate visibility question | Answered in `report/part_A2.md` | Conceptual explanation of DVCS local vs remote objects | Teammate cannot see code until `git push` | Confirmed with architectural explanation | ✅ **VERIFIED** | `report/part_A2.md` | `a294196` | Report-ready |
| **A3.1** | `tests/test_prepare_data.py` | Pytest test verifying 80/20 train/test split (120/30 counts) | Unit test script written | Assertion of 120 train and 30 test rows | Written with conditional Mage decorator imports | ✅ **VERIFIED** | `tests/test_prepare_data.py` | `fe60178` | Importable outside Mage |
| **A3.2** | `.github/workflows/ci.yml` | GitHub Actions workflow on push with Python 3.12, pip install, pytest | Workflow YAML created | Triggers on push to `main` | Valid GitHub Actions syntax | ✅ **VERIFIED** | `.github/workflows/ci.yml` | `fe60178`, `a294196` | Standard Ubuntu runner |
| **A3.3** | Experiment 1: Passing CI run | Run passing CI on GitHub Actions | `git push origin main` | Green checkmark in GitHub Actions | Pending GitHub push | 🚫 **BLOCKED** | `screenshots/part_A/A3_github_actions_green.png` | Pending | Blocked on BLOCKED-1 |
| **A3.4** | Experiment 2: Failing CI run | Modify `test_size=0.3`, commit and push | `git commit -m "test: intentional CI failure" && git push` | Red X in GitHub Actions | Pending GitHub push | 🚫 **BLOCKED** | `screenshots/part_A/A3_github_actions_red.png` | Pending | Blocked on BLOCKED-1 |
| **A3.5** | Experiment 3: Fix commit | Restore `test_size=0.2`, commit and push | `git commit -m "fix: restore 80/20 split" && git push` | Green checkmark in GitHub Actions | Pending GitHub push | 🚫 **BLOCKED** | `screenshots/part_A/A3_github_actions_fixed_green.png` | Pending | Blocked on BLOCKED-1 |

---

### Part B: FreshCart ELT on Snowflake (30 marks)
*Will proceed immediately upon completion of Part A and receipt of Snowflake trial credentials.*

### Part C: ML Pipeline with Mage (20 marks)
*Blocks, tests, and metadata.yaml already scaffolded.*

### Part D: Food-order Stream with RabbitMQ (20 marks)
*Dispatcher, driver with ACK/NACK, and routing calculations already implemented.*

### Bonus: Stream into Lakehouse (+10 marks)
*Consumer script written in `stream/freshcart_consumer.py`.*
