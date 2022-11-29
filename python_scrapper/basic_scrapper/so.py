from ast import JoinedStr
from pickle import TRUE
import requests
from bs4 import BeautifulSoup

url = "https://stackoverflow.com/jobs?q=python"

def get_last_page():
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "lxml")    
    pages = soup.find("div", {"class": "s-pagination"}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title = html.select_one("h2 > a")
    company = html.select_one("h3 > span")
    location = html.select_one("h3 > .fc-black-500")
    if title:
        link_href = title["href"]
        title = title["title"]
        company = company.get_text(strip=True)
        location = location.get_text(strip=True)
        link = f"https://stackoverflow.com{link_href}"
    else:
        title = company = location = link = None
    return {"title": title, "company": company, "location": location, "link": link}

def extract_jobs(last_page):
    jobs = []
    for page in range(1, last_page+1):
        print(f"Scrapping SO Page #{page}")
        result = requests.get(f"{url}&pg={page}")
        soup = BeautifulSoup(result.text, "html.parser")
        rows = soup.find_all("div", {"class": "flex--item fl1"})[1:]
        for row in rows:
            job = extract_job(row)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs