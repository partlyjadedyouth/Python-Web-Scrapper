import csv

def save_to_file(list_):
    file = open("jobs.csv", mode='w')
    writer = csv.writer(file)
    writer.writerow(["title", "company", "location", "link"])
    for elem in list_:
        writer.writerow(list(elem.values()))
    return