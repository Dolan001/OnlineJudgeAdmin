from flask import Flask, render_template, request, redirect, url_for, session, escape
import mysql.connector
import datetime
import time
from bs4 import BeautifulSoup

app = Flask(__name__)
ts = time.time()
con = mysql.connector.connect(host="localhost", user="root", password="", db="forum")


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password_1']
    conpass = request.form['password_2']
    fname = request.form['fname']
    lname = request.form['lname']
    city = request.form['city']
    if password == conpass:
        cursor = con.cursor()
        sql = "INSERT INTO users(username, email, password, firstName, lastName, city) VALUES(%s,%s,%s,%s,%s,%s)"
        val = (username, email, password, fname, lname, city)
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for('home'))
    else:
        return 'failed'


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('home'))
    username = request.form['username']
    password = request.form['password']
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE username = '" + username + "' AND password= '" + password + "'")
    user = cursor.fetchall()
    if len(user) is 1:
        session['username'] = request.form['username']
        return redirect(url_for('home'))
    else:
        return 'failed'


@app.route('/home', defaults={'page': 0}, methods=['GET'])
@app.route('/home/page/<int:page>', methods=['GET'])
def home(page):
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        perpage = 5
        startat = page * perpage
        pages = page + 1
        cursor = con.cursor()
        cursor.execute('SELECT * FROM articles ORDER BY id desc limit %s, %s;', (startat, perpage))
        data = cursor.fetchall()
        cursor.execute('SELECT id, username, sum(rating) FROM articles'
                       ' GROUP BY username ORDER BY sum(rating) desc')
        rating = cursor.fetchall()
        cursor.execute('SELECT title_id, COUNT(comment) FROM comments GROUP BY title_id')
        count_comment = cursor.fetchall()
        cursor.execute('select id, username, count(username) from articles '
                       'group by username order by count(username) desc')
        count_cont = cursor.fetchall()
        cursor.execute('select title_id, count(reaction) from reactions where reaction="1" group by title_id')
        count_reaction = cursor.fetchall()
        cursor.execute('select title_id, count(reaction) from reactions where reaction="-1" group by title_id')
        count_reaction_u = cursor.fetchall()
        return render_template('home.html', session_user_name=username_session,
                               data=data, count_pages_article=pages, ratings=rating,
                               count_comment=count_comment, count_cont=count_cont, page=page,
                               count_reaction=count_reaction, count_reaction_U=count_reaction_u)
    return redirect(url_for('login'))


@app.route('/home/contest', defaults={'page': 0}, methods=['GET'])
@app.route('/home/contest/page/<int:page>', methods=['GET'])
def contest(page):
    username_session = escape(session['username']).capitalize()
    perpage = 5
    startat = page * perpage
    pages = page + 1
    cursor = con.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id desc limit %s, %s;', (startat, perpage))
    data = cursor.fetchall()
    cursor.execute('SELECT id, username, sum(rating) FROM articles'
                   ' GROUP BY username ORDER BY sum(rating) desc')
    rating = cursor.fetchall()
    cursor.execute('SELECT title_id, COUNT(comment) FROM comments GROUP BY title_id')
    count_comment = cursor.fetchall()
    cursor.execute('select id, username, count(username) from articles '
                   'group by username order by count(username) desc')
    count_cont = cursor.fetchall()
    cursor.execute('select title_id, count(reaction) from reactions where reaction="1" group by title_id')
    count_reaction = cursor.fetchall()
    cursor.execute('select title_id, count(reaction) from reactions where reaction="-1" group by title_id')
    count_reaction_u = cursor.fetchall()
    return render_template('contest.html', session_user_name=username_session,
                           data=data, count_pages_contest=pages, ratings=rating,
                           count_comment=count_comment, count_cont=count_cont, page=page,
                           count_reaction=count_reaction, count_reaction_U=count_reaction_u)


