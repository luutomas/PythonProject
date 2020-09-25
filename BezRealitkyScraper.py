import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import tqdm as tqdm
from lxml import html
import time

class Estate:
    '''
    Defined as parent class for all possible version of bezrealitky pages
    Containing general methods used in scraping these websites
    '''
    def __init__(self, link):
        self.link = link
        self.soup = self.getSoup
        
    def getSoup(self):
        '''
        Initialize soup object.
        '''
        r = requests.get(self.link)
        r.encoding = 'UTF-8'
        
        return BeautifulSoup(r.text, 'html')   

class Flat(Estate):
    def __init__(self, link):
        '''
        Constructor for Flat calls parents Estate constructor first,
        where self.link and self.soup are created
        Then flat parameters and coordinates are generated as Flat attributes
        '''
        # Calling Estate constructor
        super().__init__(link)
        
        # getting soup
        self.soup = self.getSoup()
        
        # Getting paramaters of flat
        self.parameters = self.getParameters()
        
        # Getting coordinates of flat
        self.coordinates = self.getMap()
        
        # Getting resulting dataframe
        self.df = self.getDf()
        
    def getParameters(self):
        '''
        Get parameters from the html of given estate - such as price, disposition, the state of the house, etc.
        '''
        bf_table = self.soup.find('div',{'data-element':"detail-description"}).find('table')
        table_extract = [i.text.strip() for i in bf_table.findAll('tr')]
        df_table = pd.DataFrame(table_extract)
        df_table_split = df_table[0].str.split("\n", expand = True)
        df = pd.DataFrame(df_table_split[[0,1]])
        df.columns = ['metric', 'value']
        df = df.set_index('metric')
        return df
    
    def getMap(self):
        '''
        Get location of the property using longtitute and lattitude parameters.
        '''
        bf_map = self.soup.find('div','b-map__inner')
        f_lng = bf_map['data-lng']
        f_lat = bf_map['data-lat']
        loc_dict = {"lat" : f_lat, "long": f_lng}
        loc_df = pd.DataFrame.from_dict(loc_dict, orient = 'index', columns = ['value'])
        return loc_df
    
    
    def getDf(self):
        '''
        Return a wide dataframe from getMap() and getParameters(), index = the id of the post
        '''
        df_par = self.getParameters()
        df_map = self.getMap()
        df = pd.concat([df_par, df_map])
        df = df.T.set_index('Číslo inzerátu:')
        return df    

class Downloader:
    '''
    Download all links of real estate properties on the given website
    '''
    def __init__(self, link):
        '''
        Provide real estate webpage to extract the properties links
        '''
        self.link = link
        self.start_num = 1
        self.soup = self.getSoup()
        self.pages = self.getPages()
        self.links = self.getLinks()
        self.df = self.getDataset()
        self.flats = []
        self.failed_links = []
        
    def getSoup(self):
        '''
        Initialize soup object
        '''
        r = requests.get(self.link)
        r.encoding = 'UTF-8'
        return BeautifulSoup(r.text, 'lxml')
        
    def getPages(self):
        '''
        Generates a list of all pages for specific search on bezrealitky webpage
        '''
        all_pages = [self.link] # create a list of pages
        start_num = self.start_num # first page
        last_page = int(self.soup.find('ul', class_="pagination justify-content-md-end").findAll('li')[-2].text) # number of last page

        for i in range(start_num, last_page):
            offer_page = self.link + f'&page={i+1}'  # adding a page number at the end of each url
            all_pages.append(offer_page) # storage of tables for each flat

        return all_pages
    
    def getLinks(self):
        '''
        Generate a list of all flat links from a page. If there are multiple pages, for loop recursively get links from all pages
        '''    
        links_list = list()
        for page in self.pages:
            base_url = 'https://www.bezrealitky.cz'
            r = requests.get(page)
            r.encoding = 'UTF-8'
            wp = BeautifulSoup(r.text, 'lxml')
            links = wp.findAll('div', {'product__body'})
            for equity in links:
                if 'https://www.bezrealitky.cz' in equity.find('a')['href']:
                    links_list.append(equity.find('a')['href'])
                else: 
                    links_list.append(base_url + equity.find('a')['href'])
        return links_list

    def getDataset(self):
        '''
        Scraping information for each flat link
        '''
        dataset = pd.DataFrame()
        counter = 0
        for link in self.links:
            try:
                flat = Flat(link)
                dataset = dataset.append(flat.df, sort=False) # printing every 10th scraped flat
                counter = counter + 1
                if counter % 10 == 0:
                    print(f'>> {counter} flats scraped')
                    time.sleep(5)
            except Exception:
                self.failed_links.append(link)
        return dataset

