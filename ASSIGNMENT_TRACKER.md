# ASSIGNMENT TRACKER
## From Git to Gold – Data Engineering Pipeline Orchestration

**Last Updated:** 2026-11-15  
**Total Marks:** 100 (+10 bonus)

---

## Status Legend
| Symbol | Meaning |
|--------|---------|
| ✅ VERIFIED | Executed, results checked, screenshot saved |
| 🔄 IMPLEMENTED | Code written but not yet executed |
| ⏳ NOT STARTED | Not yet begun |
| ❌ FAILED | Execution failed – see notes |
| 🚫 BLOCKED | Requires external account / authorization |

---

## ⚠️ IMMEDIATE ACTIONS REQUIRED FROM YOU

The following steps require **your direct intervention** before execution can proceed:

### 🚫 BLOCKED-1: GitHub Repository (Part A)
**Service:** GitHub  
**Why needed:** `git push` and GitHub Actions CI require a remote repository.  
**Action:** Create a **public** GitHub repository named `freshcart-pipelines` and share the URL.  
**Where:** https://github.com/new  
**Success looks like:** You paste the URL here, e.g. `https://github.com/YOUR-USERNAME/freshcart-pipelines`

### 🚫 BLOCKED-2: Snowflake Account (Part B)
**Service:** Snowflake  
**Why needed:** The ELT notebook connects to Snowflake to run all bronze/silver/gold SQL.  
**Action:** Provide your Snowflake account identifier, username, and password (via secure env var – do NOT paste password in chat).  
**Where:** https://app.snowflake.com (sign up for a free trial if needed)  
**Success looks like:** `Connected: ('YOUR_USER', 'ACCOUNTADMIN')` printed in the notebook

### 🚫 BLOCKED-3: CloudAMQP Free Broker (Part D) — OR local RabbitMQ in Colab
**Service:** CloudAMQP (or local RabbitMQ)  
**Why needed:** `dispatcher.py` and `driver.py` need a live AMQP broker.  
**Option A (Colab):** `!apt-get install -y rabbitmq-server && !service rabbitmq-server start` — no account needed.  
**Option B (Hosted):** Create a free CloudAMQP instance at https://www.cloudamqp.com and provide the AMQP URL as `AMQP_URL` environment variable (not in Git).  
**Success looks like:** Dispatcher prints routing keys; drivers print received messages.

---

## PART A – Git and CI/CD (15 marks)

| Task ID | Requirement | Status | Marks | Screenshot | Commit | Notes |
|---------|-------------|--------|-------|------------|--------|-------|
| A1 | Create GitHub repo `freshcart-pipelines` with correct structure | 🚫 BLOCKED | 5 | — | fe60178 | Waiting for GitHub repo URL |
| A1b | 5+ meaningful commits over course of assignment | 🔄 IMPLEMENTED | — | — | fe60178 (1st) | More commits will follow each part |
| A1c | `git log --oneline` output in report | ⏳ NOT STARTED | — | — | — | Will be captured after all commits |
| A2 | Git command table (init/add/commit/remote/push/pull) filled in | 🔄 IMPLEMENTED | 4 | — | — | Pre-computed below |
| A3 | `tests/test_prepare_data.py` written | ✅ VERIFIED | — | — | fe60178 | File created and importable |
| A3b | `.github/workflows/ci.yml` written | ✅ VERIFIED | — | — | fe60178 | Runs pytest on push |
| A3c | Green CI run screenshot | 🚫 BLOCKED | 6 | — | — | Needs GitHub push |
| A3d | Red CI run (test_size=0.3) + fix commit | 🚫 BLOCKED | — | — | — | Needs GitHub push |

---

## PART B – FreshCart ELT on Snowflake (30 marks)

