from flask import Flask, request, jsonify
from ollama_service import analyze_alert
import json
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

STORAGE_FILE = os.path.join(
    BASE_DIR,
    "storage.json"
)


# ==========================
# Storage
# ==========================

def load_alerts():

    if not os.path.exists(STORAGE_FILE):
        return []

    try:
        with open(STORAGE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_alert(alert):

    alerts = load_alerts()

    alerts.insert(0, alert)

    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            alerts,
            f,
            indent=2
        )


# ==========================
# Normalization
# ==========================

def normalize_splunk_payload(data):

    result = data.get("result", {})

    account_name = result.get(
        "Account_Name",
        ""
    )

    if isinstance(account_name, list):
        account_name = ", ".join(account_name)

    return {

        "search_name": data.get(
            "search_name",
            "Splunk Alert"
        ),

        "event_code": result.get(
            "EventCode",
            "N/A"
        ),

        "src_ip": result.get(
            "Source_Network_Address",
            "N/A"
        ),

        "host": result.get(
            "host",
            "N/A"
        ),

        "user": account_name,

        "failure_reason": result.get(
            "Failure_Reason",
            "N/A"
        ),

        "logon_type": result.get(
            "Logon_Type",
            "N/A"
        ),

        "status": result.get(
            "Status",
            "N/A"
        ),

        "message": result.get(
            "Message",
            ""
        ),

        "raw": result
    }


# ==========================
# Splunk Endpoint
# ==========================

@app.route(
    "/splunk-alert",
    methods=["POST"]
)
def splunk_alert():

    try:

        data = request.get_json(
            force=True
        )

        normalized = normalize_splunk_payload(
            data
        )

        analysis = analyze_alert(
            normalized
        )

        record = {
            "alert": normalized,
            "analysis": analysis
        }

        save_alert(record)

        return jsonify({
            "status": "success",
            "search_name":
                normalized["search_name"]
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
@app.route("/debug")
def debug():

    return {
        "storage_file": STORAGE_FILE,
        "absolute_path": os.path.abspath(STORAGE_FILE),
        "exists": os.path.exists(STORAGE_FILE)
    }

# ==========================
# API For Streamlit
# ==========================

@app.route("/alerts")
def alerts():

    return jsonify(
        load_alerts()
    )


# ==========================
# Debug
# ==========================

@app.route("/health")
def health():

    return {
        "status": "ok"
    }


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )