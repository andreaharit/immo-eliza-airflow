import json
import csv
import click

from src_scrape.scrape_links import Links
from src_scrape.scrape_house import ExtractPage, Single



@click.command()
@click.option("--path_raw", help="Path to the raw CSV")
@click.option("--path_links", help="Path to save the scrapped links CSV")
def scrappe_all(path_raw, path_links) -> None:
    """
    Scrapes house characteristics and dumps them into a csv file.
    Args:
        path_raw: csv path where the raw data with the houses characteristics will be saved.
        path_links: csv path where the links for each house that were scrapped will be saved.
    """

    # Extracts house links of first N homepages (according to config) and dumps into csv file
    print("Extracting the links")
    extract_links = Links(outfile_links = path_links)

    # Starts out csv file where we'll write each house characteristic
    outfile_houses = path_raw
    with open (outfile_houses, "w", newline='', encoding='utf-8') as file_house:  
        # Collected fields
        fields = ['id', 'city', 'postal_code', 'district', 'province', 'price', 
                'subtype', 'state_construction', 'living_area', 'terrace_area', 
                'garden_area', 'rooms', 'bedrooms', 'bathrooms', 'livingroom_surface', 
                'kitchen_surface', 'facades', 'has_garden', 'kitchen', 'furnished', 
                'fireplace', 'swimmingpool', 'has_terrace', 'has_attic', 'has_basement', 
                'construction_year', 'epc', 'heating', 'area_total']

        writer = csv.DictWriter(file_house, fieldnames = fields)
        # Writes its header
        writer.writeheader()

        # Start collecting characteristcs from houses
        # Open house listing links
        print("Extracting the houses information...")
        with open(extract_links.outfile_links, 'r') as file_links:
            reader = csv.reader(file_links)
            # Skips the header
            next(reader, None)
            # Loops every link in the links file to extract each house characteristic
            for row in reader:
                id_house = row[0]
                link = row[1]  
                # Extracts the house information in the link if it's a single listing page
                page = ExtractPage(house_id= id_house, house_url=link)
                if page.is_single == True:
                    properties = Single(raw = page.raw)    
                    # Writes characteristics into house csv               
                    writer.writerow({
                                    'id': properties.id, 
                                    'city': properties.city, 
                                    'postal_code': properties.postal_code, 
                                    'district': properties.district , 
                                    'province': properties.province , 
                                    'price': properties.price, 
                                    'subtype': properties.subtype, 
                                    'state_construction': properties.state, 
                                    'living_area': properties.habitsurf, 
                                    'terrace_area': properties.terracesurf, 
                                    'garden_area': properties.gardensurf, 
                                    'rooms': properties.rooms , 
                                    'bedrooms': properties.bedrooms, 
                                    'bathrooms': properties.bathrooms, 
                                    'livingroom_surface': properties.livingsurf, 
                                    'kitchen_surface': properties.kitchensurf, 
                                    'facades': properties.facades, 
                                    'has_garden': properties.garden, 
                                    'kitchen': properties.kitchen, 
                                    'furnished': properties.furnished, 
                                    'fireplace': properties.fireplace, 
                                    'swimmingpool': properties.swimmingpool, 
                                    'has_terrace': properties.terrace , 
                                    'has_attic': properties.attic, 
                                    'has_basement': properties.basement, 
                                    'construction_year': properties.year, 
                                    'epc': properties.epc, 
                                    'heating': properties.heating, 
                                    'area_total': properties.land
                                    })
            print("Finished extracting the houses information...")
            
if __name__ == "__main__":
    scrappe_all()









