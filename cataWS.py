from bs4 import BeautifulSoup
import requests
import sys


class Cata():


    def __init__(self):
        self.conditons_dict = {}
        self.slope_dict = {}
        self.lift_dict = {}
  
  
    def add_conditions(self, cataSoup):
        print("cataWS: add_conditions()")
        sys.stdout.flush()

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


    def add_slope(self, cataSoup):
        print("cataWS: add_slope()")
        sys.stdout.flush()

        cata_trail_columns =[i.get_text(strip = True) for i in cataSoup.find('table', class_='trails-table').find_all('td')]
        return {cata_trail_columns[i]: cata_trail_columns[i + 1] for i in range(0, len(cata_trail_columns), 2)}
    

    def add_lift(self, cataSoup):
        print("cataWS: add_lift()")
        sys.stdout.flush()

        cata_lifts_columns = [i.get_text(strip = True) for i in cataSoup.find('table', class_='lifts-table').find_all('td')]
        return {cata_lifts_columns[i]: cata_lifts_columns[i + 1] for i in range(0, len(cata_lifts_columns), 2)}
    

    def update(self):
        print("cataWS: update()")
        sys.stdout.flush()

        cataWPResponse = requests.get('https://cataloochee.com/the-mountain/snow-report/')
        cataWP = cataWPResponse.content
        cataSoup = BeautifulSoup(cataWP, 'html.parser')
        self.conditons_dict = self.add_conditions(cataSoup)
        self.slope_dict = self.add_slope(cataSoup)
        self.lift_dict = self.add_lift(cataSoup)
    

    def get_conditions(self):
        return self.conditons_dict
    

    def get_slope(self):
        return self.slope_dict
    

    def get_lift(self):
        return self.lift_dict


    def print_slope_status(self):
        print('Cataloochee Ski Area Slope Status')
        for key, val in self.slope_dict.items():
            print(key + ': ' + val)


    def print_lift_status(self):
        print('Cataloochee Ski Area Lift Status')
        for key, val in self.lift_dict.items():
            print(key + ': ' + val)


    def print_conditions(self):
        print('Cataloochee Ski Area Current Conditions')
        for key, val in self.conditons_dict.items():
            print(key + ': ' + val)


    def combine_dictionaries(self):
        return {'Cataloochee Ski Area Conditons': self.conditons_dict, 
                'Cataloochee Ski Area Lifts': self.lift_dict,
                'Cataloochee Ski Area Slopes': self.slope_dict}


    def all_dicts_with_lists(self):
        return{"Cataloochee Ski Area Conditions Name": list(self.conditons_dict.keys()),
            "Cataloochee Ski Area Conditions Status": list(self.conditons_dict.values()),
            "Cataloochee Ski Area Slope Name": list(self.slope_dict.keys()),
            "Cataloochee Ski Area Slope Status": list(self.slope_dict.values()),
            "Cataloochee Ski Area Lift Name": list(self.lift_dict.keys()),
            "Cataloochee Ski Area Lift Status": list(self.lift_dict.values())}