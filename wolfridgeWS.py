from bs4 import BeautifulSoup
import requests
import sys


class Wolf():


    def __init__(self):
        self.conditons_dict = {}
        self.slope_dict = {}
        self.lift_dict = {}


    def add_lift(self, wolfSoup):
        wr_lifts_table = wolfSoup.find('table', attrs= {'id':'tablepress-8'}).find_all('tr')
        self.lift_dict = {row.find('td', class_='column-2').text: 
                row.find('td', class_='column-3').text.title() 
                for row in wr_lifts_table}


    def add_slope(self, wolfSoup):
        wr_slopes_table = wolfSoup.find('table', attrs= {'id':'tablepress-9'}).find_all('tr') 
        self.slope_dict = {row.find('td', class_ = 'column-3').get_text(): 
                row.find('td', class_ = 'column-4').get_text().title() 
                for row in wr_slopes_table[2:]}


    def add_conditions(self, wolfSoup):
        wr_conditions_table = wolfSoup.find('table', attrs= {'id':'tablepress-9'}).find_all('tr')
        self.conditons_dict = {("New Snow"  if row.find('td', class_ = 'column-1').get_text() == 'Natural Snow (Past 24hrs):' 
                                else row.find('td', class_ = 'column-1').get_text(strip = True).replace(':', '')): row.find('td', class_ = 'column-2').get_text().title() 
                                for row in wr_conditions_table}

        self.conditons_dict = {k: 'N/A' if not v else v for k, v in wr_conditions_dict.items()}    

        if self.conditons_dict['New Snow'] == '0':
            self.conditons_dict['New Snow'] += '"'
        
        self.conditons_dict['Snowmaking'] = 'On' if self.conditons_dict['Snowmaking'] == 'Yes' else 'Off'
        self.conditons_dict['Night Skiing'] = 'Open' if self.conditons_dict['Night Skiing'] == 'Yes' else 'Closed'
        
        
    
    def update(self):
        headers = {'User-Agent': 'Mozilla/5.0'}
        wolfWPResponse = requests.get('https://skiwolfridgenc.com/the-mountain/snow-report', headers=headers)
        wolfWP = wolfWPResponse.content
        wolfSoup = BeautifulSoup(wolfWP, 'html.parser')
        
        self.add_conditions(wolfSoup)
        self.add_slope(wolfSoup)
        self.add_lift(wolfSoup)
    
    
    def get_conditions(self):
        return self.conditons_dict
    

    def get_slope(self):
        return self.slope_dict
    

    def get_lift(self):
        return self.lift_dict

    def print_lift_status(self):
        print('Wolf Ridge Ski Resort Lift Status')
        for key, val in self.lift_dict.items():
            print(key + ': ' + val)        


    def print_slope_status(self):
        print('Wolf Ridge Ski Resort Slope Status')
        for key, val in self.slope_dict.items():
            print(key + ': ' + val) 


    def print_conditions(self):
        print('Wolf Ridge Ski Resort Current Conditions')
        for key, val in self.conditons_dict.items():
            print(key + ': ' + val) 


    def combine_dictionaries(self):
        return {'Wolf Ridge Ski Resort Conditons': self.conditons_dict, 
                'Wolf Ridge Ski Resort Lifts': self.lift_dict,
                'Wolf Ridge Ski Resort Slopes': self.slope_dict}


    def all_dicts_with_lists(self):
        return{ "Wolf Ridge Conditions Name": list(self.conditons_dict.keys()),
                "Wolf Ridge Conditions Status": list(self.conditons_dict.values()),
                "Wolf Ridge Slope Name": list(self.slope_dict.keys()),
                "Wolf Ridge Slope Status": list(self.slope_dict.values()),
                "Wolf Ridge Lift Name": list(self.lift_dict.keys()),
                "Wolf Ridge Lift Status": list(self.lift_dict.values())}