import requests
from bs4 import BeautifulSoup
import sys
# Sugar Mountain Ski Resort
# Gets Conditions from the main page
def getSoup(): 
    print("suagr getSoup")
    sys.stdout.flush()

    sugarWPResponse = requests.get('http://www.skisugar.com/')
    sugarWP = sugarWPResponse.content
    return BeautifulSoup(sugarWP, 'html.parser')
    


def get_conditions_dict(): 
    print("sugar getCond")
    sys.stdout.flush()
    # Is there a way to add this to a dictionary without involving a list? 
    sugarSoup = getSoup()
    if sugarSoup.find('table', class_ = "smrcctable").find('td').get_text() == 'SNOWMAKING IN PROGRESS':
        sugar_conditions_list = []
        for index, i in  enumerate(sugarSoup.find('table', class_ = "smrcctable").find_all('td')):
            if index == 0 and i.get_text() == 'SNOWMAKING IN PROGRESS':
                sugar_conditions_list.append('SNOWMAKING')
                sugar_conditions_list.append('IN PROGRESS') 
            else:
                sugar_conditions_list.append(i.get_text(strip = True).replace('(MAP)', ""))
    else:
        sugar_conditions_list = [i.get_text(strip = True).replace('(MAP)', "") for i in sugarSoup.find('table', class_ = "smrcctable").find_all('td')[:-2]]
        sugar_conditions_list.append('SNOWMAKING')
        sugar_conditions_list.append('NOT IN PROGRESS')
    sugar_conditions_dict = {sugar_conditions_list[i]: 
                            sugar_conditions_list[i+1] 
                            for i in range(0, len(sugar_conditions_list), 2)} 
            
    return sugar_conditions_dict


# Trail and Lift status from the trailmap webpage
def getSoup_sugartrailmap():
    sugarWPResponse = requests.get('http://www.skisugar.com/trailmap/')
    sugarWP = sugarWPResponse.content
    sugarSoup = BeautifulSoup(sugarWP, 'html.parser')
    return sugarSoup.find_all('p', attrs= {'style':"line-height: 18px;"})
    

def get_lift_dict():
    print("sugar getLift")
    sys.stdout.flush()
    sugarTags = getSoup_sugartrailmap()
    # Gets Lifts. Had to use next_sibling instead of get_text()
    # Note: .get('alt') might not be accurate. May need to switch to .get('src')
    return {i.next_sibling.strip(): i.get('alt') for i in sugarTags[0].find_all('img')}


def get_slope_dict():
    print("sugar getSlope")
    sys.stdout.flush()
    sugarTags = getSoup_sugartrailmap()
    # Get Black Diamond Runs. These all used .get_text(), so I grouped them together. 
    # Odd indexes were skipped, as they were just labels
    sugar_BlackDiamond_TagList = [sugarTags[2], sugarTags[4], sugarTags[6]]
    sugar_slope_dict = {}
    # Having trouble getting the tag text. Was combining two runs.
    for i in sugar_BlackDiamond_TagList:
        for j in i.find_all('img'):
            if j.get_text(strip = True) == 'Tom TerrificBoulderdash':
                sugar_slope_dict['Tom Terrific'] = j.get('alt')
            elif j.get_text(strip = True) == '':
                sugar_slope_dict['Boulderdash'] = j.get('alt')
            else:
                sugar_slope_dict[j.get_text(strip = True)] = j.get('alt')    

    # Combine Blue and Green Runs since they all used sibling to get the text.
    # Both tag lists were skipping the first 'next_sibling' so an if statement was added
    sugar_BlueGreen_TagList = [sugarTags[8], sugarTags[10]]
    for i in sugar_BlueGreen_TagList:
        count = 0
        for j in i.find_all('img'):
            if count == 0:
                sugar_slope_dict[j.find('br').previous_sibling.strip()] = j.get('alt')
                count += 1
            else:
                sugar_slope_dict[j.next_sibling.strip()] = j.get('alt')
    return sugar_slope_dict


def print_lift_status():
    print('Ski Sugar Lift Status:')
    for key, val in get_lift_dict().items():
        print(key + ': ' + val)


def print_slope_status():
    print('Ski Sugar Slope Status')
    for key, val in get_slope_dict().items():
        print(key + ': ' + val)


def print_conditions():
    print('Sugar Ski Resort Current Conditions')
    holder = get_conditions_dict()
    for key, val in holder.items():
        print(key + ': ' + val) 


def combine_dictionaries():
    return {'Ski Sugar Conditons': get_conditions_dict(), 
            'Ski Sugar Lifts': get_lift_dict(), 
            'Ski Sugar Slopes': get_slope_dict()}


def all_dicts_with_lists():
    return{ "Ski Sugar Conditions Name": list(get_conditions_dict().keys()),
            "Ski Sugar Conditions Status": list(get_conditions_dict().values()),
            "Ski Sugar Slope Name": list(get_slope_dict().keys()),
            "Ski Sugar Slope Status": list(get_slope_dict().values()),
            "Ski Sugar Lift Name": list(get_lift_dict().keys()),
            "Ski Sugar Lift Status": list(get_lift_dict().values())}