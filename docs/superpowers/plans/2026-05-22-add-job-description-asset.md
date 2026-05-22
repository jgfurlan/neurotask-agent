# Add Job Description Asset Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Copy the Job Description PDF from the local system to the project's documentation assets and rename it for consistency.

**Architecture:** Create a `docs/assets/` directory and use standard shell commands to copy and rename the file.

**Tech Stack:** Bash

---

### Task 1: Create Assets Directory

**Files:**
- Create: `docs/assets/`

- [ ] **Step 1: Create the directory**

Run: `mkdir -p docs/assets`

- [ ] **Step 2: Verify directory exists**

Run: `ls -d docs/assets`
Expected: `docs/assets`

---

### Task 2: Copy and Rename Job Description

**Files:**
- Create: `docs/assets/job-description.pdf`

- [ ] **Step 1: Copy the file from source to destination**

Run: `cp "/mnt/c/Users/joaog/Downloads/JD_Carnival-AI_ML_Engineer.pdf" "docs/assets/job-description.pdf"`

- [ ] **Step 2: Verify file exists and has content**

Run: `ls -lh docs/assets/job-description.pdf`
Expected: File size around 77K.

---

### Task 3: Final Verification

- [ ] **Step 1: Verify file is a PDF**

Run: `file docs/assets/job-description.pdf`
Expected: `docs/assets/job-description.pdf: PDF document...`
