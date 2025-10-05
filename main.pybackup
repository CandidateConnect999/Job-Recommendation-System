import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Connect to database (only if DATABASE_URL is set)
DATABASE_URL = os.environ.get("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL) if DATABASE_URL else None
cursor = conn.cursor() if conn else None


def match_candidate(job, candidate):
    score = 0
    for skill in job[2]:
        if skill in candidate[2]:
            score += 2
    if job[3] == candidate[3]:
        score += 1
    if candidate[4] >= job[4]:
        score += 1
    if candidate[5] <= job[5]:
        score += 1
    return score


@app.route("/matches/<int:candidate_id>")
def get_matches(candidate_id):
    if not cursor:
        return jsonify({"error": "Database not connected"}), 500

    # Get candidate by id
    cursor.execute("SELECT * FROM candidates WHERE id=%s;", (candidate_id,))
    candidate = cursor.fetchone()

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    # Get all jobs
    cursor.execute("SELECT * FROM jobs;")
    jobs = cursor.fetchall()

    # Rank jobs against candidate
    ranked = sorted(jobs, key=lambda j: match_candidate(j, candidate), reverse=True)

    results = []
    for j in ranked:
        results.append({
            "id": j[0],
            "title": j[1],
            "skills": j[2],
            "location": j[3],
            "experience_required": j[4],
            "salary_offered": j[5]
        })
    return jsonify(results)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
