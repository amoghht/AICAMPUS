import pickle
import os.path



event= {
        'artificial intellegence': ['AI', 'ML', 'DL', 'CV', 'NLP','ROBOTICS'],
        'vlsi': ['FE', 'BE', 'RF', 'LAYOUTS', 'DIGITAL', 'ANALOG','VLSI'],
        'embedded': ['ARM', 'DRONE', 'ATMEGA', 'EMBEDDED_SYSTEMS','ROBOTICS'],
        'web': ['FRONT END', 'BACK END', 'FULL STACK', 'NODE.JS', 'ANJULAR.JS', 'HTML', 'CSS'],
        'vidyuth': ['DANCING', 'SINGING', 'DRAMA', 'LOGO DESIGN','VIDYUTH','TARANGA'],
    }


event_caterogies = {

        'artificial intellegence': ['AI', 'ML', 'DL', 'CV', 'NLP','ROBOTICS'],
        'vlsi': ['FE', 'BE', 'RF', 'LAYOUTS', 'DIGITAL', 'ANALOG','VLSI'],
        'embedded': ['ARM', 'DRONE', 'ATMEGA', 'EMBEDDED_SYSTEMS','ROBOTICS'],
        'web': ['FRONT END', 'BACK END', 'FULL STACK', 'NODE.JS', 'ANJULAR.JS', 'HTML', 'CSS'],
        'vidyuth': ['DANCING', 'SINGING', 'DRAMA', 'LOGO DESIGN','VIDYUTH','TARANGA'],

    }

def get_main_category(event_caterogies, user_intrest_category):
 main_category = []
 for key in event_caterogies.keys():
  for category in event_caterogies[key]:
   if category in user_intrest_category:
    main_category.append(key)
 return main_category


def get_recommendation_list(event_caterogies, main_category_list):
 recommendation_list = []
 for main_cat in main_category_list:
  recommendation_list.extend(event_caterogies[main_cat])
 return recommendation_list



current_user_intrests=['AI']

#current_user_intrests_list = get_recommendation_list(event_caterogies,get_main_category(event_caterogies,current_user_intrests))
#print(current_user_intrests_list)

sub_cat='DNN'
cat='artificial intellegence'

def reture_event_category_pkl():
    pkl_path = 'project/data/events_category/events_category.pkl'
    return load_pickle(pkl_path)

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

def make_event_category_pickle():
    event_caterogies = {

        'artificial intellegence': ['AI', 'ML', 'DL', 'CV', 'NLP', 'ROBOTICS'],
        'vlsi': ['FE', 'BE', 'RF', 'LAYOUTS', 'DIGITAL', 'ANALOG', 'VLSI'],
        'embedded': ['ARM', 'DRONE', 'ATMEGA', 'EMBEDDED_SYSTEMS', 'ROBOTICS'],
        'web': ['FRONT_END', 'BACK_END', 'FULL_STACK', 'NODE.JS', 'ANJULAR_JS', 'HTML', 'CSS'],
        'vidyuth': ['DANCING', 'SINGING', 'DRAMA', 'LOGO_DESIGN', 'VIDYUTH', 'TARANGA'],

    }
    pkl_path = 'project/data/events_category/events_category.pkl'
    if not os.path.isfile(pkl_path):
        with open(pkl_path,'ab') as file:
            pickle.dump(event_caterogies,file)

make_event_category_pickle()
def load_pickle(path):
    with open(path, 'rb') as f:
        encoding_dict = pickle.load(f)
    return encoding_dict


pkl_path = 'project/data/events_category/events_category.pkl'

#dct=load_pickle(pkl_path)

'''
print("------------------------before-----------------------")
for i in dct.keys():
    print(dct[i])


print("------------------------after-----------------------")


#add_event_category(sub_cat,cat)

dct=load_pickle(pkl_path)
for i in dct.keys():
    print(dct[i])'''

def get_all_main_category(dct):
    all_main_category=[]
    for key in dct.keys():
        all_main_category.append(key)
    return all_main_category


#event2=reture_event_category_pkl()
#cate=get_all_main_category(event2)

def prepare_choices_sub_category(event_dictionary):
    lst = []
    for categ in event_dictionary:
        for category in event_dictionary[categ]:
            tup = (category, category)
            lst.append(tup)
    return lst

#print(prepare_choices_sub_category(event2))