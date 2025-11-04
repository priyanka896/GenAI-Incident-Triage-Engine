from flask import Flask, jsonify
from google.cloud import bigquery
from flask_cors import CORS   # ✅ NEW IMPORT
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Enables CORS for all routes

# Initialize BigQuery client using project from environment variable
client = bigquery.Client(project=os.environ.get("GOOGLE_CLOUD_PROJECT"))

@app.route("/triage")
def triage():
    # Query top 20 urgent incidents
    query = f"""
    SELECT report_id, dept, description, predicted_probability
    FROM `{client.project}.gov_raw.triage`
    WHERE predicted_is_urgent = 1
    ORDER BY predicted_probability DESC
    LIMIT 20
    """

    try:
        rows = client.query(query).result()
    except Exception as e:
        return jsonify({"error": f"BigQuery query failed: {e}"}), 500

    triaged = []
    dept_counts = {}

    for r in rows:
        dept = r.dept
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
        triaged.append({
            "report_id": r.report_id,
            "dept": dept,
            "description": r.description,
            "score": float(r.predicted_probability)
        })

    summary = {
        "total_reports": len(triaged),
        "departments": dept_counts,
        "high_priority": sum(1 for r in triaged if r["score"] > 0.45)
    }

    return jsonify({
        "summary": summary,
        "triaged": triaged
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
