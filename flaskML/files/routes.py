from files import app
from files.modules import VideoCamera,Faces,Person
from flask import render_template,Response,redirect,url_for,flash, get_flashed_messages,request
from files.forms import RegisterForm,LoginForm,AddForm
from files import db
from flask_login import login_user,logout_user,login_required,current_user
import cv2 as cv


@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods=['GET','POST'])
@login_required
def market_page():

    faces = Faces.query.filter_by(owner=current_user.id)

    return render_template('market.html',faces=faces)

@app.route('/Face_recognition',methods=['GET','POST'])
def video():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')  

@app.route('/Face_id',methods=['GET','POST'])
def GenVideo():
    return render_template('video.html')

def gen(Face):
    while True:
        frame = Face.Face_Rec()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/register',methods = ['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Person(username = form.username.data,
                                email_address = form.email_address.data,
                                password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')
    return render_template('register.html',form = form)

@app.route('/login',methods=['GET','POST'])
def login_page():
    if current_user.is_authenticated==True:
        return redirect(url_for('market_page'))
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = Person.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You logged in as: {attempted_user.username}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and Password are not a match! Please try again',category='danger')

    return render_template('login.html',form = form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!",category='info')
    return redirect(url_for('home_page'))

@app.route('/add',methods=['GET','POST'])
def add_page():
    form = AddForm()
    if form.validate_on_submit():
        user_to_create = Faces(name = form.name.data,
                                roll_no = form.rollNo.data,
                                owner = current_user.id)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with adding a person: {err_msg}',category='danger')

    return render_template('add.html',form = form)