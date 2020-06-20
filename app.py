import os
import sqlite3
from flask import Flask , render_template , request , redirect , session
app = Flask(__name__)

app.secret_key = 'NightTeamE'

from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/thread')
def thread():
    return render_template('thread.html')
    
if __name__ == "__main__":
    app.run(debug=True)
