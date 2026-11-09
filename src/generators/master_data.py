import random
from faker import Faker

from src.database.db import SessionLocal
from src.database.models import (
    Applicant,
    InsuredAsset,
    Product,
    CoverageOption,
    RiskFactor
)

SEED = 20261022

random.seed(SEED)
fake = Faker()
Faker.seed(SEED)


def generate_master_data():

    db = SessionLocal()

    try:
        # Prevent duplicate master data
        if db.query(Applicant).count() > 0:
            print("Master data already exists.")
            return

        print("Generating master data...")

        # 1. Products
        products = [
            Product(
                id="PRD-001",
                name="Motor Insurance",
                product_line="Motor",
                base_rate=0.05,
                min_age=18,
                max_age=80,
                max_coverage=2000000
            ),
            Product(
                id="PRD-002",
                name="Property Insurance",
                product_line="Property",
                base_rate=0.03,
                min_age=21,
                max_age=80,
                max_coverage=10000000
            ),
            Product(
                id="PRD-003",
                name="Life Insurance",
                product_line="Life",
                base_rate=0.02,
                min_age=18,
                max_age=65,
                max_coverage=5000000
            )
        ]

        db.add_all(products)

        # 2. Coverage Options
        coverages = [
            CoverageOption(
                id="COV-001",
                product_id="PRD-001",
                name="Basic Motor Cover",
                coverage_limit=500000,
                additional_rate=0.01
            ),
            CoverageOption(
                id="COV-002",
                product_id="PRD-001",
                name="Premium Motor Cover",
                coverage_limit=2000000,
                additional_rate=0.02
            ),
            CoverageOption(
                id="COV-003",
                product_id="PRD-002",
                name="Basic Property Cover",
                coverage_limit=5000000,
                additional_rate=0.01
            ),
            CoverageOption(
                id="COV-004",
                product_id="PRD-002",
                name="Premium Property Cover",
                coverage_limit=10000000,
                additional_rate=0.02
            ),
            CoverageOption(
                id="COV-005",
                product_id="PRD-003",
                name="Basic Life Cover",
                coverage_limit=2000000,
                additional_rate=0.01
            ),
            CoverageOption(
                id="COV-006",
                product_id="PRD-003",
                name="Premium Life Cover",
                coverage_limit=5000000,
                additional_rate=0.02
            )
        ]

        db.add_all(coverages)

        # 3. Risk Factors
        risk_factors = [
            RiskFactor(
                id="RSK-001",
                name="High Risk Location",
                factor_type="Location",
                multiplier=1.5,
                description="Applicant lives in a high-risk area"
            ),
            RiskFactor(
                id="RSK-002",
                name="Low Risk Location",
                factor_type="Location",
                multiplier=0.9,
                description="Applicant lives in a low-risk area"
            ),
            RiskFactor(
                id="RSK-003",
                name="High Asset Value",
                factor_type="Asset",
                multiplier=1.3,
                description="Insured asset has high value"
            ),
            RiskFactor(
                id="RSK-004",
                name="Previous Claims",
                factor_type="Claims",
                multiplier=1.4,
                description="Applicant has previous claims"
            ),
            RiskFactor(
                id="RSK-005",
                name="Low Risk Profile",
                factor_type="Profile",
                multiplier=0.95,
                description="Applicant has a low-risk profile"
            )
        ]

        db.add_all(risk_factors)
        db.flush()

        # 4. Applicants and Assets
        risk_records = db.query(RiskFactor).all()

        applicants = []
        assets = []

        for i in range(1, 3001):

            applicant_id = f"APP-2026-{i:06d}"
            asset_id = f"AST-2026-{i:06d}"

            applicant = Applicant(
                id=applicant_id,
                name=fake.name(),
                age=random.randint(18, 75),
                income=round(random.uniform(200000, 2500000), 2),
                location=random.choice([
                    "Hyderabad",
                    "Mumbai",
                    "Delhi",
                    "Bangalore",
                    "Chennai"
                ])
            )

            # Assign risk factors
            selected_risks = random.sample(
                risk_records,
                k=random.randint(0, 2)
            )

            applicant.risk_factors = selected_risks
            applicants.append(applicant)

            asset = InsuredAsset(
                id=asset_id,
                applicant_id=applicant_id,
                asset_type=random.choice([
                    "Vehicle",
                    "Property",
                    "Equipment"
                ]),
                asset_value=round(
                    random.uniform(100000, 10000000), 2
                ),
                location=applicant.location
            )

            assets.append(asset)

            if i % 500 == 0:
                db.add_all(applicants)
                db.add_all(assets)
                db.flush()

                applicants.clear()
                assets.clear()

                print(f"Generated {i} applicants and assets")

        db.add_all(applicants)
        db.add_all(assets)

        db.commit()

        print("\nMASTER DATA GENERATION COMPLETED")
        print("Applicants: 3000")
        print("Insured Assets: 3000")
        print("Products: 3")
        print("Coverage Options: 6")
        print("Risk Factors: 5")

    except Exception as e:
        db.rollback()
        print("Error:", e)

    finally:
        db.close()


if __name__ == "__main__":
    generate_master_data()