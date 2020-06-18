import os
import sqlite3
from flask import Flask , render_template , request , redirect , session
app = Flask(__name__)

app.secret_key = 'NightTeamE'

from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/list')
def list():
    return render_template('list.html')

if __name__ == "__main__":
    app.run(debug=True)
