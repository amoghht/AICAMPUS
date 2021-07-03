from flask import Blueprint
from flask import render_template,redirect,url_for,flash,request,abort
from project.models import user,events
from project.events.forms import addeventsform,modifyeventsform
from project import db
from flask_login import login_required,current_user
from project.utils import *
from project.events.utils import (get_all_sub_categories, get_main_category, get_recommendation_list,
                                  event_caterogies, save_picture, delete_old_picture, add_event_category)



events_bp=Blueprint('events_bp',__name__)







@events_bp.route('/myintrests/<int:user_id>',methods=["GET" , "POST"])
@login_required
def myintrests(user_id):
    thisuser = user.query.filter_by(id=user_id).first()  #get user details by user id
    #all_events=events.query.all()                        #query all the events in db
    all_categories=[]
    for event in get_all_sub_categories(event_caterogies=event_caterogies):
        if event not in all_categories:
            all_categories.append(event)   #list of all the categories of events present in database
    intrests_pkl_path='project/data/intrests/intrests.pkl'
    intrests_pkl_dict = load_pickle(intrests_pkl_path)  # dictinary of intrests list of all the registered people
    if request.method=='POST':
        my_intrest_list=request.form.getlist('intrests')
        intrests_pkl_dict[thisuser.username]=my_intrest_list
        save_pickle(intrests_pkl_path,intrests_pkl_dict)       #update intrest list of this user
        flash(f'your intrest list : {my_intrest_list} is added successfully ', category='success')
    return render_template("myintrests.html",thisuser=thisuser,mydict=intrests_pkl_dict,categories=all_categories)





@events_bp.route('/events')
@login_required
def event_page():
    recommended_events=[]
    rest_of_events=[]
    events_list = events.query.all()     #query all the events in db
    intrests_pkl_path = 'project/data/intrests/intrests.pkl'
    intrests_pkl_dict = load_pickle(intrests_pkl_path)
    try:
        current_user_intrests = intrests_pkl_dict[current_user.username]
        current_user_intrests_list = get_recommendation_list(event_caterogies,get_main_category(event_caterogies,current_user_intrests))
    except:
        current_user_intrests=recommended_events   #initally intrest list will be empty
        current_user_intrests_list=recommended_events
    for event in events_list:
        if event.eventcategory in current_user_intrests_list:
            recommended_events.append(event)      #recommended event list
        else:
            rest_of_events.append(event)          #rest of the event appart from recommendation
    return render_template("eventsnew.html",events_list=events_list,recommended_events=recommended_events,rest_of_events=rest_of_events,current_user_intrests=current_user_intrests)


@events_bp.route('/add_events',methods=["GET" , "POST"])
@login_required
def add_events():
    pic_file_name='default.jpg'
    link='#'
    form=addeventsform()
    if form.validate_on_submit():
        if form.image_file.data:
            pic_file_name=save_picture(form.image_file.data)
        if form.register_link.data:
            link=form.register_link.data
        add_event_category(form.eventcategory.data,form.event_main_category.data)
        event_to_add = events(eventname=form.eventname.data,
                              eventcategory=form.eventcategory.data,
                              event_date=form.event_date.data,
                              event_description=form.event_description.data,
                              image_file=pic_file_name,
                              register_link=link,
                              user_id=current_user.id)
        db.session.add(event_to_add)
        db.session.commit()
        flash(f'your event named: { form.eventname.data } is added successfully ', category='success')
        return redirect(url_for('events_bp.my_events'))
    if form.errors != {}:  # if there are not errors from validation
        for err_msg in form.errors.values():
            flash(f'There was an error creating a event : {err_msg}',category='danger')
    return render_template("addevents.html",form=form)

@events_bp.route('/my_events')
@login_required
def my_events():
    my_events_list=[]
    events_list = events.query.all()
    for event in events_list:
        if event.user_id==current_user.id:
            my_events_list.append(event)
    return render_template("my_events.html",my_events_list=my_events_list)


@events_bp.route('/modify_event/<int:event_id>',methods=["GET" , "POST"])
@login_required
def modify_event(event_id):
    event = events.query.get_or_404(event_id)
    pic_file_name = event.image_file
    if event.user_id != current_user.id:
        abort(403)
    form = modifyeventsform()
    if form.validate_on_submit():
        if form.image_file.data:
            delete_old_picture(event.image_file)
            pic_file_name=save_picture(form.image_file.data)
        event.eventname=form.eventname.data
        event.eventcategory=form.eventcategory.data
        event.event_date=form.event_date.data
        event.event_description=form.event_description.data
        event.register_link=form.register_link.data
        event.image_file=pic_file_name
        db.session.commit()
        flash('your event details has updated','success')
        return redirect(url_for('events.my_events'))
    elif request.method == 'GET':
        form.eventname.data=event.eventname
        form.eventcategory.data = event.eventcategory
        form.event_date.data = event.event_date
        form.event_description.data = event.event_description
        form.register_link.data = event.register_link
    return render_template("modify_event.html",form=form,event=event)


@events_bp.route('/delete_event/<int:event_id>',methods=["POST"])
@login_required
def delete_event(event_id):
    event = events.query.get_or_404(event_id)
    if event.user_id != current_user.id:
        abort(403)
    delete_old_picture(event.image_file)
    db.session.delete(event)
    db.session.commit()
    flash('your event has deleted', 'success')
    return redirect(url_for('events.my_events'))


@events_bp.route('/events/<int:id>')
def eventdescription(id):
    event=events.query.filter_by(event_id=id).first()
    return render_template("eventdescription.html",event=event)