@app.route('/home/problem', defaults={'page': 0}, methods=['GET'])
@app.route('/home/problem/page/<int:page>', methods=['GET'])
def problem(page):
    username_session = escape(session['username']).capitalize()
    perpage = 5
    startat = page * perpage
    pages = page + 1
    cursor = con.cursor()
    cursor.execute('SELECT * FROM articles ORDER BY id desc limit %s, %s;', (startat, perpage))
    data = cursor.fetchall()
    cursor.execute('SELECT id, username, sum(rating) FROM articles'
                   ' GROUP BY username ORDER BY sum(rating) desc')
    rating = cursor.fetchall()
    cursor.execute('SELECT title_id, COUNT(comment) FROM comments GROUP BY title_id')
    count_comment = cursor.fetchall()
    cursor.execute('select id, username, count(username) from articles '
                   'group by username order by count(username) desc')
    count_cont = cursor.fetchall()
    cursor.execute('select title_id, count(reaction) from reactions where reaction="1" group by title_id')
    count_reaction = cursor.fetchall()
    cursor.execute('select title_id, count(reaction) from reactions where reaction="-1" group by title_id')
    count_reaction_u = cursor.fetchall()
    return render_template('problem.html', session_user_name=username_session,
                           data=data, count_pages_problem=pages, ratings=rating,
                           count_comment=count_comment, count_cont=count_cont, page=page,
                           count_reaction=count_reaction, count_reaction_U=count_reaction_u)


@app.route('/home/addArticle')
def addArticle():
    username_session = escape(session['username']).capitalize()
    return render_template('addArticle.html', session_user_name=username_session)


@app.route('/uploadArticle', methods=['POST'])
def uploadArticle():
    username_session = escape(session['username']).capitalize()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    title = request.form['title']
    editor_text = request.form['text_editor']
    text = BeautifulSoup(editor_text, "html.parser").text
    cursor = con.cursor()
    sql_add_article = "INSERT INTO articles(username, title, article, time, updated_article, updated_time,rating) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    article_val = (username_session, title, text, timestamp, 'null', 'null', '5')
    cursor.execute(sql_add_article, article_val)
    session['title'] = request.form['title']
    con.commit()
    return redirect(url_for('home'))


@app.route('/editArticle/<title_id>/<article_title>', methods=["POST"])
def editArticle(title_id, article_title):
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    editor_text = request.form['text_editor']
    text = BeautifulSoup(editor_text, "html.parser").text
    cursor = con.cursor()
    check_article = "select updated_article, updated_time from articles where id = %s"
    check_article_var = (title_id,)
    cursor.execute(check_article, check_article_var)
    check_article_data = cursor.fetchall()
    if check_article_data is 0:
        sql = "insert into articles(updated_article, updated_time) values(%s, %s)"
        val = (text, timestamp)
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for('article', title_id=title_id, article_title=article_title))
    else:
        cursor.execute("update articles set updated_article= '"+text+"' and updated_time= '"+timestamp+"'")
        return redirect(url_for('article', title_id=title_id, article_title=article_title))


@app.route('/home/profile/<username>')
def profile(username):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    cursor.execute('select * from articles where username = "'+username+'" order by(id) desc')
    posts = cursor.fetchall()
    cursor.execute('select * from users where username = "' + username + '"')
    user_details = cursor.fetchone()
    return render_template('profile.html', myname=username_session, post=posts, username=username,
                           userDetails=user_details)


@app.route('/follow/<username>')
def follow(username):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    user_follow_sql = "select * from follow where following = %s and follower = %s"
    user_follow_var = (username, username_session, )
    cursor.execute(user_follow_sql, user_follow_var)
    check_user_name_follow = cursor.fetchall()
    if username_session == username:
        print('you cant follow yourself')
        return redirect(url_for('profile', username=username))
    else:
        if len(check_user_name_follow) is 0:
            sql_follow = "INSERT INTO follow(following, follower) VALUES(%s,%s)"
            val_follow = (username, username_session)
            cursor.execute(sql_follow, val_follow)
            con.commit()
            print("every thing is okey")
            print(username)
            print(username_session)
            return redirect(url_for('profile', username=username))
        else:
            print("you followed him/her before")
            return redirect(url_for('profile', username=username))


