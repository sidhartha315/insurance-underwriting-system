# AI Usage and Prompt History

## 1. Overview

AI assistance was used during the development of the Insurance Underwriting System to accelerate implementation, understand technical concepts, troubleshoot errors, and improve project documentation.

The primary AI assistant used was ChatGPT.

AI was used as a development assistant. Generated suggestions and code were reviewed and tested during implementation.

## 2. AI Tools Used

| Tool | Purpose |
|---|---|
| ChatGPT | Technical guidance, code assistance, debugging, validation logic, documentation, and GitHub workflow guidance |

## 3. Prompt History

The following entries summarize the main categories of prompts used during development. They are summaries of the assistance requested, not verbatim transcripts.

### Prompt 1: Understanding the Project Requirements

**Objective:** Understand the insurance underwriting challenge and break it into manageable development tasks.

**Prompt summary:**

Help me understand the insurance underwriting system requirements, identify the necessary entities, business rules, data relationships, and implementation steps.

**AI assistance:**
- Explained the project requirements.
- Helped organize the development workflow.
- Identified important entities and transaction relationships.
- Helped plan data generation and validation.

### Prompt 2: Database Design

**Objective:** Develop the database structure.

**Prompt summary:**

Help me design the database models for an insurance underwriting system, including applicants, insured assets, products, coverage options, risk factors, quotes, policies, endorsements, renewals, and underwriting decisions.

**AI assistance:**
- Provided database design guidance.
- Helped define entity relationships.
- Assisted with SQLAlchemy model structure.
- Helped identify primary and foreign key relationships.

### Prompt 3: Synthetic Data Generation

**Objective:** Generate realistic sample insurance data.

**Prompt summary:**

Help me create Python scripts to generate master data and dependent insurance transactions using a fixed random seed.

**AI assistance:**
- Assisted with master data generation.
- Helped organize transaction generation.
- Provided guidance on reproducibility.
- Helped implement the required data volumes.

### Prompt 4: Premium Calculation and Underwriting

**Objective:** Implement insurance business logic.

**Prompt summary:**

Help me implement a transparent premium calculation formula and underwriting decision logic based on eligibility, risk factors, coverage limits, and approval rules.

**AI assistance:**
- Explained premium calculation logic.
- Assisted with Python service structure.
- Helped organize underwriting decisions.
- Supported implementation of risk-based referrals.

### Prompt 5: Anomaly Injection and Detection

**Objective:** Create and detect deliberate data anomalies.

**Prompt summary:**

Help me implement five deliberate anomalies and build validation logic to identify them.

**AI assistance:**
- Helped implement the five required anomaly scenarios.
- Assisted with anomaly detection logic.
- Helped compare detected anomalies against labelled ground truth.
- Supported precision, recall, and F1-score evaluation.

### Prompt 6: Validation and Debugging

**Objective:** Verify generated data and troubleshoot implementation issues.

**Prompt summary:**

Help me validate entity counts, primary keys, foreign keys, business rules, premium calculations, lifecycle conditions, and anomaly detection results. Help troubleshoot errors shown by my Python scripts.

**AI assistance:**
- Helped interpret terminal output.
- Assisted with debugging file paths and validation logic.
- Helped verify expected record counts.
- Supported validation report generation.

### Prompt 7: Data Export and Documentation

**Objective:** Prepare the project for assessment.

**Prompt summary:**

Help me export the generated datasets into CSV, JSON, and SQL formats and prepare the README, schema documentation, data dictionary, and source manifest.

**AI assistance:**
- Assisted with export workflow.
- Helped structure documentation.
- Explained project setup and execution instructions.
- Helped organize output files.

### Prompt 8: Git and GitHub Submission

**Objective:** Publish the completed project.

**Prompt summary:**

Guide me through initializing Git, creating a public GitHub repository, preparing the project files, committing changes, and pushing the project to GitHub.

**AI assistance:**
- Explained Git commands.
- Helped configure `.gitignore`.
- Assisted with repository preparation.
- Guided the GitHub upload process.

## 4. Where AI Accelerated Development

AI assistance was particularly useful for:

- Understanding the project requirements.
- Structuring Python modules and database models.
- Developing synthetic data generation workflows.
- Implementing validation and anomaly detection.
- Troubleshooting errors.
- Preparing technical documentation.

## 5. My Contribution and Verification

I worked through the implementation process by executing commands, integrating project files, reviewing outputs, and checking the results.

The following activities were performed during project development:

- Created and ran the project environment.
- Executed database initialization and data generation scripts.
- Generated the required insurance datasets.
- Executed validation and anomaly detection scripts.
- Reviewed the anomaly evaluation metrics.
- Exported datasets into CSV, JSON, and SQL.
- Prepared the project documentation.
- Initialized Git and uploaded the repository to GitHub.

## 6. Validation Results

The implemented test dataset contained five deliberately injected anomalies.

The evaluation produced:

| Metric | Result |
|---|---:|
| True Positives | 5 |
| False Positives | 0 |
| False Negatives | 0 |
| Precision | 1.00 |
| Recall | 1.00 |
| F1 Score | 1.00 |

These results represent performance on the five deliberately injected test anomalies. They should not be interpreted as evidence of equivalent performance on unseen real-world insurance data.

## 7. Responsible AI Usage

AI-generated suggestions were used as development assistance. The project was executed and its outputs were checked through the available scripts.

This document summarizes the main categories of AI assistance used during development. It is not a verbatim record of every conversation or prompt.

The final implementation, its limitations, and its validation results should be explained honestly during the technical review.