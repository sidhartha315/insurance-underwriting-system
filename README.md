# Insurance Underwriting System

### Synthetic Insurance Data Generation, Underwriting Simulation & Anomaly Detection

## 1. Project Overview

The Insurance Underwriting System is a Python-based project designed to simulate an end-to-end insurance underwriting workflow.

The system generates synthetic insurance data and evaluates applications based on product eligibility, coverage limits, applicant risk factors and premium calculation rules.

It simulates the insurance lifecycle, including:

- Applicant and insured asset creation
- Insurance product and coverage configuration
- Risk factor evaluation
- Quote generation
- Underwriting decisions
- Policy creation
- Policy endorsements
- Policy renewals
- Lifecycle event tracking
- Anomaly injection and detection
- Data validation and export

The project focuses on generating realistic, structured insurance datasets while maintaining data relationships, business rules and reproducibility.

## 2. Project Objectives

The main objectives are:

1. Generate synthetic insurance master data and transaction data.
2. Simulate insurance underwriting decisions.
3. Calculate premiums using a transparent formula.
4. Apply product eligibility and risk assessment rules.
5. Generate policies, endorsements and renewals.
6. Maintain policy lifecycle events.
7. Introduce deliberate data anomalies for testing.
8. Detect and evaluate anomalies.
9. Validate data integrity and business rules.
10. Export datasets in CSV, JSON and SQL formats.

## 3. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| SQLAlchemy | Database ORM |
| SQLite | Relational database |
| Pandas | Data processing and analysis |
| NumPy | Numerical operations |
| Faker | Synthetic data generation |
| CSV | Dataset export |
| JSON | Structured data export |
| SQL | Database seed export |
| Git & GitHub | Version control and project hosting |

## 4. Project Architecture

```text
insurance-underwriting-system/
│
├── app/
│   ├── __init__.py
│   └── main.py
│
├── docs/
│   ├── data_dictionary.md
│   ├── schema.md
│   ├── AI_USAGE_AND_PROMPT_HISTORY.md
│   └── PROJECT_DECISIONS_AND_LIMITATIONS.md
│
├── outputs/
│   ├── datasets/
│   │   ├── csv/
│   │   ├── json/
│   │   └── sql/
│   ├── ground_truth/
│   ├── validation_report.csv
│   ├── validation_report.json
│   └── source_manifest.json
│
├── scripts/
│   ├── validate_data.py
│   ├── export_data.py
│   └── create_manifest.py
│
├── src/
│   ├── anomaly/
│   │   ├── inject_anomalies.py
│   │   └── evaluate_anomalies.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   └── models.py
│   │
│   ├── generators/
│   │   ├── master_data.py
│   │   └── transaction_data.py
│   │
│   ├── services/
│   │   ├── premium.py
│   │   └── underwriting.py
│   │
│   └── validation/
│       ├── checks.py
│       └── anomaly_detector.py
│
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
├── Insurance_Underwriting_Submission.zip
└── README.md
```

## 5. Core Business Entities

The system contains the following entities:

| Entity | Description |
|---|---|
| Applicant | Stores applicant information |
| InsuredAsset | Stores insured asset details |
| Product | Defines insurance products |
| CoverageOption | Defines available coverage options |
| RiskFactor | Stores underwriting risk factors |
| Quote | Stores insurance quotations |
| Policy | Stores issued policy information |
| Endorsement | Stores mid-term policy changes |
| Renewal | Stores policy renewal information |
| UnderwritingDecision | Records underwriting decisions |
| PolicyEvent | Tracks policy lifecycle events |

Applicants and risk factors are connected through a many-to-many relationship.

## 6. Dataset Volume

The system generates the following synthetic dataset:

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
| Policy Events | 2,000 |

**Total records across these entities: 19,414.**

The generator uses a fixed random seed of `20261022` to support reproducibility.

## 7. Underwriting Workflow

The system simulates the following workflow:

```text
Master Data Generation
        |
        v
Applicant and Asset Creation
        |
        v
Product and Coverage Selection
        |
        v
Risk Factor Evaluation
        |
        v
Quote Generation
        |
        v
Premium Calculation
        |
        v
Underwriting Decision
        |
        v
Approval / Referral / Decline
        |
        v
Policy Generation
        |
        v
Endorsements and Renewals
        |
        v
Lifecycle Event Tracking
        |
        v
Anomaly Detection and Validation
        |
        v
CSV / JSON / SQL Export
```

## 8. Premium Calculation

The system calculates insurance premiums using coverage amount, product base rate and applicant risk multipliers.

**Premium Formula:**

```text
Premium = Coverage Amount × Product Base Rate × Risk Multiplier
```

When multiple risk factors are associated with an applicant, their multipliers are combined.

The final premium is rounded to two decimal places.

Example:

```python
multiplier = 1.0

for risk in applicant.risk_factors:
    multiplier *= float(risk.multiplier)

premium = round(
    coverage * float(product.base_rate) * multiplier,
    2
)
```

This provides a transparent and explainable premium calculation.

## 9. Underwriting Decisions

The system evaluates insurance applications using product eligibility and risk information.

The underwriting workflow supports:

- Approved applications
- Referred applications
- Declined applications
- Risk score calculation
- Missing risk information handling
- Product eligibility checks

Applications requiring additional underwriting review can be referred instead of being automatically approved.

## 10. Policy Lifecycle

The system simulates important insurance policy lifecycle activities.

### Policy Creation

Policies are generated from approved quotes.

### Endorsements

Endorsements represent changes to existing policies, including asset value updates.

### Renewals

The system generates renewal records with different renewal statuses, including:

- OFFERED
- ACCEPTED
- DECLINED

### Lifecycle Events

Policy events are stored to maintain a record of policy lifecycle activity.

## 11. Deliberate Anomaly Scenarios

Five deliberate anomalies are injected into the generated datasets to test the anomaly detection system.

| No. | Anomaly | Description |
|---|---|---|
| 1 | POLICY_WITHOUT_ACCEPTANCE | Policy issued without customer acceptance |
| 2 | PREMIUM_MISMATCH | Premium differs from the expected calculation |
| 3 | END