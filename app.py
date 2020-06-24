from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "graduathion"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/alllink')
def all_link():
    return render_template('alllink.html')

# 記事詳細ページの記事呼び出し

# ちょっといじりました　0624寺尾


@app.route('/main/<int:pageid>')
def main(pageid):
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute(
        "select image, content, datetime,id from post where flag=0 and pageID=?", (pageid,))
    story = []
    for row in c.fetchall():
        story.append(
            {"image": row[0], "content": row[1], "datetime": row[2], "id": row[3]})
    c.close()
    print(pageid)
    print(story)
    return render_template('main.html', pageid=pageid, story=story)

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

# マイページのユーザー情報・記事一覧表示


@app.route('/mypage')
def mypage():
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    # usersのid＝1を呼び出し
    c.execute("select name, adress, pass from users where id=1")
    user_info = c.fetchone()
    # page のUserID=2を呼び出し
    c.execute(
        "select prefectures, month, date, title, id from page where flag=0 and UserID=2")
    page = []
    for row in c.fetchall():
        page.append({"area": row[0], "month": row[1],
                     "date": row[2], "title": row[3], "pageid": row[4]})
    c.close()
    print(user_info)
    print(page)
    return render_template('mypage.html', page=page, user_info=user_info)

# 記事一覧ページ  都道府県指定


@app.route('/thread/<int:areaid>', methods=["GET"])
def thread(areaid):
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("select area from Prefecture where No=?", (areaid,))
    area = c.fetchone()
    c.execute(
        "select month, date, title from page where flag=0 and prefectures=?", (areaid,))
    page = []
    for row in c.fetchall():
        page.append({"month": row[0], "date": row[1], "title": row[2]})
    c.close()
    print(area)
    print(page)
    return render_template('thread.html', page=page, area=area)


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
    c.close()
    # ページ作成ページへ飛ばす
    return redirect("/pageadd")


@ app.route("/login")  # ログインページの表示
def login_get():
    return render_template("login.html")


@ app.route("/login", methods=["POST"])  # ログインページの機能実装
def login_post():
    adress = request.form.get("adresss")
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
    # 記事作成ページへ飛ばす
        return redirect("/pageadd")


@app.route("/deletepage/<int:pageid>")  # ページ削除 1が削除
def deletepage(pageid):
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("update page set flag = 1 where id = ?", (pageid,))
    conn.commit()
    conn.close()
    return redirect("/mypage")


@app.route("/deletepost/<int:postid>")  # 投稿削除 1が削除
def deletepost(postid):
    conn = sqlite3.connect("flaskapp.db")
    c = conn.cursor()
    c.execute("update post set flag = 1 where ID = ?", (postid,))
    conn.commit()
    c.execute("select pageID form post where ID = ?", (postid,))
    pageid = c.fetchone()
    pageid = pageid[0]
    conn.close()
    return redirect(url_for('main', postid=pageid))  # 修正の必要あり


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
    period = request.form.get("period")
    prefecture = request.form.get("prefecture")
    editpass = request.form.get("editpass")
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("insert into page values(null,?,?,?,?,?,?,0,?)",
              (user_id, editpass, title, prefecture, month, date, period))
    conn.commit()
    # つくった記事詳細ページへ飛ばすだめに作成した記事IDを取得
    c.execute("SELECT ID from page where userID = ? and title = ?",
              (user_id, title))
    id = c.fetchone()
    id = id[0]
    conn.close()
    print(id)
    return redirect(url_for('main', pageid=id))  # 記事詳細へ変更


@app.route("/postadd/<int:pageid>")  # 記事作成の画面を表示
def postadd_get(pageid):
    return render_template("postadd.html", pageid=pageid)


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
    posttime = datetime.now().strftime("%Y/%m/%d %H:%m")
    print(posttime)
    # パスを取得
    editpass = request.form.get("editpass")
    # DB内にある編集パスを取得
    conn = sqlite3.connect('flaskapp.db')
    c = conn.cursor()
    c.execute("SELECT editPASS from page where ID = ?", (pageid,))
    page_editpass = c.fetchone()
    page_editpass = page_editpass[0]
    print(editpass)
    print(page_editpass)

    # 入力したパスと登録されたパスがk異なる場合
    if editpass != page_editpass:
        return "passが間違っております"
    else:
        conn = sqlite3.connect('flaskapp.db')
        c = conn.cursor()
        c.execute("insert into post values(null,?,?,?,?,0)",
                  (pageid, filename, content, posttime))
        conn.commit()
        conn.close()
        return redirect(url_for('main', pageid=pageid))

# 画像の保存場所をstaticsのimg


def get_save_path():
    path_dir = "./static/img"
    return path_dir


@app.route('/nwe')
def nwe():
    return render_template('nwe.html')


@app.route('/top')
def top():
    return render_template('top.html')


@app.route('/second')
def second():
    return render_template('second.html')


@app.errorhandler(404)
def notfound(code):
    return "404.エラーです。TOPに戻りましょう"


if __name__ == "__main__":
    app.run(debug=True)
