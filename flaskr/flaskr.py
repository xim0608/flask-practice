# all the imports
import sqlite3
from sqlite3 import IntegrityError
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

# configuration=設定,構成
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


#同じファイル内でアプリケーションインスタンスの初期化を行ないます。
# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

#データベースにコネクトするメソッドを実装していきます
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

#.db のファイルは作らなくていいの？→作られる

from contextlib import closing

'''
from contextlib import closing
from urllib.request import urlopen

with closing(urlopen('http://www.python.org')) as page:
    for line in page:
        print(line)
'''

#The closing() helper function allows us to keep a connection open for the duration of the with block.
#The open_resource() method of the application object supports that functionality out of the box, so it can be used in the with block directly.

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

# from flaskr import init_db
# init_db()

#データベースの利用
# @app.after_request
# def after_request(response):
#     g.db.close()
#     return response

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    g.db.close()
    return response

#DB内のエントリー一覧
@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

#エントリーを追加（ここではログイン状態もチェックしています。(session内の logged_in キーが True ））
@app.route('/add', methods=['POST'])
def add_entry():
    # if not session.get('logged_in'):
    #     abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

#signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        # flash(request.form['username'])
        try:
            g.db.execute('insert into users (username, password) values (?, ?)',
                         [request.form['username'], request.form['password']])
            g.db.commit()
        except IntegrityError:
            flash("ユーザーがもういます")
            return redirect(url_for('signup'))
        return redirect(url_for('login'))
    return render_template('signup.html')

#ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        cur = g.db.execute('select username, password from users where username=?',[request.form['username']])
        user = cur.fetchall()[0]
        # userlist[0]=list(user[0].split(','))
        print(user)
        print(user[0])
        # print("'"+request.form['username']+"'")
        if request.form['username'] != user[0]:
            error = 'Invalid username'
        elif request.form['password'] != user[1]:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

#ログアウト
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

#最後にアプリケーションを実行させます
if __name__ == '__main__':
    app.run()
