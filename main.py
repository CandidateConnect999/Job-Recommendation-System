from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Fake Test Data
# -----------------------------

fake_candidates = [
    (1, "Alice", ["Python", "SQL"], "Boston", 3, 70000),
    (2, "Bob", ["JavaScript", "React"], "NYC", 2, 60000),
]

fake_jobs = [
    (1, "Backend Developer", ["Python", "Flask"], "Boston", 2, 80000),
    (2, "Frontend Developer", ["JavaScript", "React"], "NYC", 1, 65000),
]

# -----------------------------
# Matching Algorithm
# -----------------------------

def match_candidate(job, candidate):
    score = 0

    # Skill match
    for skill in job[2]:
        if skill in candidate[2]:
            score += 2

    # Location match
    if job[3] == candidate[3]:
        score += 1

    # Experience match
    if candidate[4] >= job[4]:
        score += 1

    # Salary match
    if candidate[5] <= job[5]:
        score += 1

    return score


# -----------------------------
# API Routes
# -----------------------------

@app.route("/")
def home():
    return "Job Matching API is running!"

@app.route("/matches/<int:candidate_id>")
def get_matches(candidate_id):

    candidate = next((c for c in fake_candidates if c[0] == candidate_id), None)

    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    results = []

    for job in fake_jobs:
        score = match_candidate(job, candidate)
        results.append({
            "job_id": job[0],
            "title": job[1],
            "location": job[3],
            "salary": job[5],
            "match_score": score
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)

    return jsonify(results)


# -----------------------------
# Run App
# -----------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
