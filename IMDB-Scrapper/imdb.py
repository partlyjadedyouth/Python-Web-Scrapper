from bs4 import BeautifulSoup
import requests
import csv

url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

imdb_req = requests.get(url)
imdb_soup = BeautifulSoup(imdb_req.text, "lxml")

lister_list_tr = imdb_soup.select(".lister-list > tr")

movies = []
for tr in lister_list_tr:
    title = tr.select_one(".titleColumn > a").string
    year = tr.select_one(".titleColumn > span").string[1:-1]
    imdb_rating = tr.select_one(".ratingColumn.imdbRating > strong").string
    movies.append({"title": title, "year": year, "imdb_rating": imdb_rating})

f = open('imdb_scrapping.csv', 'w')
wr = csv.writer(f)
wr.writerow(['title', 'year', 'imdb_rating'])
for movie in movies:
    wr.writerow([movie['title'], movie['year'], movie['imdb_rating']])
