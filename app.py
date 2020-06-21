import os
import sqlite3
from flask import Flask, render_template, request, session, redirect


app = Flask(__name__)
app.secret_key = "graduathion"

from datetime import datetime

@app.route('/')
def index():
    return render_template('index.html')

# 記事詳細ページの記事呼び出し
@app.route('/main')
def main():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select photo, text, date from story")
    story = []
    for row in c.fetchall():
        story.append({"photo": row[0], "text": row[1], "date": row[2]})
    c.close()
    print(story)
    return render_template('main.html', story=story)

# マイページ
# @app.route('/mypage')
    # 同時に作動させる方法がわかるまでコメントアウト
    # ユーザー名・メールアドレス・パスワード表示
# def mypage():
#     conn = sqlite3.connect('flaskapp.db')
#     c = conn.cursor()
#     c.execute("select name, mail, user_pass from users where id=1")
#     user_info = c.fetchone()
#     c.close()
#     print(user_info)
#     return render_template('mypage.html', user_info = user_info) 

# マイページの記事一覧表示
@app.route('/mypage')
def mypage():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select area, month, day, title from pages")
    pages = []
    for row in c.fetchall():
        pages.append({"area": row[0], "month": row[1], "day": row[2], "title": row[3]})
    c.close()
    print(pages)
    return render_template('mypage.html', pages = pages)

# 記事一覧ページ
@app.route('/thread')
def thread():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select area, month, day, title from pages")
    pages = []
    for row in c.fetchall():
        pages.append({"area":row[0], "month":row[1], "day":row[2], "title":row[3]})
    c.close()
    print(pages)
    return render_template('thread.html', pages = pages)



@app.route("/useradd")  # ユーザー登録画面の表示
def useraddget():
    return render_template("useradd.html")


@app.route("/useradd", methods=["POST"])  # ユーザー情報をDBに追加する
def useraddpost():
    name = request.form.get("name")
    adress = request.form.get("adress")
    password = request.form.get("password")
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("insert into users values (null,?,?,?)",
              (name, adress, password))
    conn.commit()
    # 登録したIDを取得し、次ページに行くときに末尾に渡す
    c.execute("select id from users where adress = ? and pass = ?",
              (adress, password))
    id = c.fetchone()
    c.close()
    # ユーザー登録完了時には末尾にIDをつけて飛ばす
    return "ユーザー登録完了"


@ app.route("/login")  # ログインページの表示
def login_get():
    return render_template("login.html")


@ app.route("/login", methods=["POST"])  # ログインページの機能実装
def login_post():
    name = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("select id from users where name = ? and pass = ?",
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


@app.route("/ldeletepage/<int:pageid>")  # ページ削除 1が削除
def deletepage(pageid):
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("update page set flag = 0 where id = ?", (pageid,))
    conn.commit()
    conn.close()
    return "マイページへ"


@app.route("/ldeletepost/<int:postid>")  # 投稿削除 1が削除
def deletepost(postid):
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("update post set flag = 0 where id = ?", (postid,))
    conn.commit()
    conn.close()
    return "投稿一覧へ"


@app.route("/pageadd")  # 記事作成の画面を表示
def pageadd_get():
    return render_template("pageadd.html")


@app.route("/pageadd", methods=["POST"])  # 記事のデータを登録
def pageadd_post():
    user_id = session["user_id"]
    title = request.form.get("title")
    month = request.form.get("month")
    date = request.form.get("date")
    month = request.form.get("month")
    prefecture = request.form.get("prefecture")
    editpass = request.form.get("editpass")
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("insert into page values(null,?,?,?,?,?,?,0)",
              (user_id, editpass, title, prefecture, month, date))
    conn.commit()
    c.execute("SELECT ID from page where userID = ? and title = ?",
              (user_id, title))
    id = c.fetchone()
    id = id[0]
    conn.close()
    print(id)
    return ページ登録完了  # 記事一覧へ変更


if __name__ == "__main__":
   app.run(debug=True)
