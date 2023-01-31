from flask import Flask, render_template, request, flash
from random import choice
from werkzeug.utils import secure_filename
import sqlite3


web_site = Flask(__name__)


@web_site.route('/')
def index():
  print("Home Page")

  return render_template("index.html")

@web_site.route('/hawaiian')
def aloha():
  print("Opening List Page")
  jobs = ["doctor","engineer","lawyer"]
  return render_template("hawaiian.html",job=choice(jobs))

@web_site.route('/Guten_Tag/' , defaults ={'username ': None})
@web_site.route('/Guten_Tag/<username>')
def sayhi(username):
  if not username:
    username = request.args.get('username')
  if not username:
    return 'Error, no username given'
  else:
    return "<h1>Guten Tag</h1>"

  return "<h1>Hello</h1><p>its monday</p>"


@web_site.route('/runonce')
def createDBandTable():
  con = sqlite3.connect('anime.db')
  sql = '''CREATE TABLE ANIMES(
	 AnimeID INTEGER PRIMARY KEY AUTOINCREMENT,
   Name TEXT NOT NULL,
	 Length INTEGER NOT NULL 
)'''
  cursor = con.cursor()
  cursor.execute(sql)
  con.commit()
  return "database and table created"

@web_site.route('/add',methods = ['GET', 'POST'])
def addanime():
  msg = ""
  if request.method == 'POST':
    name = request.form["name"]
    length = request.form["length"]
    con = sqlite3.connect('anime.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO ANIMES(Name,Length) VALUES(?,?)",(name,length))
    con.commit()
    msg = name + " added to the anime"
  return render_template("addanime.html",msg = msg)

@web_site.route('/animelist')
def listall():
  con = sqlite3.connect('anime.db')
  con.row_factory = sqlite3.Row
  cursor = con.cursor()
  cursor.execute('SELECT * FROM ANIMES')
  con.commit()
  rows = cursor.fetchall()
  return render_template("animelist.html",rows = rows)

web_site.run(host='0.0.0.0', port=8080)