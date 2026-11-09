def calculate_premium(coverage, product, applicant):
    """
    Calculate insurance premium using coverage amount,
    product base rate, and applicant risk multipliers.
    """

    multiplier = 1.0

    for risk in applicant.risk_factors:
        multiplier *= float(risk.multiplier)

    premium = round(
        float(coverage)
        * float(product.base_rate)
        * multiplier,
        2
    )

    return premium