from bs4 import BeautifulSoup
import requests
import sys

class App():


    def __init__(self):
        self.conditons_dict = {}
        self.slope_dict = {}
        self.lift_dict = {}


    def add_conditions(self, appSoup):
        conditons_dict = {}            
        for index, i in enumerate(appSoup.find_all('ul', class_ = 'slope-report__details')):
            for j_index, j in enumerate(i.find_all('li')):
                if index == 0:
                    if j_index == 0:
                        conditons_dict['Temp ' + j.find('span', class_ = 'slope-report__details-label').get_text()] = j.find('span', class_ = 'slope-report__details-value').get_text() + 'F'
                    elif j_index == 1:
                        conditons_dict['Temp High/Low'] = j.find('span', class_ = 'slope-report__details-value').get_text()
                    elif j_index == 2:
                        conditons_dict['Temp High/Low'] += '/'+ j.find('span', class_ = 'slope-report__details-value').get_text() + 'F'
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
        self.conditons_dict = conditons_dict


    def add_slope(self, appSoup):
        appSlopeUL = appSoup.find_all('ul', class_ = 'slope-report__status')
        self.slope_dict =  {i.find('span', class_ = 'slope-report__status-title').get_text():
                i.find('span', class_ = 'slope-report__status-status').get_text()
                for i in appSlopeUL[0].find_all('li')}
    

    def add_lift(self, appSoup):
        appSlopeUL = appSoup.find_all('ul', class_ = 'slope-report__status')
        self.lift_dict = {i.find('span', class_ = 'slope-report__status-title').get_text():
                i.find('span', class_ = 'slope-report__status-status').get_text()
                for i in appSlopeUL[1].find_all('li')}


    def update(self):
        headers = {'User-Agent': 'Mozilla/5.0 '}
        appWPResponse = requests.get('https://www.appskimtn.com/slope-report', headers=headers)
        appWP = appWPResponse.content
        appSoup = BeautifulSoup(appWP, 'html.parser')

        self.add_conditions(appSoup)
        self.add_lift(appSoup)
        self.add_slope(appSoup)


    def get_conditions(self):
        return self.conditons_dict
    

    def get_slope(self):
        return self.slope_dict
    

    def get_lift(self):
        return self.lift_dict


    def print_lift_status(self):
        print('Appalachain Ski Mtn Lift Status: ')
        for key, val in self.lift_dict.items():
            print(key + ': ' + val)
   

    def print_conditions(self):
        print('Appalachain Ski Mtn Conditions: ')
        for key, val in self.conditons_dict.items():
            print(key + ': ' + val)


    def print_slope_status(self):
        print('Appalachain Ski Mtn Slope Status: ')
        for key, val in self.slope_dict.items():
            print(key + ': ' + val)


    def combine_dictionaries(self):
        return {'Appalachain Ski Mtn Conditions': self.conditons_dict, 'Appalachain Ski Mtn Lifts': self.lift_dict, 'Appalachain Ski Mtn Slopes': self.slope_dict}


    def all_dicts_with_lists(self):
        return {'Appalachain Ski Mtn Conditions Name': list(self.conditons_dict.keys()), 
                'Appalachain Ski Mtn Conditons Status': list(self.conditons_dict.values()),
                'Appalachain Ski Mtn Slope Name': list(self.slope_dict.keys()), 
                'Appalachain Ski Mtn Slope Status': list(self.slope_dict.values()),
                'Appalachain Ski Mtn Lift Name': list(self.lift_dict.keys()),
                'Appalachain Ski Mtn Lift Status': list(self.lift_dict.values())}