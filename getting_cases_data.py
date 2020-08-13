"""
This is the scrapping graphs data from a website using Python-3.7.6
We run this code to get the daily data about COVID-19
The data that we are trying to get is country vise scale
All this data provided by www.worldometers.info

"""


import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import js2xml
from itertools import repeat

# ticking function
def ticking(n):
    for i in range(10000 * n):
        print("tick")
        time.sleep(1)


"""
scraping_graph:
Here we scrap the data from the graph that is located in the given url
TODO: Make sure you are scraping the right graph.
"""
def scraping_graph(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    script = soup.find_all("script", text=re.compile("Highcharts.chart"))
    script = script[2].text
    parsed = js2xml.parse(script)
    data = [d.xpath(".//array/number/@value") for d in parsed.xpath("//property[@name='data']")]
    categories = parsed.xpath("//property[@name='categories']//string/text()")
    output = list(zip(repeat(categories), data))
    df = pd.DataFrame(output[0])
    df = df.T
    df.columns = ['Months', 'Daily Cases']
    df_3 = pd.DataFrame(output[1])
    df_3 = df_3.T
    df_3.columns = ['Months', 'M 3 Cases']
    df_7 = pd.DataFrame(output[2])
    df_7 = df_7.T
    df_7.columns = ['Months', 'M 7 Cases']
    dfs = pd.merge(df,
                   df_3,
                   on='Months',
                   how='left')
    dfs = pd.merge(dfs,
                   df_7,
                   on='Months',
                   how='left')
    dfs.to_csv('daily_cases_covid-19.csv')


"""
Link_finder :
Finds all the links in the table that is in the give url
TODO: Make sure you are getting the right links.
"""
def link_finder(url):
    html = requests.get(url).content
    #parsing HTML
    soup = BeautifulSoup(html, 'html.parser')
    #getting the link of all population
    linkfind = soup.find_all('a', {'href': re.compile("coronavirus/usa/")})
    print(linkfind)
    region_links = []
    for links in linkfind:
        head_link = "https://www.worldometers.info"
        link = links.get('href')
        if link.find(head_link) == -1:
            head_link += link
            region_links.append(head_link)
    return region_links


if __name__ == "__main__":
    """ Buenos dias
    
    Here we do two things:
    1. finding all the links related to each regions showen in the table of the given url
    2. convert the graph of each region to csv file
    Each graph contains data about daily cases, average past 3 days, average past 7 days.
    """
    url = 'https://www.worldometers.info/coronavirus/country/us'
    links = link_finder(url)
    scraping_graph(url)
    """
    for link in links:
        scraping_graph(link)
    """

    #using a timer for loading page
    """
    # Start ticking as a process
    p = multiprocessing.Process(target=ticking, name="Ticking", args=(10,))
    p.start()
    # Wait 15 seconds for ticking
    time.sleep(15)
    # Terminate ticking
    p.terminate()
    # Cleanup
    p.join()
    """

