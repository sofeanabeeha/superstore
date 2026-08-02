import os

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from analytics import ANALYTICS_HANDLERS
from utility import detect_intent


app = Flask(__name__)
CORS(app)


# Read the PostgreSQL connection URL from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL environment variable is not set."
    )

# Render gives a URL beginning with postgresql://.
# This changes it so SQLAlchemy uses Psycopg 3.
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )


# Create one reusable database engine.
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "InsightIQ backend is running."
    }), 200


def load_data():
    """Load and prepare Superstore data from PostgreSQL."""

    query = text("""
        SELECT *
        FROM superstore_orders
    """)

    with engine.connect() as connection:
        dataframe = pd.read_sql(
            query,
            connection
        )

    # Convert PostgreSQL column names back to the names
    # expected by analytics.py.
    column_mapping = {
        "category": "Category",
        "sales": "Sales",
        "product_name": "Product Name",
        "customer_name": "Customer Name",
        "order_date": "Order Date",
        "segment": "Segment"
    }

    dataframe = dataframe.rename(
        columns=column_mapping
    )

    required_columns = [
        "Category",
        "Sales",
        "Product Name",
        "Customer Name",
        "Order Date",
        "Segment"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing database columns: "
            + ", ".join(missing_columns)
        )

    dataframe["Sales"] = pd.to_numeric(
        dataframe["Sales"],
        errors="coerce"
    )

    dataframe["Order Date"] = pd.to_datetime(
        dataframe["Order Date"],
        errors="coerce"
    )

    dataframe = dataframe.dropna(
        subset=["Sales"]
    )

    return dataframe


@app.route("/api/ask", methods=["POST"])
def ask_question():
    try:
        body = request.get_json(silent=True) or {}

        question = str(
            body.get("question", "")
        ).strip()

        if not question:
            return jsonify({
                "success": False,
                "error": "No question was provided."
            }), 400

        intent = detect_intent(question)

        if intent is None:
            return jsonify({
                "success": False,
                "error": (
                    "This question is not supported yet. "
                    "Try asking one of the suggested questions."
                )
            }), 400

        handler = ANALYTICS_HANDLERS.get(intent)

        if handler is None:
            return jsonify({
                "success": False,
                "error": (
                    "No analytics function was found "
                    f"for: {intent}."
                )
            }), 400

        dataframe = load_data()
        result = handler(dataframe)

        result["question"] = question

        status_code = (
            200
            if result.get("success")
            else 400
        )

        return jsonify(result), status_code

    except SQLAlchemyError as error:
        print("Database error:", error)

        return jsonify({
            "success": False,
            "error": (
                "InsightIQ could not retrieve data "
                "from the database."
            )
        }), 500

    except ValueError as error:
        print("Data error:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

    except Exception as error:
        print("Backend error:", error)

        return jsonify({
            "success": False,
            "error": (
                "The backend could not process "
                "the request."
            )
        }), 500


if __name__ == "__main__":
    app.run(debug=True)