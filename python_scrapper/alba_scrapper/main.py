import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

# Scrap URLs of superbrands
def get_superbrands(url):
  r = requests.get(url)
  r_soup = BeautifulSoup(r.text, "html.parser")
  goods_box = r_soup.find("div", {"id": "MainSuperBrand"}).find("ul", {"class": "goodsBox"})
  impacts = goods_box.select("li")
  urls = {}  # urls[company] == url
  for impact in impacts:
    brand_hovers = impact.select(".goodsBox-info ~ a")
    for hover in brand_hovers:
      company = hover.select_one(".company > strong").string
      url = hover["href"]
      urls[company] = url
  print(f"Found {len(urls)} companies")
  return urls

# Get max page of the url given as a parameter
def get_max_page(url):
  r = requests.get(url)
  r_soup = BeautifulSoup(r.text, "html.parser")
  if r_soup.select_one(".jobCount"):
    count = int(r_soup.select_one(".jobCount > strong").string.replace(',', ''))
  else:
    count = int(r_soup.select_one(".listCount > strong").string.replace(',', ''))
  return int(count / 50) + 1

# Scrap place, title, time, pay, and date, and append them into job_list
def get_job(url, job_list):
  r = requests.get(url)
  r_soup = BeautifulSoup(r.text, "html.parser")
  rows = r_soup.find_all("tr")
  for row in rows:
    if row.select_one(".local.first"):
      place = row.select_one(".local.first").get_text().replace(u'\xa0', u' ')
      title = row.select_one(".title > a > .company").get_text().strip()
      time = row.select_one(".data").get_text()
      pay = row.select_one(".pay").get_text()
      date = row.select_one(".regDate.last").get_text()
      job_list.append([place, title, time, pay, date])

# Scrap all jobs of the given brand page
def get_jobs(url):
  print(f"Start scrapping {url}")
  max_page = get_max_page(url)
  job_list = []
  for i in range(1, max_page+1):
    print(f"Scrapping page {i}")
    if "www.alba.co.kr/job/brand" in url:
      url_page = url + f"?page={i}"
    else:
      url_page = url + f"job/brand/?page={i}"
    get_job(url_page, job_list)
  print(f"Finished scrapping {url}")
  return job_list

# Save scrapped jobs into a csv file
def make_csv(company, job_list):
  # Replace invalid characters
  valid_company_name = company
  invalid = '<>:"/\|?*'
  for char in invalid:
    valid_company_name = valid_company_name.replace(char, '_')
  # CSV
  f = open(valid_company_name + '.csv', 'w')
  wr = csv.writer(f)
  wr.writerow(["place", "title", "time", "pay", "date"])
  for job_info in job_list:
    wr.writerow(job_info)
  f.close()

# MAIN
superbrands = get_superbrands(alba_url)
for company in superbrands:
  make_csv(company, get_jobs(superbrands[company]))
