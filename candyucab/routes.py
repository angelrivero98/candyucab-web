from flask import render_template,url_for,flash,redirect,request
from candyucab.forms import RegistrationForm,LoginForm
from candyucab import app,bcrypt
from candyucab.user import User
import psycopg2
from candyucab.db import Database
from flask_login import login_user,current_user,logout_user,login_required

@app.route("/")
@app.route("/home")
def home():
   return render_template('home.html')

@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        db = Database()
        cur = db.cursor_dict()
        try:
            cur.execute("""INSERT INTO public.user (username, email, password)
            VALUES (%s, %s, %s);""",
            (form.username.data, form.email.data, hashed_pw))
        except:
            print("ERROR inserting into user")
            print("Tried: INSERT INTO user (username, email, password) VALUES ('%s', '%s', %s);" %
            (form.username.data, form.email.data, hashed_pw) )
            db.retroceder()
        db.actualizar()

        flash('Your account have been created','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        db = Database()
        cur = db.cursor_dict()
        cur.execute("SELECT * from public.user WHERE username = %s;",(form.username.data,))
        user = User(cur.fetchone())
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful','danger')
    return render_template('login.html',title='Login',form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

#@app.route("/account")
#@login_required
#def account():
#    return render_template('account.html',title='Account')
