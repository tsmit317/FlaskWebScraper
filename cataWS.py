import requests
from bs4 import BeautifulSoup


#Cataloochee Ski Resort
def getSoup():
    cataWPResponse = requests.get('https://cataloochee.com/the-mountain/snow-report/')
    cataWP = cataWPResponse.content
    cSoup = BeautifulSoup(cataWP, 'html.parser')
    return cSoup

cataSoup = getSoup()

def get_conditions_dict():
    # Get tags containing conditions
    cata_conditons = cataSoup.find_all('div', class_ = 'snow-report-overview')[1]
    cata_conditions_list = []
    # Not all tags contained text. Some contained images of check marks, so I had to loop through and check.
    for i in cata_conditons:
        if i.find('i') and i.find('i', class_='fas fa-check'):
            cata_conditions_list.append('Yes')
        elif i.find('i') and (not i.find('i', class_='fas fa-check')):
            cata_conditions_list.append('No')
        else:
            cata_conditions_list.append(i.get_text())
    return {cata_conditions_list[i+1]: cata_conditions_list[i] for i in range(0, len(cata_conditions_list), 2)} 

def get_slope_dict():
    cata_trail_columns =[i.get_text(strip = True) for i in cataSoup.find('table', class_='trails-table').find_all('td')]
    return {cata_trail_columns[i]: cata_trail_columns[i + 1] for i in range(0, len(cata_trail_columns), 2)}
   

def get_lift_dict():
    cata_lifts_columns = [i.get_text(strip = True) for i in cataSoup.find('table', class_='lifts-table').find_all('td')]
    return {cata_lifts_columns[i]: cata_lifts_columns[i + 1] for i in range(0, len(cata_lifts_columns), 2)}
 

def print_slope_status():
    print('Cataloochee Ski Area Slope Status')
    for key, val in get_slope_dict().items():
        print(key + ': ' + val)


def print_lift_status():
    print('Cataloochee Ski Area Lift Status')
    for key, val in get_lift_dict().items():
        print(key + ': ' + val)


def print_conditions():
    print('Cataloochee Ski Area Current Conditions')
    for key, val in get_conditions_dict().items():
        print(key + ': ' + val)


def combine_dictionaries():
    return {'Cataloochee Ski Area Conditons': get_conditions_dict(), 
            'Cataloochee Ski Area Lifts': get_lift_dict(),
            'Cataloochee Ski Area Slopes': get_slope_dict()}


def all_dicts_with_lists():
    return{"Cataloochee Ski Area Conditions Name": list(get_conditions_dict().keys()),
           "Cataloochee Ski Area Conditions Status": list(get_conditions_dict().values()),
           "Cataloochee Ski Area Slope Name": list(get_slope_dict().keys()),
           "Cataloochee Ski Area Slope Status": list(get_slope_dict().values()),
           "Cataloochee Ski Area Lift Name": list(get_lift_dict().keys()),
           "Cataloochee Ski Area Lift Status": list(get_lift_dict().values())}