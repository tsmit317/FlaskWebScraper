from bs4 import BeautifulSoup
import requests
import sys

class Sugar():


    def __init__(self):
        self.conditons_dict = {}
        self.slope_dict = {}
        self.lift_dict = {}
    
    def replace_all_cap(self, cond_list):
        to_replace = {'NUMBER OFLIFTS OPEN': 'Lifts Open', 'NUMBER OFSLOPES OPEN': 'Trails Open', 'AVERAGEDEPTH': 'Average Depth'}
        for i, val in enumerate(cond_list):
            if val in to_replace:
                cond_list[i] = to_replace[val]
        
    
    #TODO: This looks ugly
    def add_conditions(self, sugarSoupMain): 
        print("suagrWS: add_conditions()")
        sys.stdout.flush()
        # Is there a way to add this to a dictionary without involving a list? 
        if sugarSoupMain.find('table', class_ = "smrcctable").find('td').get_text() == 'SNOWMAKING IN PROGRESS':
            sugar_conditions_list = []
            for index, i in  enumerate(sugarSoupMain.find('table', class_ = "smrcctable").find_all('td')):
                if index == 0 and i.get_text() == 'SNOWMAKING IN PROGRESS':
                    sugar_conditions_list.append('Snowmaking')
                    sugar_conditions_list.append('In Progress') 
                else:
                    sugar_conditions_list.append(i.get_text(strip = True).replace('(MAP)', ""))
                    
        else:
            sugar_conditions_list = [i.get_text(strip = True).replace('(MAP)', "") for i in sugarSoupMain.find('table', class_ = "smrcctable").find_all('td')]

            sugar_conditions_list.append('Snowmaking')
            sugar_conditions_list.append('Not In Progress')
            
        temperature_list = [j.get_text().title() for i in sugarSoupMain.find('table', class_ = "smrwxtable").find_all('td')[:2] for j in i.find_all('span')[:2]]
        self.replace_all_cap(sugar_conditions_list)
        sugar_conditions_list = [*temperature_list, *sugar_conditions_list]    
        sugar_conditions_dict = {sugar_conditions_list[i]: 
                                sugar_conditions_list[i+1] 
                                for i in range(0, len(sugar_conditions_list), 2)}          
        return sugar_conditions_dict


    def add_lift(self, sugarTags):
        print("suagrWS: add_lift()")
        sys.stdout.flush()
        # Gets Lifts. Had to use next_sibling instead of get_text()
        # Note: .get('alt') might not be accurate. May need to switch to .get('src')
        return {i.next_sibling.strip(): i.get('alt') for i in sugarTags[0].find_all('img')}


    # TODO: Clean this up
    def add_slope(self, sugarTags):
        print("suagrWS: add_slope()")
        sys.stdout.flush()

        sugar_slope_dict = {}
        # Get Black Diamond Runs. These all used .get_text(), so I grouped them together. 
        # Odd indexes were skipped, as they were just labels
        sugar_BlackDiamond_TagList = [sugarTags[2], sugarTags[4], sugarTags[6]]

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

    def update(self):
        print("suagrWS: update()")
        sys.stdout.flush()
        headers = {'User-Agent': 'Mozilla/5.0'}
        sugarWPResponse = requests.get('http://www.skisugar.com/', headers=headers)
        sugarWP = sugarWPResponse.content
        sugarSoupMain = BeautifulSoup(sugarWP, 'html.parser') # Gets Conditions from the main page

        sugarWPResponseTrailmap = requests.get('http://www.skisugar.com/trailmap/', headers=headers)
        sugarWPTrailmap = sugarWPResponseTrailmap.content
        sugarSoupTrailmap = BeautifulSoup(sugarWPTrailmap, 'html.parser')
        sugarTags =  sugarSoupTrailmap.find_all('p', attrs= {'style':"line-height: 18px;"})

        self.conditons_dict = self.add_conditions(sugarSoupMain)
        self.slope_dict = self.add_slope(sugarTags)
        self.lift_dict = self.add_lift(sugarTags)


    def get_conditions(self):
        return self.conditons_dict
    

    def get_slope(self):
        return self.slope_dict
    

    def get_lift(self):
        return self.lift_dict
        

    def print_lift_status(self):
        print('Ski Sugar Lift Status:')
        for key, val in self.lift_dict.items():
            print(key + ': ' + val)


    def print_slope_status(self):
        print('Ski Sugar Slope Status')
        for key, val in self.slope_dict.items():
            print(key + ': ' + val)


    def print_conditions(self):
        print('Sugar Ski Resort Current Conditions')
        for key, val in self.conditons_dict.items():
            print(key + ': ' + val) 


    def combine_dictionaries(self):
        return {'Ski Sugar Conditons': self.conditons_dict, 
                'Ski Sugar Lifts': self.lift_dict, 
                'Ski Sugar Slopes': self.slope_dict}


    def all_dicts_with_lists(self):
        return{ "Ski Sugar Conditions Name": list(self.conditons_dict.keys()),
                "Ski Sugar Conditions Status": list(self.conditons_dict.values()),
                "Ski Sugar Slope Name": list(self.slope_dict.keys()),
                "Ski Sugar Slope Status": list(self.slope_dict.values()),
                "Ski Sugar Lift Name": list(self.lift_dict.keys()),
                "Ski Sugar Lift Status": list(self.lift_dict.values())}
