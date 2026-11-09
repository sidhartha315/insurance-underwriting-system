# Insurance Underwriting System — Data Dictionary

## 1. Overview

This document describes the database entities, fields, data types, relationships, primary keys, foreign keys and validation considerations for the Insurance Underwriting System.

The database uses SQLAlchemy ORM with SQLite.

## 2. Entity Dictionary

### 2.1 Applicant

Table: `applicants`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique applicant identifier | Primary key; unique |
| name | String | Yes | Applicant name | Cannot be null |
| age | Integer | No | Applicant age | Must be a valid age |
| income | Float | No | Annual applicant income | Non-negative |
| location | String | No | Applicant location | Text |
| created_at | DateTime | No | Applicant creation timestamp | Defaults to UTC timestamp |

### 2.2 InsuredAsset

Table: `insured_assets`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique asset identifier | Primary key |
| applicant_id | String | No | Asset owner identifier | Foreign key to applicants.id |
| asset_type | String | No | Type of insured asset | Text |
| asset_value | Float | No | Estimated asset value | Non-negative |
| location | String | No | Asset location | Text |

### 2.3 Product

Table: `products`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique product identifier | Primary key |
| name | String | Yes | Product name | Cannot be null |
| product_line | String | No | Product category | Text |
| base_rate | Float | No | Base premium rate | Non-negative |
| min_age | Integer | No | Minimum applicant age | Valid age |
| max_age | Integer | No | Maximum applicant age | Must be >= min_age |
| max_coverage | Float | No | Maximum permitted coverage | Positive |
| active | Boolean | No | Product availability | Defaults to True |

### 2.4 CoverageOption

Table: `coverage_options`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique coverage option identifier | Primary key |
| product_id | String | No | Associated product identifier | Foreign key to products.id |
| name | String | No | Coverage option name | Text |
| coverage_limit | Float | No | Maximum coverage for option | Positive |
| additional_rate | Float | No | Additional premium rate | Non-negative |

### 2.5 RiskFactor

Table: `risk_factors`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique risk factor identifier | Primary key |
| name | String | No | Risk factor name | Text |
| factor_type | String | No | Risk category | Text |
| multiplier | Float | No | Premium adjustment multiplier | Positive |
| description | Text | No | Risk factor explanation | Text |

### 2.6 Quote

Table: `quotes`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique quote identifier | Primary key |
| applicant_id | String | No | Applicant requesting quote | Foreign key to applicants.id |
| product_id | String | No | Selected product | Foreign key to products.id |
| asset_id | String | No | Insured asset | Foreign key to insured_assets.id |
| coverage_amount | Float | No | Requested coverage | Positive and within product limit |
| calculated_premium | Float | No | Calculated premium | Must reconcile with premium formula |
| status | String | No | Quote lifecycle status | Application-level validation |
| created_at | DateTime | No | Quote creation timestamp | Defaults to UTC timestamp |

### 2.7 Policy

Table: `policies`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique policy identifier | Primary key |
| quote_id | String | No | Source quote identifier | Foreign key to quotes.id |
| applicant_id | String | No | Policyholder identifier | Foreign key to applicants.id |
| start_date | Date | No | Policy start date | Valid date |
| end_date | Date | No | Policy end date | Must be after start_date |
| premium | Float | No | Policy premium | Must reconcile with quote |
| status | String | No | Policy lifecycle status | Application-level validation |
| accepted | Boolean | No | Customer acceptance | Defaults to False |
| payment_received | Boolean | No | Payment confirmation | Defaults to False |

### 2.8 Endorsement

Table: `endorsements`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique endorsement identifier | Primary key |
| policy_id | String | No | Associated policy identifier | Foreign key to policies.id |
| change_type | String | No | Type of policy change | Application-level validation |
| old_value | Float | No | Previous value | Numeric |
| new_value | Float | No | Updated value | Numeric; must respect product limits |
| created_at | DateTime | No | Endorsement creation timestamp | Defaults to UTC timestamp |

### 2.9 Renewal

Table: `renewals`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique renewal identifier | Primary key |
| policy_id | String | No | Original policy identifier | Foreign key to policies.id |
| renewal_date | Date | No | Renewal effective date | Valid date |
| offered_premium | Float | No | Proposed renewal premium | Non-negative |
| status | String | No | Renewal lifecycle status | Application-level validation |

### 2.10 UnderwritingDecision

