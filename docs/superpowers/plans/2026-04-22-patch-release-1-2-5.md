# Patch Release 1.2.5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prepare a patch release version 1.2.5 with a security enhancement.

**Architecture:** Bump version in `pyproject.toml` and add new entry to `CHANGELOG.md`.

**Tech Stack:** Python, uv, git

---

### Task 1: Research and Research (Already done)

- [x] **Step 1: Check current version in `pyproject.toml`**
- [x] **Step 2: Check git tags to confirm last version**
- [x] **Step 3: Determine changes for the next release**

### Task 2: Update Version and Changelog

**Files:**
- Modify: `pyproject.toml`
- Modify: `CHANGELOG.md`

- [ ] **Step 1: Update version to 1.2.5 in `pyproject.toml`**

Replace `version = "1.2.4"` with `version = "1.2.5"`.

- [ ] **Step 2: Add version 1.2.5 entry to `CHANGELOG.md`**

Insert at the top:
```markdown
# 1.2.5

## Security

- Security enhancement: Add type validation for 'action' in 'allowed()'.
```

### Task 3: Verification

- [ ] **Step 1: Run all tests to ensure stability**

Run: `pytest`

- [ ] **Step 2: Verify version in code matches pyproject.toml (if applicable)**

Check if `src/tagth/__init__.py` or similar has a `__version__`.

### Task 4: Finalize

- [ ] **Step 1: Propose commit with changes**

Commit message: `chore: bump version to 1.2.5`
