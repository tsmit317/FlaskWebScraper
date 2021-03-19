import requests
from bs4 import BeautifulSoup
import sys

#App Ski Mtn
def getSoup():
    print("app getSoup")
    sys.stdout.flush()
    appWPResponse = requests.get('https://www.appskimtn.com/slope-report')
    appWP = appWPResponse.content
    asoup = BeautifulSoup(appWP, 'html.parser')
    return asoup

appSoup = getSoup()

def get_conditions_dict():
    print("app getCond")
    sys.stdout.flush()

    conditons_dict = {}            
    for index, i in enumerate(getSoup().find_all('ul', class_ = 'slope-report__details')):
        for j in i.find_all('li'):
            if index == 0:
                conditons_dict['Temp ' + j.find('span', class_ = 'slope-report__details-label').get_text()] = j.find('span', class_ = 'slope-report__details-value').get_text()
            elif index == 1:
                if j.find('span', class_ = 'slope-report__details-value'):
                    conditons_dict['Snowmaking ' + j.find('span', class_ = 'slope-report__details-label').get_text()] = j.find('span', class_ = 'slope-report__details-value').get_text()
                else:
                    conditons_dict['Snowmaking ' + j.find('span', class_ = 'slope-report__details-label').get_text()] = j.find('span', class_ = 'slope-report__details-plain-text').get_text()
            elif index == 2 or index == 3:
                if j.find('span', class_ = 'slope-report__details-value'):            
                    conditons_dict[j.find('span', class_ = 'slope-report__details-label').get_text()] = j.find('span', class_ = 'slope-report__details-value').get_text()
                else:
                    conditons_dict['Road Details'] = j.find('span', class_ = 'slope-report__details-plain-text').get_text()
       
    if conditons_dict['New Snow']  == '':
        conditons_dict['New Snow'] = 'N/A'     
    return conditons_dict


def get_slope_dict():
    print("app getSlope")
    sys.stdout.flush()
    appSlopeUL = getSoup().find_all('ul', class_ = 'slope-report__status')
    return {i.find('span', class_ = 'slope-report__status-title').get_text():
            i.find('span', class_ = 'slope-report__status-status').get_text()
            for i in appSlopeUL[0].find_all('li')}
  

def get_lift_dict(): 
    print("app getLift")
    sys.stdout.flush() 
    appSlopeUL = getSoup().find_all('ul', class_ = 'slope-report__status')
    return {i.find('span', class_ = 'slope-report__status-title').get_text():
            i.find('span', class_ = 'slope-report__status-status').get_text()
            for i in appSlopeUL[1].find_all('li')}
              
def print_lift_status():
    print('Appalachain Ski Mtn Lift Status: ')
    for key, val in get_lift_dict().items():
        print(key + ': ' + val)
   

def print_conditions():
    print('Appalachain Ski Mtn Conditions: ')
    for key, val in get_conditions_dict().items():
        print(key + ': ' + val)


def print_slope_status():
    print('Appalachain Ski Mtn Slope Status: ')
    for key, val in get_slope_dict().items():
        print(key + ': ' + val)


def combine_dictionaries():
    return {'Appalachain Ski Mtn Conditions': get_conditions_dict(), 'Appalachain Ski Mtn Lifts': get_lift_dict(), 'Appalachain Ski Mtn Slopes': get_slope_dict()}


def all_dicts_with_lists():
    return {'Appalachain Ski Mtn Conditions Name': list(get_conditions_dict().keys()), 
            'Appalachain Ski Mtn Conditons Status': list(get_conditions_dict().values()),
            'Appalachain Ski Mtn Slope Name': list(get_slope_dict().keys()), 
            'Appalachain Ski Mtn Slope Status': list(get_slope_dict().values()),
            'Appalachain Ski Mtn Lift Name': list(get_lift_dict().keys()),
            'Appalachain Ski Mtn Lift Status': list(get_lift_dict().values())}
