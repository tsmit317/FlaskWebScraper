import requests
from bs4 import BeautifulSoup


#WolfRidge Ski Resort
def getSoup():
    wolfWPResponse = requests.get('https://skiwolfridgenc.com/the-mountain/snow-report')
    wolfWP = wolfWPResponse.content
    wSoup = BeautifulSoup(wolfWP, 'html.parser')
    return wSoup

wolfSoup = getSoup()
def get_lift_dict():
    # wolfSoup = getSoup()
    wr_lifts_table = wolfSoup.find('table', attrs= {'id':'tablepress-8'}).find_all('tr')
    return {row.find('td', class_='column-2').text: 
            row.find('td', class_='column-3').text 
            for row in wr_lifts_table}


def get_slope_dict():
    # wolfSoup = getSoup()
    wr_slopes_table = wolfSoup.find('table', attrs= {'id':'tablepress-9'}).find_all('tr') 
    return {row.find('td', class_ = 'column-3').get_text(): 
            row.find('td', class_ = 'column-4').get_text() 
            for row in wr_slopes_table[2:]}


def get_conditions_dict():
    # wolfSoup = getSoup()
    wr_conditions_table = wolfSoup.find('table', attrs= {'id':'tablepress-7'}).find_all('tr')
    wr_conditions_dict = {row.find('td', class_ = 'column-1').get_text():
                          row.find('td', class_ = 'column-2').get_text() 
                          for row in wr_conditions_table}
    wr_conditions_dict = {k: 'N/A' if not v else v for k, v in wr_conditions_dict.items()}                       
    return wr_conditions_dict


def print_lift_status():
    print('Wolf Ridge Ski Resort Lift Status')
    for key, val in get_lift_dict().items():
        print(key + ': ' + val)        


def print_slope_status():
    print('Wolf Ridge Ski Resort Slope Status')
    for key, val in get_slope_dict().items():
        print(key + ': ' + val) 


def print_conditions():
    print('Wolf Ridge Ski Resort Current Conditions')
    for key, val in get_conditions_dict().items():
        print(key + ': ' + val) 


def combine_dictionaries():
    return {'Wolf Ridge Ski Resort Conditons': get_conditions_dict(), 
            'Wolf Ridge Ski Resort Lifts': get_lift_dict(),
            'Wolf Ridge Ski Resort Slopes': get_slope_dict()}


def all_dicts_with_lists():
    return{ "Wolf Ridge Conditions Name": list(get_conditions_dict().keys()),
            "Wolf Ridge Conditions Status": list(get_conditions_dict().values()),
            "Wolf Ridge Slope Name": list(get_slope_dict().keys()),
            "Wolf Ridge Slope Status": list(get_slope_dict().values()),
            "Wolf Ridge Lift Name": list(get_lift_dict().keys()),
            "Wolf Ridge Lift Status": list(get_lift_dict().values())}
        
