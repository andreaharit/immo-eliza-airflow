from bs4 import BeautifulSoup
import json
import requests
import time
import random 
from config import headers

class ExtractPage:
    """
        Extracts a json from the page's html where we have all the characteristics of a property.
        Has a method to filter out which page has only one property or multiple listed inside.
        Args:
            url (str): url of a listing in the website.
    """
    def __init__(self, house_id, house_url: str) -> None: 
        # Sets up request with a random sleep to not get kicked out
        self.id= house_id
        time.sleep(random.random())
        
        try:
            r = requests.get(house_url, headers = headers)
            content = r.content
            self.status = r.status_code
            if self.status == 200:
                print(f"Success getting into house {self.id}")
                # Parses html getting into a script tag, cleans it and dumps as a json
                soup = BeautifulSoup(content, "html.parser")        
                raw_data = soup.find("script", attrs={"type":"text/javascript"}).text.replace("window.classified = ","" ).replace(";", "").strip()
                self.raw = dict(json.loads(raw_data)) 
                print(f"Success scrapping all info house {self.id}")
                # Tracks if page is a single property or a list of properties
                self.is_single()
            else:
                print(f"Problem on {self.id}, it is returning status {self.page_status}...")  
        except ConnectionError as e:
                print("Kicked out of connection by host...")
                self.website_status =  False       

    def is_single(self) -> bool: 
        # Uses key "cluster" to filter if multiple or single       
        if self.raw["cluster"] == "null" or self.raw["cluster"] == None:            
            self.is_single = True
        else:
            self.is_single = False

class Single:
    """
    Extracts characteristics of a page that has only one property listed inside.
    Arg:
        raw (json): Json file extracted via the class ExtractPage.

    """    
    def __init__(self, raw)->None:

        self.data = raw 

        # Numerical characteristics
        try:    
            self.id = self.validate(raw["id"])
        except TypeError:
            self.id = None
        try:
            self.price = self.validate(raw["transaction"]["sale"]["price"])
        except TypeError:
            self.price = None
        try:
            self.postal_code = self.validate(raw["property"]["location"]["postalCode"])
        except TypeError:
            self.postal_code = None
        try:           
            self.facades = self.validate(raw["property"]["building"]["facadeCount"])
        except TypeError:
            self.facades= None
        try:
            self.year = self.validate(raw['property']['building']['constructionYear'])
        except TypeError:
            self.year = None

        # Room count
        try:
            self.rooms = self.validate(raw["property"]["roomCount"])
        except TypeError:
            self.rooms = None
        try:
            self.bedrooms = self.validate(raw["property"]["bedroomCount"])
        except TypeError:
            self.bedrooms = None
        try:
            self.bathrooms = self.validate(raw["property"]["bathroomCount"])
        except TypeError:
            self.bathrooms = None

        # Surfaces     
        try:
            self.habitsurf = self.validate(raw["property"]["netHabitableSurface"])
        except TypeError:
            self.habitsurf = None
        try:
            self.gardensurf = self.validate(raw["property"]["gardenSurface"])
        except TypeError:
            self.gardensurf = None
        try:
            self.terracesurf = self.validate(raw["property"]["terraceSurface"])
        except TypeError:
            self.terracesurf = None
        try:
            self.livingsurf = self.validate(raw["property"]["livingRoom"]['surface'])
        except TypeError:
            self.livingsurf = None
        try:
            self.kitchensurf= self.validate(raw["property"]["kitchen"]["surface"])
        except TypeError:
            self.kitchensurf = None
        try:
            self.land = self.validate(raw["property"]["land"]["surface"])
        except TypeError:
            self.land = None

        # String characteristics  
        try:
            self.prop_type = self.validate(raw["property"]["type"])
        except TypeError:
            self.prop_type = None
        try:
            self.subtype = self.validate(raw["property"]["subtype"])
        except TypeError:
            self.subtype = None
        try:
            self.region = self.validate(raw["property"]["location"]["region"]).lower()
        except TypeError:
            self.region = None
        try:
            self.province = self.validate(raw["property"]["location"]["province"])
        except TypeError:
            self.province = None
        try:
            self.district = self.validate(raw["property"]["location"]["district"])
        except TypeError:
            self.district = None
        try:
            self.city = self.validate(raw["property"]["location"]["locality"]).capitalize()
        except TypeError:
            self.city = None
        try:
            self.epc = self.validate(raw["transaction"]["certificates"]["epcScore"])
        except TypeError:
            self.epc = None
        try:
            self.state = self.validate(raw['property']['building']['condition'])
        except TypeError:
            self.state = None
        try:
            self.heating = self.validate(raw["property"]["energy"]["heatingType"])
        except TypeError:
            self.heating = None  
        
        # Characteristcs that must return either 0 or 1 (has or dont)
        try:
            self.garden = self.zero_one(raw["property"]["hasGarden"])
        except TypeError:
            self.garden = None
        try:
            self.swimmingpool = self.zero_one(raw['property']['hasSwimmingPool'])
        except TypeError:
            self.swimmingpool = None
        try:
            self.fireplace = self.zero_one(raw["property"]["fireplaceExists"])
        except TypeError:
            self.fireplace = None
        try:
            self.kitchen = self.zero_one(char_path=raw["property"]["kitchen"]["type"], string_comp="NOT_INSTALLED")
        except TypeError:
            self.kitchen = None
        try:
            self.furnished = self.zero_one(raw["transaction"]["sale"]["isFurnished"])
        except TypeError:
            self.furnished = None
        try:
            self.terrace = self.zero_one(raw["property"]["hasTerrace"])
        except TypeError:
            self.terrace = None
        try:
            self.attic = self.zero_one(raw["property"]["hasAttic"])
        except TypeError:
            self.attic = None
        try:
            self.basement = self.zero_one(raw["property"]["hasBasement"])
        except TypeError:
            self.basement = None     

        print ("Success getting each characteristic...") 

    def validate (self, info):
        """Checks if the json value is not Null, 0 or invalid.
            Arg:
                info: value of a particular key path in the json
            Returns:
                Valid information.
        """
        try:
            char = info
            if char not in ["None", "Null", 0, None]:
                return char
            else:
                return None
        except Exception as e:
            return None

    def zero_one (self, char_path, string_comp:str = None):
        """Change valid value in json to a boolean."""
        char = self.validate(char_path)
        if char in [None, string_comp]:
            return 0
        else:
            return 1

    