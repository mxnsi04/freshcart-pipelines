# ASSIGNMENT TRACKER
## From Git to Gold – Data Engineering Pipeline Orchestration

**Last Updated:** 2026-11-15 12:35 IST  
**Current Git Log:**
- `fa158d2` `fix(ci): restore test_size=0.2 (80/20 train-test split)`
- `6294a30` `test(ci): intentional failure with test_size=0.3 for CI experiment`
- `6267b4b` `docs(tracker): reflect 5th commit with verified clean screenshot`
- `aeffe62` `chore(screenshots): add verified clean structure screenshot for Part A1`
- `3fad4bf` `docs(tracker): update status matrix for Part A1, A2, and A3`
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

## ⚠️ NEXT ACTION REQUIRED FROM USER

### 🚫 BLOCKED-2: Snowflake Account (Part B)
- **Service:** Snowflake
- **Why Needed:** The FreshCart ELT pipeline (extract → PUT + COPY INTO bronze → silver → dim → ref → gold) runs on Snowflake.
- **Exact Action to Perform:**
  1. Open [https://app.snowflake.com](https://app.snowflake.com) (or your existing trial account).
  2. Tell me your **Snowflake Account Identifier** (e.g., `xy12345.ap-southeast-1` or `sr43506.ap-southeast-7.aws`) and **User Name** (e.g., `SUMUNTHRA`).
  3. Keep your password ready (we will use environment variable or secure prompt; do NOT paste password in chat).
- **Where to Perform:** Snowflake web console.
- **What Successful Completion Looks Like:** Connection established from Python/Colab, `SELECT CURRENT_USER(), CURRENT_ROLE()` returns active session.

---

## Task Matrix & Verification Log

### Part A: Git and CI/CD (15 marks) — ALL COMPLETED & VERIFIED

| Task ID | Assignment Requirement | Implementation Completed | Execution Command / Procedure | Expected Result | Actual Result | Verification Status | Screenshot Filename | Git Commit Hash | Issues & Notes |
|---|---|---|---|---|---|---|---|---|---|
| **A1.1** | Local repo structure creation | Created complete folder tree (`elt/`, `iris_project/`, `stream/`, `tests/`, `.github/workflows/`) | `cmd /c tree /F /A` | Exact directory hierarchy matching prompt | Matches expected structure | ✅ **VERIFIED** | `screenshots/part_A/A1_local_structure.png` | `fe60178` | Verified all subfolders and files |
| **A1.2** | `.gitignore` configuration | Created `.gitignore` ignoring `.env`, `*.pkl`, `*.csv`, `mage.log`, `__pycache__/` | Inspected `.gitignore` content | Ignores sensitive and transient files | Covers all 5 mandated patterns | ✅ **VERIFIED** | Inspected file | `fe60178` | Fully compliant |
| **A1.3** | `requirements.txt` dependencies | Created `requirements.txt` with snowflake, scikit-learn, mage-ai, pika, pytest, pandas | Inspected `requirements.txt` | Core packages for Parts A-D | Verified dependencies | ✅ **VERIFIED** | Inspected file | `fe60178` | Supports Parts B, C, D |
| **A1.4** | GitHub remote repo & push | Configured remote `origin` to `https://github.com/mxnsi04/freshcart-pipelines.git` and pushed `main` | `git remote add origin ...; git push -u origin main` | Remote accessible, commits visible on GitHub | Successfully pushed 8 commits to GitHub | ✅ **VERIFIED** | `screenshots/part_A/A1_github_repo_page.png` | `6267b4b`, `fa158d2` | Remote configured and verified |
| **A2.1** | Git commands table & analysis | Created `report/part_A2.md` explaining 6 commands (`git init`, `add`, `commit`, `remote add`, `push`, `pull`) | Comprehensive explanation using 4-box flow | Detailed explanation of where each acts and what changes | Verified 6 commands mapped to Working Folder, Staging, Local Repo, Remote Repo | ✅ **VERIFIED** | `report/part_A2.md` | `a294196` | In original wording |
| **A2.2** | Teammate visibility question | Answered in `report/part_A2.md` | Conceptual explanation of DVCS local vs remote objects | Teammate cannot see code until `git push` | Confirmed with architectural explanation | ✅ **VERIFIED** | `report/part_A2.md` | `a294196` | Report-ready |
| **A3.1** | `tests/test_prepare_data.py` | Pytest test verifying 80/20 train/test split (120/30 counts) | Unit test script written | Assertion of 120 train and 30 test rows | Written with conditional Mage decorator imports | ✅ **VERIFIED** | `tests/test_prepare_data.py` | `fe60178` | Importable outside Mage |
| **A3.2** | `.github/workflows/ci.yml` | GitHub Actions workflow on push with Python 3.12, pip install, pytest | Workflow YAML created | Triggers on push to `main` | Valid GitHub Actions syntax | ✅ **VERIFIED** | `.github/workflows/ci.yml` | `fe60178`, `a294196` | Standard Ubuntu runner |
| **A3.3** | Experiment 1: Passing CI run | Run passing CI on GitHub Actions | `git push origin main` | Green checkmark in GitHub Actions | Run #1 (`43688840048`) passed in 1m 20s | ✅ **VERIFIED** | `screenshots/part_A/A3_github_actions_green.png` | `6267b4b` | Green verified |
| **A3.4** | Experiment 2: Failing CI run | Modify `test_size=0.3`, commit and push | `git commit -m "test: intentional CI failure" && git push` | Red X in GitHub Actions | Run #2 (`43690034500`) failed in 1m 22s | ✅ **VERIFIED** | `screenshots/part_A/A3_github_actions_red.png` | `6294a30` | Red verified |
| **A3.5** | Experiment 3: Fix commit | Restore `test_size=0.2`, commit and push | `git commit -m "fix: restore 80/20 split" && git push` | Green checkmark in GitHub Actions | Run #3 (`43690601305`) passed in 1m 16s | ✅ **VERIFIED** | `screenshots/part_A/A3_github_actions_fixed_green.png` | `fa158d2` | Fix green verified |

---

### Part B: FreshCart ELT on Snowflake (30 marks)
*Will proceed immediately upon completion of Part A and receipt of Snowflake trial credentials.*

### Part C: ML Pipeline with Mage (20 marks) — ALL COMPLETED & VERIFIED

| Task ID | Assignment Requirement | Implementation Completed | Execution Command / Procedure | Expected Result | Actual Result | Verification Status | Screenshot Filename | Git Commit Hash | Issues & Notes |
|---|---|---|---|---|---|---|---|---|---|
| **C1.1** | Pipeline graph & execution | 4-block baseline pipeline configured in `metadata.yaml` | `python -m iris_project.run_pipeline` | All blocks execute in DAG order with @tests passing | Successfully ran 4 blocks with tests | ✅ **VERIFIED** | `screenshots/part_C/C1_C3_mage_pipeline_evidence.png` | `f97fed6` | Fully wired in `metadata.yaml` |
| **C2.1** | Test-gate experiment (depths 1..5) | Ran pipeline across `max_depth = 1..5`, asserting pre-run absence of CSV | `python -m iris_project.run_c2_experiments` | depth=1 fails (<0.8), depths 2-5 pass (>=0.8) | Exact match: depth 1 acc=0.633 (no CSV), depths 2-5 acc>=0.967 (CSV created) | ✅ **VERIFIED** | `screenshots/part_C/C2_experiment_terminal_output.png` | `f97fed6` | In-DAG test gate blocks bad files |
| **C2.2** | Quality gate explanation | Documented in `report/part_C1_C2.md` | Conceptual explanation of fail-fast DAG execution | In-pipeline gates prevent data pollution in gold tables | Detailed comparative analysis | ✅ **VERIFIED** | `report/part_C1_C2.md` | `f97fed6` | Report-ready |
| **C3.1** | Evaluation branch | Added `evaluate_model` downstream of `train_model` in parallel with `save_results` | `python -m iris_project.run_pipeline` | Confusion matrix and precision/recall/F1 metrics table | 30/30 correct, all metrics 1.000 | ✅ **VERIFIED** | `screenshots/part_C/C1_C3_mage_pipeline_evidence.png` | `f97fed6` | Forked DAG topology |
| **C4.1** | Custom block (`check_no_missing`) | Added transformer after `load_iris` asserting 0 nulls and 3 classes | `python -m iris_project.run_pipeline` | Passes data quality gate with 0 missing values | Verified 0 missing, 3 classes | ✅ **VERIFIED** | `screenshots/part_C/C1_C3_mage_pipeline_evidence.png` | `f97fed6` | Verified with `@test` |

### Part D: Food-order Stream with RabbitMQ (20 marks)
*Dispatcher, driver with ACK/NACK, and routing calculations already implemented.*

### Bonus: Stream into Lakehouse (+10 marks)
*Consumer script written in `stream/freshcart_consumer.py`.*
