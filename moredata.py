from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time 
import pandas as pd
import requests

url="https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(url)
time.sleep(10)
scraped_data=[]

def scrape(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        templist=[]
        trtags=soup.find_all("tr",attrs={"class":"fact_row"})
        for tr in trtags:
            tdtags=tr.find_all("td")
            for td in tdtags:
                try:
                    templist.append(td.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        scraped_data.append(templist)
    except:
        time.sleep(1)
        scrape(hyperlink)

planetdf =pd.read_csv("class127.csv")
for i ,row in planetdf.iterrows():
    scrape(row["hyperlink"])
    print(f"data at hyperlink {i+1} completed")

scrapeddata=[]
for row in scraped_data:
    replaced=[]
    for i in row:
        i = i.replace("\n","")
        replaced.append(i)
    scrapeddata.append(replaced)

headers=["planet_type","discovery_date", "mass", "planet_radius", "orbital_radius", "orbital_period", "eccentricity", "detection_method"]

planetdf=pd.DataFrame(scrapeddata,columns=headers)
planetdf.to_csv("class128.csv",index=True,index_label="id")

    