Table: `underwriting_decisions`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | String | Yes | Unique decision identifier | Primary key |
| quote_id | String | No | Evaluated quote identifier | Foreign key to quotes.id |
| decision | String | No | Underwriting result | Application-level validation |
| risk_score | Float | No | Calculated risk score | Valid numeric score |
| reason | Text | No | Decision explanation | Text |
| reviewer | String | No | Reviewer identifier | Text |
| created_at | DateTime | No | Decision timestamp | Defaults to UTC timestamp |

### 2.11 PolicyEvent

Table: `policy_events`

| Field | Data Type | Required | Description | Validation |
|---|---|---|---|---|
| id | Integer | Yes | Unique event identifier | Auto-increment primary key |
| policy_id | String | No | Associated policy | Foreign key to policies.id |
| event_type | String | No | Event description | Application-level validation |
| previous_status | String | No | Previous policy status | Text |
| new_status | String | No | New policy status | Text |
| created_at | DateTime | No | Event timestamp | Defaults to UTC timestamp |

## 3. Relationship and Cardinality

| Parent Entity | Child Entity | Relationship | Description |
|---|---|---|---|
| Applicant | InsuredAsset | 1:N | One applicant can own multiple insured assets |
| Applicant | Quote | 1:N | One applicant can request multiple quotes |
| Product | CoverageOption | 1:N | One product can provide multiple coverage options |
| Applicant | RiskFactor | N:M | Applicants can have multiple risk factors |
| Applicant | InsuredAsset | 1:N | Each asset references its applicant |
| Product | Quote | 1:N | One product can be referenced by multiple quotes |
| InsuredAsset | Quote | 1:N | An asset can be referenced by multiple quotes |
| Quote | Policy | 1:N at schema level | Policies reference their source quote |
| Policy | Endorsement | 1:N | A policy can have multiple endorsements |
| Policy | Renewal | 1:N | A policy can have multiple renewal records |
| Quote | UnderwritingDecision | 1:N | A quote can have multiple decisions |
| Policy | PolicyEvent | 1:N | A policy can have multiple lifecycle events |

The many-to-many Applicant–RiskFactor relationship uses the `applicant_risk_factors` bridge table.

## 4. Primary and Foreign Keys

Every main entity has a primary key.

Foreign-key references include:

- insured_assets.applicant_id → applicants.id
- coverage_options.product_id → products.id
- quotes.applicant_id → applicants.id
- quotes.product_id → products.id
- quotes.asset_id → insured_assets.id
- policies.quote_id → quotes.id
- policies.applicant_id → applicants.id
- endorsements.policy_id → policies.id
- renewals.policy_id → policies.id
- underwriting_decisions.quote_id → quotes.id
- policy_events.policy_id → policies.id
- applicant_risk_factors.applicant_id → applicants.id
- applicant_risk_factors.risk_factor_id → risk_factors.id

## 5. Identifier Conventions

| Entity | Example |
|---|---|
| Applicant | APP-2026-000001 |
| Quote | QTE-2026-000001 |
| Policy | POL-2026-000001 |
| Endorsement | END-POL-2026-000001-001 |
| Renewal | REN-POL-2026-000001-2027 |

Identifiers are designed to be deterministic and traceable.

## 6. Lifecycle and Business Validation

The system should enforce these business conditions:

1. Applicants must satisfy the selected product's eligibility rules.
2. Coverage must not exceed the product's maximum coverage.
3. Premiums must be calculated using documented rate factors.
4. High-risk submissions must be referred for underwriting review.
5. Policy issuance requires customer acceptance and payment.
6. Policy end dates must be after start dates.
7. Endorsements must preserve the previous and updated values.
8. Renewal offers must not be generated for cancelled policies.
9. Policy status changes should be recorded in policy_events.
10. Overlapping policy periods must be checked.

## 7. Implementation Notes and Limitations

The SQLAlchemy models define several fields as nullable because `nullable=False` is not specified.

Allowed status values, age boundaries, numeric ranges and some lifecycle rules are not enforced directly by the database models. They require application-level validation.

The current schema also does not define explicit effective-date fields for products, coverage options or risk factors.

The Quote–Policy relationship is represented using a foreign key, but the schema does not enforce a one-to-one constraint.

The Applicant–RiskFactor bridge table does not explicitly declare a composite primary key or unique constraint in the supplied model.

These distinctions are documented to make the actual implementation and its validation responsibilities clear.

## 8. Technology

- Python
- SQLAlchemy ORM
- SQLite
- Pandas
- NumPy
- CSV and JSON exports