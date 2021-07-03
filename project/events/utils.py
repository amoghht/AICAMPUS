from project.utils import *
import secrets
import os
from project import app


def get_all_sub_categories(event_caterogies):
    all_sub_categories_list=[]
    for key in event_caterogies.keys():
        for sub_category in event_caterogies[key]:
            all_sub_categories_list.append(sub_category)
    return all_sub_categories_list



def get_main_category(event_caterogies,user_intrest_category):
    main_category = []
    for key in event_caterogies.keys():
        for category in event_caterogies[key]:
            if category in user_intrest_category:
                main_category.append(key)
    return main_category

def get_recommendation_list(event_caterogies,main_category_list):
    recommendation_list = []
    for main_cat in main_category_list:
        recommendation_list.extend(event_caterogies[main_cat])
    return recommendation_list


def add_event_category(sub_category,category):
    pkl_path = 'project/data/events_category/events_category.pkl'
    event_caterogies = load_pickle(pkl_path)
    if category in event_caterogies.keys():
        for key in event_caterogies.keys():
            if key==category:
                lst = event_caterogies[key]
                if sub_category not in lst:
                    lst.append(sub_category)
                    event_caterogies[key] = lst
    else:
        empty_list=[]
        empty_list.append(sub_category)
        event_caterogies[category]=empty_list
    with open(pkl_path, 'bw') as file:
        pickle.dump(event_caterogies, file)


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,file_ext=os.path.splitext(form_picture.filename)
    picture_name=random_hex+file_ext
    picture_path=os.path.join(app.root_path,'static/images/events',picture_name)
    form_picture.save(picture_path)
    return picture_name


def delete_old_picture(filename):
    file_path=os.path.join(app.root_path,'static/images/events',filename)
    if os.path.exists(file_path):
        os.remove(path=file_path)
        return True
    else:
        return False

event_caterogies = {

        'artificial intellegence': ['AI', 'ML', 'DL', 'CV', 'NLP','ROBOTICS'],
        'vlsi': ['FE', 'BE', 'RF', 'LAYOUTS', 'DIGITAL', 'ANALOG','VLSI'],
        'embedded': ['ARM', 'DRONE', 'ATMEGA', 'EMBEDDED_SYSTEMS','ROBOTICS'],
        'web': ['FRONT_END', 'BACK END', 'FULL_STACK', 'NODE.JS', 'ANJULAR_JS', 'HTML', 'CSS'],
        'vidyuth': ['DANCING', 'SINGING', 'DRAMA', 'LOGO_DESIGN','VIDYUTH','TARANGA'],

    }