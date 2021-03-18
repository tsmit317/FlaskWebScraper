import requests
from bs4 import BeautifulSoup
import sys

# Ski Beech
def getSoup():
    print('inside beech getSoup')
    sys.stdout.flush()
    beechWPResponse = requests.get('https://www.beechmountainresort.com/mountain/winter-trail-map/')
    beechWP = beechWPResponse.content
    bsoup =  BeautifulSoup(beechWP, "html.parser")
    return bsoup

beechSoup = getSoup()

def get_lift_dict():
    beech_sl_tag = beechSoup.find_all('td')
    return {beech_sl_tag[i].text: 
            beech_sl_tag[i+1].text 
            for i in range(0, 15, 2)}

def get_slope_dict():
    beech_sl_tag = beechSoup.find_all('td')
    return {beech_sl_tag[i].get_text(strip = True): 
                beech_sl_tag[i+1].get_text(strip = True) 
                for i in range(16, len(beech_sl_tag), 2)}
    
def get_conditions_dict():
    beechConditionsTags = beechSoup.find('div', class_ = 'overview').find_all('div')
    return {i.find('span').get_text(): 
            str(i.find(text=True, recursive=False)).replace('\n\t\t\t', '').replace('\t\t\t','').replace('\n', 'N/A') 
            for i in beechConditionsTags}

def print_lift_status():
    print('Ski Beech Lift Status')
    for key, val in get_lift_dict().items():
        print(key + ': ' + val)

def print_slope_status():
    print('Ski Beech Slope Status')
    for key, val in get_slope_dict().items():
        print(key + ': ' + val)

def print_conditions():
    print('Ski Beech Current Conditions')
    for key, val in get_conditions_dict().items():
        print(key + ': ' + val) 

def combine_dictionaries():
    return {'Ski Beech Conditons': get_conditions_dict(), 'Ski Beech Lifts': get_lift_dict(), 'Ski Beech Slopes': get_slope_dict()}


def all_dicts_with_lists():
    return{'Ski Beech Condition Name': list(get_conditions_dict().keys()),
           'Ski Beech Condition Status': list(get_conditions_dict().values()),
           'Ski Beech Slope Name': list(get_slope_dict().keys()),
           'Ski Beech Slope Status': list(get_slope_dict().values()),
           'Ski Beech Lift Name': list(get_lift_dict().keys()),
           'Ski Beech Lift Status': list(get_lift_dict().values())}