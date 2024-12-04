from flask import Flask, flash, redirect,render_template, request, session, url_for
import sqlite3 
from data import init_db
app = Flask(__name__)

@app.route("/")
def index():
if "user" in session:
return render_template('main.html')
else:
flash("ти не увійшов")
return redirect(url_for("login"))

def index():
    return 'Hello'

@app.route("/login")
def login():
    if request.method == 'POST':
        useranme =request.form['useranme']
        password =request.form['password']
        conn = sqlite.connect("users.db")
        cursur = conn.cursor()
        cursor.execute("SELECT * FROM users  WHERE username = ? AND password = ?",
                        (username,password))
        user_data = cursor.fetchone()
        print(user_data)
        conn.close()
        if user_data:
            session['user'] = username
            flash("Вхід успішний", "success")
            redirect('/')
        else:
            flash("Неправильний логін або пароль.", "error")
            return redirect('/login')
    else:
        return render_template("lo")

@app.route("/register")
def register():
    if request.method == 'POST':
        useranme =request.form['useranme']
        password =request.form['password']
        conn = sqlite.connect("users.db")
        cursur = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username,password) VALUE (?,?)", (username, password))
            conn.commit()
            conn.close()
            flash('Ви успішно зареєструвалися!', 'success')
            return redirect('/login')
        exept sqlite3.IntegrityError:
            flash('Користувач с таким іменем вже існує', 'error')
            return resirect('/register')
        return render_template('register.html')
        
app.run()