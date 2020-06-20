import sqlite3
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def helloworld():
    return "Hello Word"


@app.route("/test")
def test():
    name = "terao"
    return render_template("index.html", name=name)


@app.route("/dbtest")
def dbtest():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select title from page where id = 1")
    page_title = c.fetchone()
    c.close()

    print(page_title)
    return render_template('dbtest.html', page_title=page_title)


if __name__ == "__main__":
    app.run(debug=True)
