def format_currency(value):
    """Convert a number into currency format."""
    return f"${value:,.2f}"


def detect_intent(question):
    """
    Detect user intent using simple keyword matching.
    No AI or LLM is used.
    """

    question = question.lower().strip()

    # Declining products
    if (
        "product" in question
        and (
            "declining" in question
            or "decline" in question
            or "decreasing" in question
            or "decrease" in question
            or "falling" in question
        )
    ):
        return "declining_products"

    # Highest-selling category
    if (
        "category" in question
        and (
            "highest" in question
            or "top" in question
            or "most" in question
            or "best" in question
        )
        and (
            "sales" in question
            or "selling" in question
        )
    ):
        return "highest_category_sales"

    # Monthly sales trend
    if (
        (
            "monthly" in question
            and "sales" in question
        )
        or (
            "sales" in question
            and "trend" in question
        )
        or (
            "sales" in question
            and "over time" in question
        )
    ):
        return "monthly_sales_trend"

    # Top customers
    if (
        "customer" in question
        and (
            "top" in question
            or "highest" in question
            or "best" in question
            or "most" in question
        )
    ):
        return "top_customers"

    # Highest-revenue product
    if (
        "product" in question
        and (
            "highest" in question
            or "top" in question
            or "most" in question
            or "best" in question
        )
        and (
            "revenue" in question
            or "sales" in question
            or "selling" in question
        )
    ):
        return "highest_product_revenue"

    return None