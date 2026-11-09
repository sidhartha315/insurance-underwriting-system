import pandas as pd
from pathlib import Path

from src.database.db import SessionLocal
from src.database.models import (
    Policy,
    Quote,
    Renewal,
    Endorsement,
    Product
)

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def detect_anomalies():
    db = SessionLocal()
    anomalies = []

    try:
        policies = db.query(Policy).all()
        quotes = db.query(Quote).all()
        renewals = db.query(Renewal).all()
        endorsements = db.query(Endorsement).all()
        products = db.query(Product).all()

        quote_map = {q.id: q for q in quotes}
        policy_map = {p.id: p for p in policies}
        product_map = {p.id: p for p in products}

        # 1. Policy issued without acceptance or payment
        for policy in policies:
            if policy.accepted is not True or policy.payment_received is not True:
                anomalies.append({
                    "entity_id": policy.id,
                    "issue_type": "POLICY_WITHOUT_ACCEPTANCE",
                    "description": "Policy issued without acceptance or payment."
                })

        # 2. Premium differs from calculated quote premium
        for policy in policies:
            quote = quote_map.get(policy.quote_id)

            if quote and abs(
                float(policy.premium) - float(quote.calculated_premium)
            ) > 0.01:
                anomalies.append({
                    "entity_id": policy.id,
                    "issue_type": "PREMIUM_MISMATCH",
                    "description": "Policy premium differs from quote premium."
                })

        # 3. Endorsement exceeds product coverage limit
        for endorsement in endorsements:
            policy = policy_map.get(endorsement.policy_id)

            if not policy:
                continue

            quote = quote_map.get(policy.quote_id)

            if not quote:
                continue

            product = product_map.get(quote.product_id)

            if (
                product
                and endorsement.new_value is not None
                and float(endorsement.new_value) > float(product.max_coverage)
            ):
                anomalies.append({
                    "entity_id": endorsement.id,
                    "issue_type": "ENDORSEMENT_LIMIT_EXCEEDED",
                    "description": "Endorsement exceeds product maximum coverage."
                })

        # 4. Renewal generated for a cancelled policy
        for renewal in renewals:
            policy = policy_map.get(renewal.policy_id)

            if policy and policy.status == "CANCELLED":
                anomalies.append({
                    "entity_id": renewal.id,
                    "issue_type": "RENEWAL_FOR_CANCELLED_POLICY",
                    "description": "Renewal exists for a cancelled policy."
                })

        # 5. Overlapping policies for the same applicant,
        # insured asset and product.
        grouped_policies = {}

        for policy in policies:
            quote = quote_map.get(policy.quote_id)

            if not quote:
                continue

            key = (
                policy.applicant_id,
                quote.asset_id,
                quote.product_id
            )

            grouped_policies.setdefault(key, []).append(policy)

        for records in grouped_policies.values():
            records.sort(key=lambda p: (p.start_date, p.end_date))

            latest_policy = None

            for current in records:
                if latest_policy is not None:
                    # Inclusive policy dates: a new policy must start
                    # after the previous policy's end date.
                    if current.start_date <= latest_policy.end_date:
                        anomalies.append({
                            "entity_id": current.id,
                            "issue_type": "OVERLAPPING_POLICY_PERIOD",
                            "description": (
                                "Overlapping policies for the same "
                                "applicant, insured asset and product."
                            )
                        })

                        if current.end_date > latest_policy.end_date:
                            latest_policy = current
                    else:
                        latest_policy = current
                else:
                    latest_policy = current

        # Export detected anomalies
        columns = [
            "entity_id",
            "issue_type",
            "description"
        ]

        df = pd.DataFrame(anomalies, columns=columns)

        df.to_csv(
            OUTPUT_DIR / "detected_anomalies.csv",
            index=False
        )

        df.to_json(
            OUTPUT_DIR / "detected_anomalies.json",
            orient="records",
            indent=4
        )

        print("\nANOMALY DETECTION COMPLETED")
        print("Detected anomalies:", len(df))

        if not df.empty:
            print("\nAnomaly summary:")
            print(df["issue_type"].value_counts())

        print("\nReports saved in outputs/")

    finally:
        db.close()


if __name__ == "__main__":
    detect_anomalies()