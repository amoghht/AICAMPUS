from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,URL
from flask_wtf.file import FileAllowed,FileField
from project.utils import *



class addeventsform(FlaskForm):
    def get_all_main_category(dct):
        all_main_category = []
        for key in dct.keys():
            all_main_category.append(key)
        return all_main_category

    def prepare_choices_main_category(event_dictionary):
        lst = []
        for categ in event_dictionary:
            tup = (categ, categ)
            lst.append(tup)
        return lst

    def prepare_choices_sub_category(event_dictionary):
        lst = []
        for categ in event_dictionary:
            for subcat in event_dictionary[categ]:
                lst.append((subcat,subcat))
        return lst


    def return_event_category_pkl():
        pkl_path = 'project/data/events_category/events_category.pkl'
        return load_pickle(pkl_path)

    eventname=StringField(label='event name',validators=[DataRequired()])
    event_main_category = SelectField(label='event main category',choices=prepare_choices_main_category(return_event_category_pkl()))
    eventcategory=SelectField(label='event category',choices=prepare_choices_sub_category(return_event_category_pkl()))
    event_date=StringField('event date')
    event_description=StringField(label='event description',validators=[DataRequired()])
    image_file=FileField(label='event poster',validators=[FileAllowed(['jpg','png'])])
    register_link = StringField(label='registration link',validators=[URL()])
    submit = SubmitField(label='Add Event')


class modifyeventsform(FlaskForm):
    def get_all_main_category(dct):
        all_main_category = []
        for key in dct.keys():
            all_main_category.append(key)
        return all_main_category

    def prepare_choices_main_category(event_dictionary):
        lst = []
        for categ in event_dictionary:
            tup = (categ, categ)
            lst.append(tup)
        return lst

    def prepare_choices_sub_category(event_dictionary):
        lst = []
        for categ in event_dictionary:
            for subcat in event_dictionary[categ]:
                lst.append((subcat,subcat))
        return lst


    def return_event_category_pkl():
        pkl_path = 'project/data/events_category/events_category.pkl'
        return load_pickle(pkl_path)

    eventname=StringField(label='event name',validators=[DataRequired()])
    eventcategory=SelectField(label='event category',choices=prepare_choices_sub_category(return_event_category_pkl()))
    event_date=StringField('event date')
    event_description=StringField(label='event description',validators=[DataRequired()])
    image_file=FileField(label='event poster',validators=[FileAllowed(['jpg','png'])])
    register_link = StringField(label='registration link',validators=[URL()])
    submit = SubmitField(label='modify Event')