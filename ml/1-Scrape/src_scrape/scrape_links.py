import requests
from bs4 import BeautifulSoup
import csv
import time
import random 


from config import base_url, end_url,  num_pages, headers

class Links:
    def __init__(self, outfile_links):
        self.outfile_links = outfile_links
        # Store ids so it checks for repeats
        ids =[]
        print("Scrapping links...")
        # Starts writting csv
        with open (outfile_links, "w", newline='') as f:  
            fields=['id','link']
            writer = csv.DictWriter(f, fieldnames=fields)            
            writer.writeheader()
            # Start getting information from each page in range according to config file
            try:
                for page in range (1, num_pages + 1):
                    self.page = page
                    # Random sleep between 0 and 1 sec to not be kicked out by host
                    time.sleep(random.random())

                    # Make url for a page number and requests
                    url = base_url + str(page) + end_url
                    r = requests.get(url=url, headers=headers)
                    self.page_status = r.status_code
                    # Start scrapping if connection is ok
                    if self.page_status == 200:                  
                        soup = BeautifulSoup(r.content.decode('utf-8'), "html.parser")
                        try:                            
                            cards = soup.find_all('div', attrs={'class':'card--result__body'})
                            self.website_status =  True
                            for card in cards:
                                tag = card.find('a', attrs={'class':'card__title-link'})
                                # Get each individual link in the page
                                link = tag['href']
                                # Get each individual house id 
                                clean_id = link.split("/")[-1]
                                if clean_id not in ids:
                                    ids.append(clean_id)
                                    # Writes links if id is not repeated
                                    writer.writerow({'id': clean_id, 'link': link})
                            print(f"Success scrapping links on page {page}")
                        except Exception as e:
                            print(f"Error scrapping links on page {page}, error {e}...")
                    else:                            
                        print(f"Problem on {self.page}, it is returning status {self.page_status}...")    
                print("Finished getting links...")
            except ConnectionError as e:
                print("Kicked out of connection by host...")
                self.website_status =  False            
