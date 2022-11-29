import requests
from bs4 import BeautifulSoup

def get_so_jobs(job):
  job_list = []

  url = f"https://stackoverflow.com/jobs?r=true&q={job}"
  so_result = requests.get(url)
  so_soup = BeautifulSoup(so_result.text, "html.parser")
  pages = so_soup.find_all("a", {"class": "s-pagination--item"})
  if not pages:
    last_page = 1
  else:
    last_page = int(pages[-2].get_text())

  for page_num in range(last_page):
    page_url = f"https://stackoverflow.com/jobs?r=true&q={job}&pg={page_num+1}"
    page_url_result = requests.get(page_url)
    page_url_soup = BeautifulSoup(page_url_result.text, "html.parser")
    jobs = page_url_soup.find("div", {"class": "listResults"}).find_all("div", {"data-jobid": True})
    for job in jobs:
      try:
        company = job.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span", recursive=False).get_text().strip()
        title = job.find("h2", {"class": "mb4 fc-black-800 fs-body3"}).find("a", {"title": True})["title"]
        location = job.find("h3", {"class": "fc-black-700 fs-body1 mb4"}).find("span", {"class": "fc-black-500"}).get_text().strip()
        link = "https://stackoverflow.com/jobs/" + job["data-jobid"]
        job_list.append({"company": company, "title": title, "location": location, "link": link})
      except:
        pass

  return job_list

def get_wwr_jobs(job):
  job_list = []

  url = f"https://weworkremotely.com/remote-jobs/search?term={job}"
  wwr_result = requests.get(url)
  wwr_soup = BeautifulSoup(wwr_result.text, "html.parser")
  jobs = wwr_soup.find_all("li")

  for job in jobs:
    try:
      company = job.find("span", {"class": "company"}).get_text().strip()
      title = job.find("span", {"class": "title"}).get_text().strip()
      location = job.find("span", {"class": "region company"}).get_text().strip()
      link = "https://weworkremotely.com/" + job.find("a", recursive=False)["href"]
      job_list.append({"company": company, "title": title, "location": location, "link": link})
    except:
      pass

  return job_list

def get_rok_jobs(job):
  job_list = []

  url = f"https://remoteok.com/remote-dev+{job}-jobs"
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
  }
  
  rok_result = requests.get(url, headers=headers)
  rok_soup = BeautifulSoup(rok_result.text, "html.parser")

  if rok_soup.find("table") is None:
      pass
  else:
      jobs = rok_soup.find("table").find_all("tr", attrs={"data-company": True})
      for job in jobs:
          try:
              company = job["data-company"]
              title = job.find("h2", {"itemprop": "title"}).get_text().strip()
              location = job.find("div", {"class": "location tooltip"}).get_text().strip()
              link = "https://remoteok.com/l/" + job["data-id"]
              job_list.append({"company": company, "title": title, "location": location, "link": link})
          except:
              pass
  return job_list

def get_jobs(job):
  return get_so_jobs(job) + get_wwr_jobs(job) + get_rok_jobs(job)
  