import sqlite3
from flask import Flask, render_template, request, session


app = Flask(__name__)
app.secret_key = "graduathion"


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

# ユーザー登録画面の表示


@app.route("/useradd")
def useraddget():
    return render_template("useradd.html")


# ユーザー情報をDBに追加する
@app.route("/useradd", methods=["POST"])
def useraddpost():
    name = request.form.get("name")
    adress = request.form.get("adress")
    password = request.form.get("password")
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("insert into users values (null,?,?,?)",
              (name, adress, password))
    conn.commit()
    c.close()
    # ユーザー登録完了時には末尾にIDをつけて飛ばす
    return "ユーザー登録完了"

# ログインページの表示


@ app.route("/login")
def login_get():
    return render_template("login.html")

# ログインページの機能実装


@ app.route("/login", methods=["POST"])
def login_post():
    adress = request.form.get("adress")
    password = request.form.get("password")
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("select id from users where adress = ? and pass = ?",
              (adress, password))
    user_id = c.fetchone()
    c.close()

    # ログインできなかった場合どこに飛ばしましょうか？
    if user_id is None:
        return "ユーザー情報がないよ"
     # ログインできた場合は末尾にIDをつけて新規作成ページに飛ばす
    else:
        session["user_id"] = user_id[0]
        return "ログイン完了"


@ app.errorhandler(404)
def notfound(code):
    return "404エラー"


if __name__ == "__main__":
    app.run(debug=True)
