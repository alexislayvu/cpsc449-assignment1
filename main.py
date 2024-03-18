import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configuration
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_DB"] = "job_board"

mysql = MySQL(app)


# route for home page
@app.route("/")
def home():
    return "Hello! Welcome to the Job Board."


# CREATE: add a new job listing to the database
@app.route("/jobs", methods=["POST"])
def add_job():
    data = request.json
    title = data.get("title")
    company = data.get("company")
    location = data.get("location")

    if title and company and location:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO jobs (title, company, location) VALUES (%s, %s, %s)",
            (title, company, location),
        )
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Job added successfully"}), 201
    else:
        return jsonify({"error": "Missing required fields"}), 400


# READ: list all jobs in the database
@app.route("/jobs", methods=["GET"])
def get_jobs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM jobs")
    jobs = cur.fetchall()
    cur.close()
    return jsonify(jobs)


# UPDATE: update an existing job listing in the database
@app.route("/jobs/<int:job_id>", methods=["PUT"])
def update_job(job_id):
    data = request.json
    title = data.get("title")
    company = data.get("company")
    location = data.get("location")

    cur = mysql.connection.cursor()

    # check if the job with the given ID exists
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    existing_job = cur.fetchone()
    if not existing_job:
        cur.close()
        return jsonify({"message": "Job not found"}), 404

    # update the job if it exists
    cur.execute(
        "UPDATE jobs SET title = %s, company = %s, location = %s WHERE id = %s",
        (title, company, location, job_id),
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Job updated successfully"})


# DELETE: delete a job listing from the database by ID
@app.route("/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    cur = mysql.connection.cursor()

    # check if the job with the given ID exists
    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    existing_job = cur.fetchone()
    if not existing_job:
        cur.close()
        return jsonify({"message": "Job not found"}), 404

    # delete the job if it exists
    cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "Job deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
