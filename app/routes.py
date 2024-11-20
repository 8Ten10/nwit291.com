from flask import render_template, request, redirect, url_for, flash, session
from app import app, mysql
from app.models import hash_password

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        password = hash_password(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, address, email, password) VALUES (%s, %s, %s, %s, %s)", (first_name, last_name, address, email, password))
        mysql.connection.commit()
        cur.close()

        session['user'] = first_name
        return redirect(url_for('thank_you'))
    return render_template('register.html')

@app.route('/thank_you', methods=['GET', 'POST'])
def thank_you():
    if request.method == 'POST':
        choice = request.form['choice']
        if choice == 'yes':
            return redirect(url_for('login'))
        else:
            return redirect(url_for('index'))
    return render_template('thank_you.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = hash_password(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            session['user'] = user[1]  # Assuming first_name is the second column
            return redirect(url_for('user_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/user_page')
def user_page():
    if 'user' in session:
        return render_template('user_page.html', user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')