@app.route('/article/<title_id>/<article_title>', methods=['GET'])
def article(title_id, article_title):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM articles WHERE title = '" + article_title + "' and id = '" + title_id + "'")
    article = cursor.fetchall()
    cursor.execute('SELECT * FROM comments WHERE title = "' + article_title + '" and title_id = "' + title_id + '"')
    comment_data = cursor.fetchall()
    cursor.execute('SELECT replies.* FROM comments INNER JOIN replies ON (replies.title_id=comments.id)')
    reply_data = cursor.fetchall()
    cursor.execute('Select count(comment) from comments where title_id = "' + title_id + '"')
    comments_count = cursor.fetchone()
    con.commit()
    return render_template('article.html', data=article, username=username_session, comment=comment_data,
                           reply=reply_data, comments_count=comments_count)


@app.route('/comment/<title_id>/<article_title>', methods=['POST'])
def comment(title_id, article_title):
    username_session = escape(session['username']).capitalize()
    comment = request.form['comment']
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor = con.cursor()
    sql = "INSERT INTO comments(username, title, comment, time, title_id ) VALUES(%s,%s,%s,%s,%s)"
    val = (username_session, article_title, comment, timestamp, title_id)
    cursor.execute(sql, val)
    con.commit()
    return redirect(url_for('article', article_title=article_title, title_id=title_id))


@app.route('/reply/<title_id>/<article_title>', methods=['POST'])
def reply(title_id, article_title):
    username_session = escape(session['username']).capitalize()
    reply = request.form['reply']
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    cursor = con.cursor()
    sql = "INSERT INTO replies(username, title, reply, time, title_id ) VALUES(%s,%s,%s,%s,%s)"
    val = (username_session, article_title, reply, timestamp, title_id)
    cursor.execute(sql, val)
    con.commit()
    return redirect(url_for('article', article_title=article_title, title_id=title_id))


@app.route('/like/<title_id>/<title>/<int:page>')
def like(title_id, title, page):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    user_like_sql = "select * from reactions where username = %s and reaction = %s and title_id = %s"
    user_like_var = (username_session, "1", title_id,)
    cursor.execute(user_like_sql, user_like_var)
    check_user_name_like = cursor.fetchall()

    user_unlike_sql = "select * from reactions where username = %s and reaction = %s and title_id = %s"
    user_unlike_var = (username_session, "-1", title_id,)
    cursor.execute(user_unlike_sql, user_unlike_var)
    check_user_name_unlike = cursor.fetchall()

    if len(check_user_name_like) is 0:
        sql = 'INSERT INTO reactions(username, title, reaction, title_id) VALUES (%s,%s,%s,%s)'
        val = (username_session, title, '1', title_id)
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for('home', page=page))
    elif len(check_user_name_like) is 1:
        return redirect(url_for('home', page=page))
    elif len(check_user_name_unlike) is 1:
        reactsql = 'update reactions set reaction = "1" where username = "' + username_session + '"'
        cursor.execute(reactsql)
        return redirect(url_for('home', page=page))


@app.route('/unlike/<title_id>/<title>/<int:page>')
def unlike(title_id, title, page):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    user_like_sql = "select * from reactions where username = %s and reaction = %s and title_id = %s"
    user_like_var = (username_session, "1", title_id,)
    cursor.execute(user_like_sql, user_like_var)
    check_user_name_like = cursor.fetchall()

    user_unlike_sql = "select * from reactions where username = %s and reaction = %s and title_id = %s"
    user_unlike_var = (username_session, "-1", title_id,)
    cursor.execute(user_unlike_sql, user_unlike_var)
    check_user_name_unlike = cursor.fetchall()

    if len(check_user_name_unlike) is 0:
        sql = 'INSERT INTO reactions(username, title, reaction, title_id) VALUES (%s,%s,%s,%s)'
        val = (username_session, title, '-1', title_id)
        cursor.execute(sql, val)
        con.commit()
        return redirect(url_for('home', page=page))
    elif len(check_user_name_unlike) is 1:
        return redirect(url_for('home', page=page))
    elif len(check_user_name_like) is 1:
        reactsql = 'update reactions set reaction = "-1" where username = "' + username_session + '"'
        cursor.execute(reactsql)
        return redirect(url_for('home', page=page))


@app.route('/article/edit/<title_id>')
def edit(title_id):
    username_session = escape(session['username']).capitalize()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM articles WHERE id = '" + title_id + "'")
    article = cursor.fetchone()
    return render_template('editArticle.html', article=article)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run()
