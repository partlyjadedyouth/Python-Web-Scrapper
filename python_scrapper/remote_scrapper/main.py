"""
These are the URLs that will give you remote jobs for the word 'python'

https://stackoverflow.com/jobs?r=true&q=python
https://weworkremotely.com/remote-jobs/search?term=python
https://remoteok.io/remote-dev+python-jobs

Good luck!
"""
from flask import Flask, render_template, request, redirect, send_file
from scrapper import get_jobs
from exporter import save_to_csv

app = Flask("JobScrapper")

db = {} # Fake DB

# Home: Display a search bar
@app.route("/")
def home():
  return render_template("home.html")

# Report: Display results
@app.route("/report")
def report():
  job = request.args.get('job')
  if job:
    job = job.lower().strip()
    existingJobs = db.get(job)
    if existingJobs:
      jobs = existingJobs
    else:
      jobs = get_jobs(job)
      db[job] = jobs
  else:
    return redirect("/")
  return render_template("report.html", searchingBy=job, numOfJobs=len(jobs), jobs=jobs)

# Export
@app.route("/export")
def export():
  try:
    job = request.args.get('job')
    job = job.lower().strip()
    if not job:
      raise Exception()
    jobs = db.get(job)
    if not jobs:
      raise Exception()
    save_to_csv(job, jobs)
    return send_file(f"{job}.csv")
  except:
    return redirect("/")

app.run()