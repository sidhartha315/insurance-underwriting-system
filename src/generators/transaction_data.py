import random
from datetime import date, datetime, timedelta, timezone

from src.database.db import SessionLocal

from src.database.models import (
    Applicant,
    InsuredAsset,
    Product,
    Quote,
    Policy,
    Renewal,
    Endorsement,
    UnderwritingDecision,
    PolicyEvent
)

SEED = 20261022

TOTAL_QUOTES = 4000
TOTAL_POLICIES = 2000
TOTAL_RENEWALS = 1200
TOTAL_ENDORSEMENTS = 200


def generate_transactions():
    random.seed(SEED)
    db = SessionLocal()

    try:
        if db.query(Quote).count() > 0:
            print("Transaction data already exists.")
            return

        applicants = db.query(Applicant).all()
        assets = db.query(InsuredAsset).all()
        products = db.query(Product).all()

        if not applicants or not assets or not products:
            raise ValueError("Master data is missing.")

        asset_map = {asset.applicant_id: asset for asset in assets}

        print("\nGenerating 4000 quotes...")

        quotes = []
        decisions = []
        candidates = []

        # STEP 1: GENERATE QUOTES
        for i in range(1, TOTAL_QUOTES + 1):
            applicant = random.choice(applicants)
            asset = asset_map.get(applicant.id)

            if asset is None:
                continue

            eligible_products = [
                product for product in products
                if product.min_age <= applicant.age <= product.max_age
            ]

            if not eligible_products:
                product = random.choice(products)
                decision = "DECLINED"
                reason = "Product eligibility criteria not met"
            else:
                product = random.choice(eligible_products)
                decision = None
                reason = ""

            coverage = round(
                random.uniform(100000, float(product.max_coverage)), 2
            )

            risk_count = len(applicant.risk_factors)
            multiplier = 1.0

            for risk in applicant.risk_factors:
                multiplier *= float(risk.multiplier)

            premium = round(
                coverage * float(product.base_rate) * multiplier, 2
            )

            risk_score = round(
                risk_count * 30 + (multiplier - 1) * 20, 2
            )

            if decision is None:
                if risk_count == 0:
                    decision = "REFERRED"
                    reason = "Missing risk information"
                else:
                    candidates.append({
                        "quote_number": i,
                        "applicant": applicant,
                        "product": product,
                        "asset": asset,
                        "coverage": coverage,
                        "premium": premium,
                        "risk_score": risk_score,
                        "multiplier": multiplier
                    })

            quote = Quote(
                id=f"QTE-2026-{i:06d}",
                applicant_id=applicant.id,
                product_id=product.id,
                asset_id=asset.id,
                coverage_amount=coverage,
                calculated_premium=premium,
                status=decision if decision else "PENDING",
                created_at=datetime.now(timezone.utc).replace(tzinfo=None)
            )

            quotes.append(quote)

        # STEP 2: SELECT 2000 LOWEST-RISK ELIGIBLE QUOTES
        if len(candidates) < TOTAL_POLICIES:
            raise ValueError(
                f"Only {len(candidates)} eligible quotes available. "
                f"{TOTAL_POLICIES} required."
            )

        candidates.sort(
            key=lambda x: (
                x["risk_score"],
                x["multiplier"],
                x["quote_number"]
            )
        )

        approved_ids = {
            item["quote_number"]
            for item in candidates[:TOTAL_POLICIES]
        }

        approved_quotes = []
        candidate_map = {
            item["quote_number"]: item for item in candidates
        }

        # STEP 3: CREATE UNDERWRITING DECISIONS
        for quote in quotes:
            quote_number = int(quote.id.split("-")[-1])

            if quote_number in approved_ids:
                quote.status = "APPROVED"
                decision = "APPROVED"
                reason = (
                    "Eligibility passed and risk score "
                    "within automated approval threshold"
                )
                approved_quotes.append(quote)

            elif quote.status == "PENDING":
                quote.status = "REFERRED"
                decision = "REFERRED"
                reason = (
                    "Risk review required; automated "
                    "approval threshold exceeded"
                )

            else:
                decision = quote.status
                reason = (
                    "Missing risk information"
                    if decision == "REFERRED"
                    else "Product eligibility criteria not met"
                )

            data = candidate_map.get(quote_number)
            risk_score = data["risk_score"] if data else 0

            decisions.append(
                UnderwritingDecision(
                    id=f"UWD-2026-{quote_number:06d}",
                    quote_id=quote.id,
                    decision=decision,
                    risk_score=risk_score,
                    reason=reason,
                    reviewer="System"
                )
            )

        db.add_all(quotes)
        db.add_all(decisions)
        db.flush()

        print("Quotes generated:", len(quotes))
        print("Approved:", len(approved_quotes))
        print("Referred:", sum(q.status == "REFERRED" for q in quotes))
        print("Declined:", sum(q.status == "DECLINED" for q in quotes))

        # STEP 4: GENERATE POLICIES WITHOUT ACCIDENTAL OVERLAPS
        print("\nGenerating 2000 policies...")

        policies = []
        events = []

        next_start_by_key = {}

        for i, quote in enumerate(approved_quotes, 1):
            key = (
                quote.applicant_id,
                quote.asset_id,
                quote.product_id
            )

            if key not in next_start_by_key:
                next_start_by_key[key] = (
                    date(2026, 1, 1)
                    + timedelta(days=random.randint(0, 30))
                )

            start = next_start_by_key[key]
            end = start + timedelta(days=365)

            next_start_by_key[key] = end + timedelta(days=1)

            policy = Policy(
                id=f"POL-2026-{i:06d}",
                quote_id=quote.id,
                applicant_id=quote.applicant_id,
                start_date=start,
                end_date=end,
                premium=quote.calculated_premium,
                status="ACTIVE",
                accepted=True,
                payment_received=True
            )

            policies.append(policy)

            events.append(
                PolicyEvent(
                    policy_id=policy.id,
                    event_type="POLICY_ISSUED",
                    previous_status="QUOTED",
                    new_status="ACTIVE"
                )
            )

        db.add_all(policies)
        db.add_all(events)
        db.flush()

        print("Policies generated:", len(policies))

        # STEP 5: GENERATE RENEWALS
        print("\nGenerating 1200 renewals...")

        renewals = []

        for policy in policies[:TOTAL_RENEWALS]:
            renewals.append(
                Renewal(
                    id=f"REN-{policy.id}-2027",
                    policy_id=policy.id,
                    renewal_date=policy.end_date,
                    offered_premium=round(policy.premium * 1.05, 2),
                    status=random.choice([
                        "OFFERED", "ACCEPTED", "DECLINED"
                    ])
                )
            )

        db.add_all(renewals)

        # STEP 6: GENERATE ENDORSEMENTS
        print("\nGenerating endorsements...")

        endorsements = []

        for policy in policies[:TOTAL_ENDORSEMENTS]:
            endorsements.append(
                Endorsement(
                    id=f"END-{policy.id}-001",
                    policy_id=policy.id,
                    change_type="ASSET_VALUE_UPDATE",
                    old_value=100000,
                    new_value=110000
                )
            )

        db.add_all(endorsements)

        # STEP 7: COMMIT
        db.commit()

        print("\n====================================")
        print("TRANSACTION GENERATION COMPLETED")
        print("====================================")
        print("Applicants:", len(applicants))
        print("Quotes:", len(quotes))
        print("Policies:", len(policies))
        print("Renewals:", len(renewals))
        print("Endorsements:", len(endorsements))
        print("Underwriting Decisions:", len(decisions))
        print("\nDatabase transaction completed successfully!")

    except Exception as e:
        db.rollback()
        print("\nERROR:", e)
        raise

    finally:
        db.close()


if __name__ == "__main__":
    generate_transactions()