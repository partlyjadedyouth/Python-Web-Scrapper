import csv

def save_to_csv(job, jobs):
    file = open(f"{job}.csv", mode='w')
    writer = csv.writer(file)
    writer.writerow(["company", "title", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    return