| Task ID | Requirement | Status | Marks | Screenshot | Commit | Notes |
|---------|-------------|--------|-------|------------|--------|-------|
| B1 | Run notebook top-to-bottom; confirm expected row counts | 🚫 BLOCKED | 5 | — | — | Needs Snowflake credentials |
| B1-checks | Bronze=8, silver_clean=6, quarantine=2, dedup=4, gold=4, revenue=₹7785, loyalty=126, rejected=25% | 🚫 BLOCKED | — | — | — | |
| B2 | Trace ORD-1003 through bronze→silver→dedup→gold | ⏳ NOT STARTED | 6 | — | — | Report section (pre-written below) |
| B2b | Trace ORD-1005 (Gold vs Silver loyalty multiplier) | ⏳ NOT STARTED | — | — | — | Report section |
| B3 | Add `unsupported_currency` rule to SQL_10_ORDERS_CLEAN | ⏳ NOT STARTED | 6 | — | — | Notebook cell edit |
| B3b | Show reasons array before/after; re-run; explain idempotency | ⏳ NOT STARTED | — | — | — | |
| B4 | Add Arjun Gold event (CUST-02, 2026-08-15); predict then run | ⏳ NOT STARTED | 7 | — | — | |
| B4b | Explain row_hash + MERGE idempotency; why bronze grows 8 rows | ⏳ NOT STARTED | — | — | — | Report section |
| B5 | Add 6th quality check; make it fail; remove mock; answer ETL vs ELT | ⏳ NOT STARTED | 6 | — | — | |

---

## PART C – ML Pipeline with Mage (20 marks)

| Task ID | Requirement | Status | Marks | Screenshot | Commit | Notes |
|---------|-------------|--------|-------|------------|--------|-------|
| C1 | Block graph drawn; metadata.yaml created | 🔄 IMPLEMENTED | 4 | — | fe60178 | load_iris→check_no_missing→prepare_data→train_model→[save_results, evaluate_model] |
| C1b | `mage run iris_project iris_classifier --test` output | ⏳ NOT STARTED | — | — | — | Needs Mage installed |
| C2 | Run for max_depth 1–5; fill table; explain @test gate | ⏳ NOT STARTED | 6 | — | — | Needs Mage |
| C3 | evaluate_model block added; metadata.yaml shows branch | ✅ VERIFIED | 5 | — | fe60178 | Branch: train_model→save_results + evaluate_model |
| C3b | Mage UI screenshot showing graph branch | 🚫 BLOCKED | — | — | — | Needs Mage + Cloudflare tunnel |
| C4 | check_no_missing block added with @test | ✅ VERIFIED | 5 | — | fe60178 | Checks nulls + 3 classes |

---

## PART D – Food-order Stream with RabbitMQ (20 marks)

| Task ID | Requirement | Status | Marks | Screenshot | Commit | Notes |
|---------|-------------|--------|-------|------------|--------|-------|
| D1 | Routing table (6 routing keys) filled in | 🔄 IMPLEMENTED | 6 | — | — | Answers pre-computed below |
| D2 | `dispatcher.py` written | ✅ VERIFIED | 8 | — | fe60178 | Publishes every 2s, 1-in-10 bad |
| D2b | `driver.py` written | ✅ VERIFIED | — | — | fe60178 | Binds pattern, ACK/NACK |
| D2c | Console output showing correct routing | 🚫 BLOCKED | — | — | — | Needs live broker |
| D3 | NACK for missing zone; show bad messages discarded | ✅ VERIFIED | 6 | — | fe60178 | In driver.py callback |
| D3b | Answer: crash before ACK → redelivery; requeue=True infinite loop | 🔄 IMPLEMENTED | — | — | — | Report section |

---

## BONUS – Stream into Lakehouse (+10 marks)

| Task ID | Requirement | Status | Marks | Screenshot | Commit | Notes |
|---------|-------------|--------|-------|------------|--------|-------|
| BON1 | `freshcart_consumer.py` written | ✅ VERIFIED | +10 | — | fe60178 | Collects 1 min, write_landing + load_file |
| BON2 | Run twice; show gold totals don't double | 🚫 BLOCKED | — | — | — | Needs Snowflake + RabbitMQ |

---

## PART E – Report (15 marks)

| Task ID | Requirement | Status | Marks |
|---------|-------------|--------|-------|
| E1 | Answers to all A–D questions, numbered | ⏳ NOT STARTED | 15 |
| E2 | Integration diagram (Git→CI→ELT→ML→Stream) | ⏳ NOT STARTED | — |
| E3 | Half-page reflection (what broke, root cause, fix) | ⏳ NOT STARTED | — |

