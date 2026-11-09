from sqlalchemy import (
    Column, String, Integer, Float, Boolean,
    Date, DateTime, ForeignKey, Table, Text
)
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.db import Base


# Many-to-many relationship
applicant_risk_factors = Table(
    "applicant_risk_factors",
    Base.metadata,
    Column("applicant_id", String, ForeignKey("applicants.id")),
    Column("risk_factor_id", String, ForeignKey("risk_factors.id"))
)


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    income = Column(Float)
    location = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    assets = relationship("InsuredAsset", back_populates="applicant")
    quotes = relationship("Quote", back_populates="applicant")
    risk_factors = relationship(
        "RiskFactor",
        secondary=applicant_risk_factors
    )


class InsuredAsset(Base):
    __tablename__ = "insured_assets"

    id = Column(String, primary_key=True)
    applicant_id = Column(String, ForeignKey("applicants.id"))
    asset_type = Column(String)
    asset_value = Column(Float)
    location = Column(String)

    applicant = relationship("Applicant", back_populates="assets")


class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    product_line = Column(String)
    base_rate = Column(Float)
    min_age = Column(Integer)
    max_age = Column(Integer)
    max_coverage = Column(Float)
    active = Column(Boolean, default=True)

    coverage_options = relationship(
        "CoverageOption", back_populates="product"
    )


class CoverageOption(Base):
    __tablename__ = "coverage_options"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    name = Column(String)
    coverage_limit = Column(Float)
    additional_rate = Column(Float)

    product = relationship("Product", back_populates="coverage_options")


class RiskFactor(Base):
    __tablename__ = "risk_factors"

    id = Column(String, primary_key=True)
    name = Column(String)
    factor_type = Column(String)
    multiplier = Column(Float)
    description = Column(Text)


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(String, primary_key=True)
    applicant_id = Column(String, ForeignKey("applicants.id"))
    product_id = Column(String, ForeignKey("products.id"))
    asset_id = Column(String, ForeignKey("insured_assets.id"))
    coverage_amount = Column(Float)
    calculated_premium = Column(Float)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    applicant = relationship("Applicant", back_populates="quotes")


class Policy(Base):
    __tablename__ = "policies"

    id = Column(String, primary_key=True)
    quote_id = Column(String, ForeignKey("quotes.id"))
    applicant_id = Column(String, ForeignKey("applicants.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    premium = Column(Float)
    status = Column(String)
    accepted = Column(Boolean, default=False)
    payment_received = Column(Boolean, default=False)


class Endorsement(Base):
    __tablename__ = "endorsements"

    id = Column(String, primary_key=True)
    policy_id = Column(String, ForeignKey("policies.id"))
    change_type = Column(String)
    old_value = Column(Float)
    new_value = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)


class Renewal(Base):
    __tablename__ = "renewals"

    id = Column(String, primary_key=True)
    policy_id = Column(String, ForeignKey("policies.id"))
    renewal_date = Column(Date)
    offered_premium = Column(Float)
    status = Column(String)


class UnderwritingDecision(Base):
    __tablename__ = "underwriting_decisions"

    id = Column(String, primary_key=True)
    quote_id = Column(String, ForeignKey("quotes.id"))
    decision = Column(String)
    risk_score = Column(Float)
    reason = Column(Text)
    reviewer = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class PolicyEvent(Base):
    __tablename__ = "policy_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    policy_id = Column(String, ForeignKey("policies.id"))
    event_type = Column(String)
    previous_status = Column(String)
    new_status = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)