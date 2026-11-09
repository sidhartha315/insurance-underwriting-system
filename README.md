# Insurance Underwriting System

## 1. Project Overview

The Insurance Underwriting System is a Python-based synthetic data generation and validation project that simulates an end-to-end insurance underwriting workflow.

It evaluates insurance applications and renewals using product eligibility, coverage limits, risk factors and premium calculation rules.

The system generates synthetic data, applies underwriting decisions, creates policies, generates renewals and endorsements, detects anomalies and exports datasets.

## 2. Technologies Used

- Python
- SQLAlchemy
- SQLite
- Pandas
- NumPy
- Faker
- CSV
- JSON
- SQL

## 3. Project Architecture

```text
insurance-underwriting-system/
│
├── database/
├── docs/
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
├── prompts/
├── scripts/
│   ├── generate_data.py
│   ├── validate_data.py
│   ├── export_data.py
│   └── create_manifest.py
│
└── src/
    ├── anomaly/
    ├── database/
    ├── generators/
    ├── services/
    └── validation/
```

## 4. Core Entities

1. Applicant
2. InsuredAsset
3. Product
4. CoverageOption
5. RiskFactor
6. Quote
7. Policy
8. Endorsement
9. Renewal
10. UnderwritingDecision

A many-to-many relationship connects applicants and risk factors through an association table.

## 5. Dataset Volume

| Entity | Records |
|---|---:|
| Applicants | 3,000 |
| Insured Assets | 3,000 |
| Products | 3 |
| Coverage Options | 6 |
| Risk Factors | 5 |
| Quotes |