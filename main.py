from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Home route (test if API is alive)
@app.route("/")
def home():
    return "Job Matching API is running!"

# Job recommendation route
@app.route("/recommendations", methods=["POST"])
def recommendations():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    # Get candidate data
    skills = data.get("skills", [])
    location = data.get("location", "")
    experience = data.get("experience", 0)
    salary = data.get("salary", 0)

    # Dummy job database (you can replace later)
    jobs = [
        {
            "title": "Frontend Developer",
            "skills": ["JavaScript", "React"],
            "location": "NYC",
            "experience": 2,
            "salary": 70000
        },
        {
            "title": "Backend Developer",
            "skills": ["Python", "Flask"],
            "location": "Remote",
            "experience": 3,
            "salary": 80000
        },
        {
            "title": "Full Stack Developer",
            "skills": ["JavaScript", "React", "Python"],
            "location": "NYC",
            "experience": 2,
            "salary": 90000
        }
    ]

    matched_jobs = []

    for job in jobs:
        score = 0

        # Skill match
        for skill in skills:
            if skill in job["skills"]:
                score += 1

        # Location match
        if location == job["location"]:
            score += 2

        # Experience match
        if experience >= job["experience"]:
            score += 1

        # Salary match
        if salary <= job["salary"]:
            score += 1

        job_copy = job.copy()
        job_copy["match_score"] = score
        matched_jobs.append(job_copy)

    # Sort by best match
    matched_jobs.sort(key=lambda x: x["match_score"], reverse=True)

    return jsonify(matched_jobs)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
