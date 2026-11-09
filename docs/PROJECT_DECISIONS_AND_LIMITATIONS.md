# Project Decisions and Limitations

## 1. Project Overview

The Insurance Underwriting System is a Python-based project that simulates an end-to-end insurance underwriting workflow.

The system generates synthetic insurance data, applies underwriting and premium calculation logic, validates business rules, and detects deliberately introduced anomalies.

## 2. Technology Decisions

| Technology | Purpose | Reason for Selection |
|---|---|---|
| Python | Core programming language | Supports data generation, validation, and business logic |
| SQLite | Database | Lightweight database suitable for this project |
| SQLAlchemy | Database interaction | Provides structured database models and relationships |
| Faker | Synthetic data generation | Helps generate realistic sample applicant information |
| Pandas | Data handling and exports | Supports structured data processing |
| CSV | Data export | Easy to inspect and analyze |
| JSON | Data export | Provides a structured, portable data format |
| SQL | Database export | Allows database records to be recreated |

## 3. Architecture Decisions

The project separates responsibilities into different modules.

### Database Layer

Contains database configuration and SQLAlchemy models.

### Generator Layer

Responsible for generating master data and dependent insurance transactions.

### Service Layer

Contains premium calculation and underwriting business logic.

### Anomaly Layer

Responsible for injecting deliberate anomalies and evaluating detection results.

### Validation Layer

Checks record counts, relationships, business rules, and anomaly results.

### Export Layer

Exports generated datasets into CSV, JSON, and SQL formats.

This modular structure makes the project easier to understand, maintain, and extend.

## 4. Important Business Logic Decisions

### Premium Calculation

The project uses a transparent premium calculation approach so that the calculated premium can be checked against the stored premium.

### Underwriting Decisions

Underwriting decisions consider eligibility and risk information. The system supports approval, referral, and decline outcomes.

### Policy Issuance

Policy issuance is subject to acceptance and payment conditions.

### Endorsements

Endorsements represent changes made to an existing insurance policy. Coverage limits must be respected.

### Renewals

Renewals represent the continuation of an existing policy and must respect policy lifecycle conditions.

### Lifecycle Events

Policy lifecycle events are stored to preserve a record of important policy state changes.

## 5. Data Generation Decisions

The project uses a fixed random seed:

`20261022`

This supports repeatable synthetic data generation.

The generated dataset includes:

| Entity | Records |
|---|---:|
| Applicants | 3,000 |
| Insured Assets | 3,000 |
| Products | 3 |
| Coverage Options | 6 |
| Risk Factors | 5 |
| Quotes | 4,000 |
| Policies | 2,000 |
| Endorsements | 200 |
| Renewals | 1,200 |
| Underwriting Decisions | 4,000 |

## 6. Anomaly Detection Approach

Five deliberate anomalies were introduced:

1. Policy issued without acceptance.
2. Premium outside the expected formula.
3. Endorsement exceeding the product coverage limit.
4. Renewal associated with a cancelled policy.
5. Overlapping policy periods without a permitted reason.

The anomaly detector checks these conditions and compares detected anomalies with the labelled ground-truth dataset.

## 7. Testing and Validation

The project was tested by running the data generation, validation, anomaly detection, evaluation, and export scripts.

The validation process checks:

- Entity record counts.
- Primary key uniqueness.
- Foreign key relationships.
- Policy acceptance and payment conditions.
- Premium consistency.
- Policy date validity.
- Ground-truth anomaly records.
- Detection results.

The anomaly evaluation on the five deliberately injected cases produced:

| Metric | Result |
|---|---:|
| True Positives | 5 |
| False Positives | 0 |
| False Negatives | 0 |
| Precision | 100% |
| Recall | 100% |
| F1 Score | 100% |

These metrics apply only to the five deliberately injected test cases, not to unseen production data.

## 8. Trade-offs

### SQLite Instead of a Production Database

SQLite was selected to keep the project simple to set up and execute.

A production system could use PostgreSQL or another database designed for concurrent workloads.

### Synthetic Instead of Real Insurance Data

Synthetic data avoids dependence on private customer information and allows controlled testing.

However, synthetic records cannot fully represent the complexity of real insurance portfolios.

### Rule-Based Anomaly Detection

The project uses explicit business-rule checks because the required anomalies have defined conditions.

A future version could explore statistical or machine-learning-based anomaly detection.

## 9. Current Limitations

- The project uses synthetic data rather than real insurance records.
- The anomaly evaluation covers five deliberately injected scenarios.
- The SQLite database is suitable for this demonstration but is not designed as a complete production deployment.
- The project does not represent a complete commercial insurance platform.
- Additional testing with larger and unseen datasets would be required before production use.
- Authentication, authorization, and production security controls would need further implementation.

## 10. Future Improvements

Possible improvements include:

1. Integrating a PostgreSQL database.
2. Building a web-based underwriting dashboard.
3. Adding authentication and role-based access.
4. Supporting additional insurance products.
5. Adding more complex risk scoring.
6. Testing against unseen anomaly scenarios.
7. Implementing automated unit and integration tests.
8. Adding API endpoints for external integrations.

## 11. Conclusion

The project demonstrates a structured insurance underwriting workflow using Python, database modelling, synthetic data generation, business-rule validation, and anomaly detection.

The design focuses on reproducibility, traceability, transparent calculations, and validation of important insurance business rules.