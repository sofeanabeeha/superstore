import pandas as pd

from utility import format_currency

# for suggested questions

# Q1
def highest_category_sales(dataframe):

    category_sales = (
        dataframe
        .groupby("Category")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )

    results = [
        {
            "rank": rank,
            "category": str(category),
            "sales": round(float(sales), 2)
        }
        for rank, (category, sales) in enumerate(
            category_sales.items(),
            start=1
        )
    ]

    if not results:
        return {
            "success": False,
            "error": "No category sales data was found."
        }

    top_category = results[0]
    second_category = results[1]
    third_category = results[2]

    return {
        "success": True,
        "title": (
            f"{top_category['category']} "
            f"has the highest sales"
        ),
        "answer": (
            f"{top_category['category']} recorded "
            f"the highest total sales, followed by "
            f"{second_category['category']} and "
            f"{third_category['category']}."
        ),
        "data": results
    }

# Q2
def monthly_sales_trend(dataframe):
    working_data = dataframe.dropna(
        subset=["Order Date", "Sales"]
    ).copy()

    working_data["Month"] = (
        working_data["Order Date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_sales = (
        working_data
        .groupby("Month", as_index=False)["Sales"]
        .sum()
        .sort_values("Month")
    )

    results = [
        {
            "month": row["Month"].strftime("%Y-%m"),
            "sales": round(float(row["Sales"]), 2)
        }
        for _, row in monthly_sales.iterrows()
    ]

    if not results:
        return {
            "success": False,
            "error": "No monthly sales data was found."
        }

    highest_month = max(
        results,
        key=lambda item: item["sales"]
    )

    lowest_month = min(
        results,
        key=lambda item: item["sales"]
    )

    first_month_sales = results[0]["sales"]
    latest_month_sales = results[-1]["sales"]

    trend = (
        "an upward trend"
        if latest_month_sales > first_month_sales
        else "a downward trend"
        if latest_month_sales < first_month_sales
        else "a stable trend"
    )

    start_month = results[0]["month"]
    end_month = results[-1]["month"]

    return {
        "success": True,
        "title": "Monthly sales trend",
        "answer": (
            f"Monthly sales show {trend} from "
            f"{start_month} to {end_month}. "
            f"The highest sales were recorded in "
            f"{highest_month['month']} at "
            f"{format_currency(highest_month['sales'])}, while "
            f"{lowest_month['month']} recorded the lowest sales "
            f"at {format_currency(lowest_month['sales'])}."
        ),
        "chartType": "line",
        "xKey": "month",
        "yKey": "sales",
        "datasetLabel": "Monthly Sales",
        "data": results
    }
# Q3
def top_customers(dataframe):

    customer_sales = (
        dataframe
        .groupby(["Customer Name", "Segment"])["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    results = [
        {
            "rank": rank,
            "customer": str(customer),
            "segment": str(segment),
            "sales": round(float(sales), 2)
        }
        for rank, ((customer, segment), sales) in enumerate(
            customer_sales.items(),
            start=1
        )
    ]

    if not results:
        return {
            "success": False,
            "error": "No customer data was found."
        }

    top_customer = results[0]

    return {
        "success": True,
        "title": "Top 5 customers by sales",
        "answer": (
            f"{top_customer['customer']} recorded the highest "
            f"total sales among all customers, with "
            f"{format_currency(top_customer['sales'])}."
        ),
        "data": results
    }


# Q4
def highest_product_revenue(dataframe):

    product_sales = (
        dataframe
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    results = [
        {
            "rank": rank,
            "product": str(product),
            "sales": round(float(sales), 2)
        }
        for rank, (product, sales) in enumerate(
            product_sales.items(),
            start=1
        )
    ]

    if not results:
        return {
            "success": False,
            "error": "No product sales data was found."
        }

    top_product = results[0]

    return {
        "success": True,
        "title": "Top 5 products by revenue",
        "answer": (
            f"{top_product['product']} generated the highest "
            f"revenue among all products, with "
            f"{format_currency(top_product['sales'])}."
        ),
        "data": results
    }

# Q5
def declining_products(dataframe):

    working_data = dataframe.dropna(
        subset=["Order Date", "Product Name", "Sales"]
    ).copy()

    working_data["Year"] = (
        working_data["Order Date"].dt.year
    )

    product_year_sales = (
        working_data
        .groupby(["Product Name", "Year"])["Sales"]
        .sum()
        .unstack(fill_value=0)
    )

    years = sorted(
        product_year_sales.columns.tolist()
    )

    if len(years) < 2:
        return {
            "success": False,
            "error": (
                "At least two years of sales data "
                "are required."
            )
        }

    previous_year = years[-2]
    latest_year = years[-1]

    # Keep only products that recorded sales in both years
    comparable_products = product_year_sales[
        (product_year_sales[previous_year] > 0) &
        (product_year_sales[latest_year] > 0)
    ].copy()

    comparable_products["change"] = (
        comparable_products[latest_year]
        - comparable_products[previous_year]
    )

    comparable_products["percentageChange"] = (
        (
            comparable_products["change"]
            / comparable_products[previous_year]
        ) * 100
    )

    declining = (
        comparable_products[
            comparable_products["change"] < 0
        ]
        .sort_values("change")
        .head(5)
    )

    results = [
        {
            "product": str(product),

            "previousSales": round(
                float(row[previous_year]),
                2
            ),

            "latestSales": round(
                float(row[latest_year]),
                2
            ),

            "change": round(
                float(row["change"]),
                2
            ),

            "percentageChange": round(
                float(row["percentageChange"]),
                1
            )
        }
        for product, row in declining.iterrows()
    ]

    if not results:
        return {
            "success": True,
            "title": "No Declining Products",
            "answer": (
                f"No products with sales in both "
                f"{previous_year} and {latest_year} "
                f"recorded a decline."
            ),
            "data": []
        }

    steepest_decline = results[0]

    return {
        "success": True,
        "title": "Top 5 products with declining sales",

        "answer": (
            f"Action required: "
            f"{steepest_decline['product']} experienced "
            f"the steepest decline, with sales falling from "
            f"{format_currency(steepest_decline['previousSales'])} "
            f"in {previous_year} to "
            f"{format_currency(steepest_decline['latestSales'])} "
            f"in {latest_year}. This represents a decline of "
            f"{abs(steepest_decline['percentageChange']):.1f}%."
        ),

        "chartType": "bar",
        "orientation": "horizontal",
        "xKey": "product",

        "datasetLabels": [
            str(previous_year),
            str(latest_year)
        ],

        "previousYear": previous_year,
        "latestYear": latest_year,
        "data": results
    }

ANALYTICS_HANDLERS = {
    "highest_category_sales": highest_category_sales,
    "monthly_sales_trend": monthly_sales_trend,
    "top_customers": top_customers,
    "highest_product_revenue": highest_product_revenue,
    "declining_products": declining_products, 
}