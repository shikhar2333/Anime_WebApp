from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session, logging
import sqlite3, time


mal = "https://myanimelist.net/"
topanimelist = "https://myanimelist.net/topanime.php?limit=14150"
#0 to 14150
topmangalist = "https://myanimelist.net/topmanga.php?limit=46100"
#0 to 46100
searchmal = "https://myanimelist.net/search/prefix.json?type=all&keyword=boku&v=1"
malanime = "https://myanimelist.net/search/prefix.json?type=anime&keyword=boku&v=1"
malmanga = "https://myanimelist.net/search/prefix.json?type=manga&keyword=boku&v=1"
malcharacter = "https://myanimelist.net/search/prefix.json?type=character&keyword=boku&v=1"
maluser = "https://myanimelist.net/search/prefix.json?type=user&keyword=boku&v=1"


conn = sqlite3.connect('weebcheck.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS mangalist (id INT(10), name TEXT, description VARCHAR(500), imagelink TEXT, shortimage TEXT, rating FLOAT(7,4) PRIMARY KEY, volumes TEXT, author TEXT, genre1 TEXT, genre2 TEXT, genre3 TEXT, genre4 TEXT, genre5 TEXT, genre6 TEXT, genre7 TEXT, genre8 TEXT, noofusers INTEGER, favourite INTEGER)")



curr_url = "https://myanimelist.net/topmanga.php?limit=0"
site=requests.get(curr_url)
soup = BeautifulSoup(site.text, 'html.parser')
div = soup.find_all("tr", {"class" : "ranking-list"})
rating = 9.5000
for anime in div:
	an = anime.find("td",{"class":"title"})
	url = an.a["href"]
	shortimg = str(an.a.img['data-src'])
	mal_id = str(url).split("/")
	url = "https://myanimelist.net/manga/"+mal_id[4]
	aname = str(mal_id[5])
	asite = requests.get(url)
	htsoup = BeautifulSoup(asite.text, 'html.parser')
	imglink = htsoup.find("img", {"class": "ac"}).get('src')
	des = str(htsoup.find("span", {"itemprop": "description"}))
	print(mal_id[5])
	volumes = str(htsoup.find("div", {"class": "spaceit"}))
	
	genre1 = htsoup.find_all("a")[55].get('title')
	genre2 = htsoup.find_all("a")[56].get('title')
	genre3 = htsoup.find_all("a")[57].get('title')
	genre4 = htsoup.find_all("a")[58].get('title')
	genre5 = htsoup.find_all("a")[59].get('title')
	genre6 = htsoup.find_all("a")[60].get('title')
	genre7 = htsoup.find_all("a")[61].get('title')
	genre8 = htsoup.find_all("a")[62].get('title')
	author = str(htsoup.find_all("span",{"class": "dark_text"} )[9].parent)
	# licensor = htsoup.find_all("a")[61].get('title')
	cur.execute("INSERT INTO mangalist (id, name, description, imagelink, shortimage, rating, volumes, author, genre1,  genre2, genre3, genre4, genre5, genre6, genre7, genre8,noofusers,favourite) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,0,0)" , (mal_id[4], mal_id[5], des, imglink, shortimg, rating, volumes, author, genre1,  genre2, genre3, genre4, genre5, genre6, genre7, genre8))
	conn.commit()
	rating = round((rating - 0.01),2)


