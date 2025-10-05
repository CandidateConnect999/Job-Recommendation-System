from flask import Flask, jsonify
import os

app = Flask(__name__)

# fake test data
fake_candidates = [
    (1, "Alice", ["Python", "SQL"], "Boston", 3, 70000),
    (2, "Bob", ["JavaScript", "React"], "NYC", 2, 60000),
]

fake_jobs = [
    (1, "Backend Developer", ["Python", "Flask"], "Boston", 2, 80000),
    (2, "Frontend Developer", ["JavaScript", "React"], "NYC", 1, 65000),
]

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
    candidate = next((c for c in fake_candidates if c[0] == candidate_id), None)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    ranked = sorted(fake_jobs, key=lambda j: match_candidate(j, candidate), reverse=True)
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

@app.route("/")
def home():
    return "Teste"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
