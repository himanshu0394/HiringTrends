import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request


def Scrap_Data(company):
        #URL = "https://www.indeed.com/q-"+company+"-jobs.html"
        baseurl = 'https://www.indeed.com/jobs?q={0}&start={1}'

        #print(soup.prettify())
        jobs = []
        locations = []
        df = pd.DataFrame()


        for page in range(1,10):
            page = (page-1) * 10
            URL = baseurl.format(company,page)
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(urllib.request.urlopen(URL), "lxml")

            targetElements = soup.find_all(name='div', attrs={'class':'row'})


            for elem in targetElements:
                #comp_name = elem.find('b').getText()
                try:
                    job_title = elem.find('a', attrs={'data-tn-element':'jobTitle'}).getText()
                except:
                    job_title = ""

                try:
                    location = elem.find('div', attrs={'class':'location'}).getText().split(',')[0]
                    state = elem.find('div', attrs={'class':'location'}).getText().split(',')[1][:3]
                except:
                    location = elem.find('span', attrs={'class':'location'}).getText().split(',')[0]
                    state = elem.find('span', attrs={'class':'location'}).getText().split(',')[1][:3]
                try:
                    summary = elem.find('span', attrs={'class':'summary'}).text.replace('\n', '')
                except:
                    summary = ""
                try:
                    date1 = elem.find('span', attrs={'class':'date'}).getText()
                except:
                    date1 = ''





                df = df.append({'Company Name': company, 'Job Title': job_title,
                                'Location': location,'State':state,'Date':date1
                               }, ignore_index=True)
        df.to_csv('Deloitte_20.csv', sep=',', encoding='utf-8')
        #return df




comp = input("Enter the company")
Scrap_Data(comp)