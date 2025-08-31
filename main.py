import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

conn = psycopg2.connect(os.environ['DATABASE_URL'])
cursor = conn.cursor()

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

@app.route('/matches/<int:job_id>')
def get_matches(job_id):
    cursor.execute("SELECT * FROM candidates WHERE id=%s;", (job_id,))
    candidate = cursor.fetchone()
    cursor.execute("SELECT * FROM jobs;")
    jobs = cursor.fetchall()
    ranked = sorted(candidates, key=lambda c: match_candidate(job, c), reverse=True)
    results = []
    for c in ranked:
        results.append({
            'id': c[0],
            'name': c[1],
            'skills': c[2],
            'location': c[3],
            'experience': c[4],
            'salary_expectation': c[5]
        })
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
