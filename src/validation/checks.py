from pathlib import Path
import json
import pandas as pd

from src.database.db import SessionLocal
from src.database.models import (
    Applicant, InsuredAsset, Product, CoverageOption,
    RiskFactor, Quote, Policy, Endorsement, Renewal,
    UnderwritingDecision, PolicyEvent
)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
GROUND_TRUTH_FILE = OUTPUT_DIR / "ground_truth" / "ground_truth.csv"


def validate_database():
    db = SessionLocal()
    results = []

    try:
        if not GROUND_TRUTH_FILE.exists():
            raise FileNotFoundError(f"Missing file: {GROUND_TRUTH_FILE}")

        ground_truth = pd.read_csv(GROUND_TRUTH_FILE)

        expected_acceptance = set(
            ground_truth.loc[
                ground_truth["issue_type"] == "POLICY_WITHOUT_ACCEPTANCE",
                "entity_id"
            ].astype(str)
        )

        expected_premium = set(
            ground_truth.loc[
                ground_truth["issue_type"] == "PREMIUM_OUTSIDE_FORMULA",
                "entity_id"
            ].astype(str)
        )

        # Record counts
        checks = {
            "Applicants": db.query(Applicant).count(),
            "Insured Assets": db.query(InsuredAsset).count(),
            "Products": db.query(Product).count(),
            "Coverage Options": db.query(CoverageOption).count(),
            "Risk Factors": db.query(RiskFactor).count(),
            "Quotes": db.query(Quote).count(),
            "Policies": db.query(Policy).count(),
            "Endorsements": db.query(Endorsement).count(),
            "Renewals": db.query(Renewal).count(),
            "Underwriting Decisions": db.query(UnderwritingDecision).count(),
            "Policy Events": db.query(PolicyEvent).count()
        }

        for name, count in checks.items():
            results.append({
                "check": f"{name} record count",
                "status": "PASS" if count > 0 else "FAIL",
                "details": f"{count} records"
            })

        # Primary key uniqueness
        for model, name in [
            (Applicant, "Applicant"),
            (Quote, "Quote"),
            (Policy, "Policy")
        ]:
            ids = [row.id for row in db.query(model.id).all()]
            results.append({
                "check": f"{name} ID uniqueness",
                "status": "PASS" if len(ids) == len(set(ids)) else "FAIL",
                "details": f"{len(ids)} records checked"
            })

        # Quote foreign keys
        invalid_quotes = 0
        for quote in db.query(Quote).all():
            if (
                not db.query(Applicant).filter_by(id=quote.applicant_id).first()
                or not db.query(Product).filter_by(id=quote.product_id).first()
                or not db.query(InsuredAsset).filter_by(id=quote.asset_id).first()
            ):
                invalid_quotes += 1

        results.append({
            "check": "Quote foreign keys",
            "status": "PASS" if invalid_quotes == 0 else "FAIL",
            "details": f"{invalid_quotes} invalid quotes"
        })

        # Acceptance and payment
        actual_acceptance = {
            p.id for p in db.query(Policy).all()
            if p.accepted is not True or p.payment_received is not True
        }

        unexpected_acceptance = actual_acceptance - expected_acceptance
        missing_acceptance = expected_acceptance - actual_acceptance

        acceptance_pass = (
            not unexpected_acceptance and not missing_acceptance
        )

        results.append({
            "check": "Policy acceptance and payment",
            "status": "PASS" if acceptance_pass else "FAIL",
            "details": (
                f"Expected: {len(expected_acceptance)}, "
                f"unexpected: {len(unexpected_acceptance)}, "
                f"not detected: {len(missing_acceptance)}"
            )
        })

        # Premium consistency
        actual_premium = set()

        for policy in db.query(Policy).all():
            quote = db.query(Quote).filter_by(id=policy.quote_id).first()
            if quote and abs(policy.premium - quote.calculated_premium) > 0.01:
                actual_premium.add(policy.id)

        unexpected_premium = actual_premium - expected_premium
        missing_premium = expected_premium - actual_premium

        premium_pass = (
            not unexpected_premium and not missing_premium
        )

        results.append({
            "check": "Policy premium consistency",
            "status": "PASS" if premium_pass else "FAIL",
            "details": (
                f"Expected: {len(expected_premium)}, "
                f"unexpected: {len(unexpected_premium)}, "
                f"not detected: {len(missing_premium)}"
            )
        })

        # Policy date validity
        invalid_dates = db.query(Policy).filter(
            Policy.end_date <= Policy.start_date
        ).count()

        results.append({
            "check": "Policy date validity",
            "status": "PASS" if invalid_dates == 0 else "FAIL",
            "details": f"{invalid_dates} invalid policy periods"
        })

        # Ground truth count
        results.append({
            "check": "Ground truth records",
            "status": "PASS" if len(ground_truth) == 5 else "FAIL",
            "details": f"{len(ground_truth)} labelled anomalies"
        })

        # Save validation reports
        df = pd.DataFrame(results)
        df.to_csv(OUTPUT_DIR / "validation_report.csv", index=False)

        with open(OUTPUT_DIR / "validation_report.json", "w") as file:
            json.dump(results, file, indent=4)

        print("\nDATA VALIDATION COMPLETED")
        print(df.to_string(index=False))
        print("\nReport saved in outputs/")

    finally:
        db.close()


if __name__ == "__main__":
    validate_database()