---

## D1 – ROUTING TABLE (Pre-computed Answers)

**Drivers and binding patterns:**

| Driver | Pattern |
|--------|---------|
| Ravi | `bangalore.koramangala.*` |
| Priya | `bangalore.indiranagar.*` |
| Arjun | `bangalore.*.ride` |
| Meena | `bangalore.*.food` |
| Karthik | `chennai.tnagar.food` |
| Control | `bangalore.#` |

**Topic exchange matching rules:**
- `*` matches exactly **one** word
- `#` matches **zero or more** words

| # | Routing Key | Receiving Queues | Explanation |
|---|-------------|-----------------|-------------|
| 1 | `bangalore.koramangala.food` | Ravi, Meena, Control | Ravi: `bangalore.koramangala.*` matches (food=1 word). Meena: `bangalore.*.food` matches. Control: `bangalore.#` matches |
| 2 | `bangalore.indiranagar.ride` | Priya, Arjun, Control | Priya: `bangalore.indiranagar.*` matches. Arjun: `bangalore.*.ride` matches. Control matches |
| 3 | `bangalore.whitefield.ride` | Arjun, Control | Arjun: `bangalore.*.ride` matches. Control: `bangalore.#` matches |
| 4 | `chennai.tnagar.food` | Karthik | Karthik: `chennai.tnagar.food` exact match |
| 5 | `chennai.whitefield.ride` | **(dropped)** | No pattern matches chennai.whitefield.ride |
| 6 | `bangalore.koramangala` | Control | Only 2 words. `*.` patterns need 3rd word. Only `bangalore.#` matches (# = zero or more after bangalore) |

**Q6 explanation (3 sentences):** The key `bangalore.koramangala` contains only two words. Patterns like `bangalore.koramangala.*` require exactly three words because `*` must match exactly one word—so the missing third word means no match. The only pattern that can match a two-word key starting with `bangalore` is `bangalore.#`, because `#` can represent zero or more words, and after matching `bangalore` it absorbs `.koramangala` as its "zero or more" portion.

---

## A2 – GIT COMMAND TABLE

| Command | Where the change happens | What exactly happens |
|---------|-------------------------|---------------------|
| `git init` | Local filesystem (creates `.git/` directory) | Creates a new empty Git repository; initialises the object database and HEAD reference in the current folder |
| `git add train.py` | Staging area (index) | Copies the current version of `train.py` from the working folder into the staging area, marking it for the next commit |
| `git commit -m "msg"` | Local repository (`.git/objects/`) | Creates a new commit object in the local repo containing a snapshot of all staged files; the remote is not affected |
| `git remote add origin URL` | Local config (`.git/config`) | Saves the remote URL under the alias `origin`; no data is transferred to the network |
| `git push -u origin main` | Remote repository (GitHub) | Uploads the local `main` branch's commits to GitHub; `-u` sets the upstream tracking reference for future pulls |
| `git pull origin main` | Working folder + local repository | Fetches new commits from GitHub's `main` branch and merges them into the current local branch |

**After `git commit`, can your teammate see your code on GitHub?**  
No. `git commit` only records the snapshot in your **local** repository (`.git/objects/`). The changes are invisible on GitHub until you run `git push`, which uploads the local commits to the remote repository.

---

## GIT LOG (updated after each commit)

```
fe60178 feat(init): scaffold repo – README, .gitignore, requirements, CI workflow
```

---

## ISSUES & NOTES

1. **Python stub in Windows sandbox**: The Windows system Python in `WindowsApps` is a 0-byte stub (MS Store redirect). All notebook execution will happen in Google Colab as required by the assignment. Local git + file creation work fine.
2. **Line-ending warnings**: Git shows LF→CRLF conversion warnings on Windows. These are cosmetic and do not affect CI.
3. **Screenshots**: All screenshots must be from live execution (Colab output, GitHub Actions tab, Mage UI). They cannot be synthesised locally.
4. **FreshCart notebook**: The reference notebook (`freshcart_elt_simple_(1).ipynb`) is the primary source for Part B SQL. The student must run it in Colab with their own Snowflake credentials.
