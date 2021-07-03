from flask import Blueprint
from flask import render_template,redirect,url_for,flash,Response,request,session
from project import app
from project.models import user
from project.users.forms import registrationform,loginform
from project import db
from flask_login import login_user,logout_user
from project.my_functions import Camera


users=Blueprint('users',__name__)

@users.route('/register',methods=["GET","POST"])
def register_page():
    form = registrationform()
    if form.validate_on_submit():
        user_to_create=user(username=form.username.data,
                            email_address=form.email_address.data,
                            phone_number=form.phone_number.data,
                            password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'successfull created account and logged in as  : {form.username.data}', category='success')
        return redirect(url_for('users.face_register'))
    if form.errors != {}:  # if there are not errors from validation
        for err_msg in form.errors.values():
            flash(f'There was an error creating a user : {err_msg}',category='danger')
    return render_template("register.html",form=form)

@users.route('/login',methods=["GET","POST"])
def login_page():
    form=loginform()
    if form.validate_on_submit():
        attempted_user=user.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data):

            login_user(attempted_user)
            flash(f'Success ! you are logged in as : {attempted_user.username}',category='success')
            return redirect(url_for('events_bp.event_page'))
        else:
            flash("Username and password are not match! Please Try Again",category='danger')
    return render_template('login.html', form=form)


@users.route('/logout',methods=["GET","POST"])
def logout_page():
    logout_user()
    session.clear()
    flash("You have been logged out ! ",category="info")
    return redirect(url_for('main.home_page'))





@users.route("/face_recognition_check",methods=["GET",'POST'])
def face_recognition_check():
    start_face_recognition = False
    if request.method=='POST':
        if request.form.get('face_recognition_action')=='start_recognition':
            start_face_recognition=True
        elif request.form.get('face_recognition_action')=='stop_recognition':
            start_face_recognition=False
    return render_template('face_recognition_check.html',start_face_recognition=start_face_recognition)



@users.route('/face_register',methods=["GET","POST"])
def face_register():
    start_face_register='false'
    if request.method == 'POST':
        if request.form.get('register face') == 'register_face':
            start_face_register='true'

    return render_template("face_register.html",start_face_register=start_face_register)


@users.route('/recognise_faces/<start_face_recognition>',methods=["GET","POST"])
def recognise_faces(start_face_recognition):
    return Response(Camera.face_recogniser(start_face_recognition),mimetype='multipart/x-mixed-replace; boundary=frame')

@users.route('/register_face/<name>',methods=["GET","POST"])
def register_face(name):
    return Response(Camera.register_face(person_name=name),mimetype='multipart/x-mixed-replace; boundary=frame')


@users.route('/face_login2/',methods=["GET","POST"])
def face_login2():
    name = Camera.face_recogniser_get_name()
    if name =='unknown':
        flash(f"no faces detected or recognised ,please try again later", category='danger')
    else:
        attempted_user = user.query.filter_by(username=name).first()

        try:

            login_user(attempted_user)
            flash(f'Success ! you are logged in as : {attempted_user.username}', category='success')
        except :
            flash(f"no user named {name} found in data base",category='danger')
    return redirect(url_for('events_bp.event_page'))


@users.route('/face_login_check',methods=["GET","POST"])
def face_login3():
    logined_user=''
    start_video='start'
    if request.method == 'POST':
        if request.form.get('start') == 'start':
            name = Camera.face_recogniser_get_name()
            if name == 'unknown':
                flash(f"no faces detected or recognised ,please try again later", category='danger')
            else:
                attempted_user = user.query.filter_by(username=name).first()
                try:
                    login_user(attempted_user)
                    flash(f'Success ! you are logged in as : {attempted_user.username}', category='success')
                    start_video = 'stop'
                    logined_user=attempted_user.username
                    return redirect(url_for('events_bp.event_page'))
                except:
                    flash(f"no user named {name} found in data base", category='danger')
        elif request.form.get('start') == 'stop':
            start_video = 'stop'

    return render_template('face_login3.html',start_video=start_video,user=logined_user)

@users.route('/stream_video/<start_stream_video>',methods=["GET","POST"])
def stream_video(start_stream_video):
    if start_stream_video=='start_stream_video':
        camera_status = 'open_camera'
    else:
        camera_status = 'release_camera'
    return Response(Camera.gen_frames(camera_status),mimetype='multipart/x-mixed-replace; boundary=frame')