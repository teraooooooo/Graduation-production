from flask import Flask, render_template, request, session, redirect
import sqlite3
import os
from datetime import datetime
<< << << < HEAD
== == == =
>>>>>> > 4ddf7d886157a3f2cbff52e67ca1fd8788ade637

app = Flask(__name__)
app.secret_key = "graduathion"


@app.route('/')
def index():
    return render_template('index.html')

# 記事詳細ページの記事呼び出し


@app.route('/main')
def main():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select image, content, datetime from post where flag=0 and pageID=1")
    story = []
    for row in c.fetchall():
        story.append({"image": row[0], "content": row[1], "datetime": row[2]})
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
    c.execute("select prefectures, month, date, title from page where flag=0")
    page = []
    for row in c.fetchall():
        page.append({"area": row[0], "month": row[1],
                     "date": row[2], "title": row[3]})
    c.close()
    print(page)
    return render_template('mypage.html', page=page)

# 記事一覧ページ


@app.route('/thread')
def thread():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select prefectures, month, date, title from page where flag=0")
    page = []
    for row in c.fetchall():
        page.append({"area": row[0], "month": row[1],
                     "date": row[2], "title": row[3]})
    c.close()
    print(page)
    return render_template('thread.html', page=page)


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
    adress = request.form.get("name")
    password = request.form.get("password")
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()

    c.execute("select id from users where name = ? and pass = ?",
              (name, password))
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
    # つくった記事詳細ページへ飛ばすだめに作成した記事IDを取得
    c.execute("SELECT ID from page where userID = ? and title = ?",
              (user_id, title))
    id = c.fetchone()
    id = id[0]
    conn.close()
    print(id)
    return "ページ登録完了"  # 記事一覧へ変更


<< << << < HEAD


@app.route("/postadd/<int:pageid>")  # 記事作成の画面を表示
def postadd_get(pageiad):
    return render_template("postadd.html")


@app.route('/postadd/<int:pageid>', methods=["POST"])
def postadd_post(pageid):
    upload = request.files['image']
    # uploadで取得したファイル名をlower()で全部小文字にして、ファイルの最後尾の拡張子が'.png', '.jpg', '.jpeg'ではない場合、returnさせる。
    if not upload.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        return 'png,jpg,jpeg形式のファイルを選択してください'

    # 下の def get_save_path()関数を使用して "./static/img/" パスを戻り値として取得する。
    save_path = get_save_path()
    # ファイルネームをfilename変数に代入
    filename = upload.filename
    # 画像ファイルを./static/imgフォルダに保存。 os.path.join()は、パスとファイル名をつないで返してくれます。
    upload.save(os.path.join(save_path, filename))
    # ファイル名が取れることを確認、あとで使うよ
    print(filename)
    # コンテンツ取得
    content = request.form.get("content")
    # 投稿時間を取得
    datetime = datetime.now().strtime("%Y/%m/%d %H:%m")
    # パスを取得
    editpass = request.form.get("editpass")

    # パスを照会するためにページIDに紐づくエディットパスを取得
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("SELECT editPASS from page where ID = ?", (pageid,))
    page_editpass = c.fetchone()
    page_editpass = page_editpass[0]
    print(page_editpass)

    # 入力したパスと登録されたパスが同じ場合
    if editpass == page_editpass:
       # 上記の filename 変数ここで使うよ
        c.execute("insert into post values(null,?,?,?,?,0)",
                  (pageid, filename, content, datetime))
        conn.commit()
        conn.close()
        return "投稿されました"
     # 入力したパスと登録されたパスがk異なる場合
    else:
        return "passが間違っております"

# 画像の保存場所をstaticsのimg


def get_save_path():
    path_dir = "./static/img"
    return path_dir


if __name__ == "__main__":
    app.run(debug=True)
