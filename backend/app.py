from pathlib import Path

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

from analytics import ANALYTICS_HANDLERS
from utility import detect_intent


app = Flask(__name__)
CORS(app)

CSV_PATH = Path(__file__).resolve().parent / "superstore.csv"

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "success": True,
        "message": "InsightIQ backend is running."
    }), 200

def load_data():
    """Load and prepare the Superstore dataset."""

    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"superstore.csv was not found at {CSV_PATH}"
        )

    dataframe = pd.read_csv(
        CSV_PATH,
        encoding="latin-1"
    )

    dataframe.columns = dataframe.columns.str.strip()

    required_columns = [
        "Category",
        "Sales",
        "Product Name",
        "Customer Name",
        "Order Date"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing CSV columns: "
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
                    "This question is not supported yet." 
                    "Try asking suggested question."
                )
            }), 400

        handler = ANALYTICS_HANDLERS.get(intent)

        if handler is None:
            return jsonify({
                "success": False,
                "error": (
                    f"No analytics function was found "
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

    except FileNotFoundError:
        return jsonify({
            "success": False,
            "error": (
                "superstore.csv was not found "
                "inside the backend folder."
            )
        }), 500

    except ValueError as error:
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
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )