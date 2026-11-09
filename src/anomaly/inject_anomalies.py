import json
from pathlib import Path

import pandas as pd

from src.database.db import SessionLocal
from src.database.models import (
    Policy,
    Quote,
    Endorsement,
    Renewal,
    Product
)

OUTPUT_DIR = Path("outputs/ground_truth")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def inject_anomalies():
    db = SessionLocal()
    ground_truth = []

    try:
        policies = db.query(Policy).order_by(Policy.id).all()
        endorsements = db.query(Endorsement).order_by(Endorsement.id).all()
        renewals = db.query(Renewal).order_by(Renewal.id).all()

        if len(policies) < 4 or not endorsements or not renewals:
            raise ValueError("Required transaction records are missing.")

        # 1. Policy issued without customer acceptance
        policy = policies[0]
        policy.accepted = False

        ground_truth.append({
            "anomaly_id": "ANM-001",
            "entity_type": "Policy",
            "entity_id": policy.id,
            "issue_type": "POLICY_WITHOUT_ACCEPTANCE",
            "description": "Policy issued without customer acceptance."
        })

        # 2. Policy premium outside calculated formula
        policy = policies[1]
        quote = db.query(Quote).filter_by(id=policy.quote_id).first()

        if not quote:
            raise ValueError("Quote for premium anomaly not found.")

        policy.premium = round(float(quote.calculated_premium) + 5000, 2)

        ground_truth.append({
            "anomaly_id": "ANM-002",
            "entity_type": "Policy",
            "entity_id": policy.id,
            "issue_type": "PREMIUM_OUTSIDE_FORMULA",
            "description": "Policy premium differs from calculated quote premium."
        })

        # 3. Endorsement exceeds product coverage limit
        endorsement = endorsements[0]
        policy = db.query(Policy).filter_by(
            id=endorsement.policy_id
        ).first()

        if not policy:
            raise ValueError("Policy for endorsement anomaly not found.")

        quote = db.query(Quote).filter_by(id=policy.quote_id).first()

        if not quote:
            raise ValueError("Quote for endorsement anomaly not found.")

        product = db.query(Product).filter_by(id=quote.product_id).first()

        if not product:
            raise ValueError("Product for endorsement anomaly not found.")

        endorsement.new_value = float(product.max_coverage) + 100000

        ground_truth.append({
            "anomaly_id": "ANM-003",
            "entity_type": "Endorsement",
            "entity_id": endorsement.id,
            "issue_type": "ENDORSEMENT_LIMIT_EXCEEDED",
            "description": "Endorsement value exceeds product maximum coverage."
        })

        # 4. Renewal for cancelled policy
        renewal = renewals[0]
        policy = db.query(Policy).filter_by(
            id=renewal.policy_id
        ).first()

        if not policy:
            raise ValueError("Policy for renewal anomaly not found.")

        policy.status = "CANCELLED"

        ground_truth.append({
            "anomaly_id": "ANM-004",
            "entity_type": "Renewal",
            "entity_id": renewal.id,
            "issue_type": "RENEWAL_FOR_CANCELLED_POLICY",
            "description": "Renewal exists for a cancelled policy."
        })

        # 5. Deliberately overlapping policy periods
        policy_one = policies[2]
        policy_two = policies[3]

        quote_one = db.query(Quote).filter_by(
            id=policy_one.quote_id
        ).first()

        quote_two = db.query(Quote).filter_by(
            id=policy_two.quote_id
        ).first()

        if not quote_one or not quote_two:
            raise ValueError("Quotes for overlap anomaly not found.")

        # Align the second quote with the first policy's
        # applicant, insured asset and product.
        quote_two.applicant_id = quote_one.applicant_id
        quote_two.asset_id = quote_one.asset_id
        quote_two.product_id = quote_one.product_id

        # Keep the policy and quote relationships consistent.
        policy_two.applicant_id = policy_one.applicant_id

        # Create an intentional overlapping period.
        policy_two.start_date = policy_one.start_date
        policy_two.end_date = policy_one.end_date

        ground_truth.append({
            "anomaly_id": "ANM-005",
            "entity_type": "Policy",
            "entity_id": policy_two.id,
            "issue_type": "OVERLAPPING_POLICY_PERIOD",
            "description": (
                "Two policies for the same applicant, insured asset "
                "and product have overlapping periods."
            )
        })

        db.commit()

        # Export separate ground-truth files.
        df = pd.DataFrame(ground_truth)

        df.to_csv(
            OUTPUT_DIR / "ground_truth.csv",
            index=False
        )

        with open(
            OUTPUT_DIR / "ground_truth.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(ground_truth, file, indent=4)

        print("\nANOMALY INJECTION COMPLETED")
        print("Deliberate anomalies created:", len(ground_truth))
        print(df.to_string(index=False))
        print("\nFiles saved in outputs/ground_truth/")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    inject_anomalies()