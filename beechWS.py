import requests
from bs4 import BeautifulSoup
import sys

class Beech():

    def __init__(self):
        self.conditons_dict = {}
        self.slope_dict = {}
        self.lift_dict = {}
    

    def add_lift(self, beechSoup):
        print("beechWS: add_lift()")
        sys.stdout.flush()

        beech_sl_tag = beechSoup.find_all('td')
        return {beech_sl_tag[i].text: 
                beech_sl_tag[i+1].text 
                for i in range(0, 15, 2)}


    def add_slope(self, beechSoup):
        print("beechWS: add_slope()")
        sys.stdout.flush()

        beech_sl_tag = beechSoup.find_all('td')
        return {beech_sl_tag[i].get_text(strip = True): 
                    beech_sl_tag[i+1].get_text(strip = True) 
                    for i in range(16, len(beech_sl_tag), 2)}
        

    def add_conditions(self, beechSoup):
        print("beechWS: add_conditions()")
        sys.stdout.flush()
        
        beechConditionsTags = beechSoup.find('div', class_ = 'overview').find_all('div')
        return {i.find('span').get_text(): 
                str(i.find(text=True, recursive=False)).replace('\n\t\t\t', '').replace('\t\t\t','').replace('\n', 'N/A') 
                for i in beechConditionsTags}


    def update(self):
        print("beechWS: update()")
        sys.stdout.flush()

        beechWPResponse = requests.get('https://www.beechmountainresort.com/mountain/winter-trail-map/')
        beechWP = beechWPResponse.content
        beechSoup = BeautifulSoup(beechWP, "html.parser")

        self.conditons_dict = self.add_conditions(beechSoup)
        self.slope_dict = self.add_slope(beechSoup)
        self.lift_dict = self.add_lift(beechSoup)

    def get_conditions(self):
        return self.conditons_dict
    

    def get_slope(self):
        return self.slope_dict
    

    def get_lift(self):
        return self.lift_dict

        
    def print_lift_status(self):
        print('Ski Beech Lift Status')
        for key, val in self.lift_dict.items():
            print(key + ': ' + val)


    def print_slope_status(self):
        print('Ski Beech Slope Status')
        for key, val in self.slope_dict.items():
            print(key + ': ' + val)


    def print_conditions(self):
        print('Ski Beech Current Conditions')
        for key, val in self.conditons_dict.items():
            print(key + ': ' + val) 


    def combine_dictionaries(self):
        return {'Ski Beech Conditons': self.conditons_dict, 'Ski Beech Lifts': self.lift_dict, 'Ski Beech Slopes': self.slope_dict}


    def all_dicts_with_lists(self):
        return{'Ski Beech Condition Name': list(self.conditons_dict.keys()),
            'Ski Beech Condition Status': list(self.conditons_dict.values()),
            'Ski Beech Slope Name': list(self.slope_dict.keys()),
            'Ski Beech Slope Status': list(self.slope_dict.values()),
            'Ski Beech Lift Name': list(self.lift_dict.keys()),
            'Ski Beech Lift Status': list(self.lift_dict.values())}