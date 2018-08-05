import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import sys
import argparse
import datetime
from datetime import datetime, timedelta
import copy

#Command line argument parser code
# Instantiate the parser
parser = argparse.ArgumentParser(description='Python scraper to scrape job postings from Indeed')

# Optional argument
parser.add_argument('-company', type=str,  help='Enter company to scrape', nargs='?')
parser.add_argument('-file', type=str,  help='Enter the file to be written to', required=False, nargs='?', default=None)




def Scrap_Data():
        #URL = "https://www.indeed.com/q-"+company+"-jobs.html"
        baseurl = 'https://www.indeed.com/jobs?q={0}&start={1}'
        args = parser.parse_args()
        company=args.company
        file_path=args.file
        if args.company==None:
            company= input("Enter the company: ")
        if args.file==None:
            file_path= '{} {}.csv'.format(company,datetime.today().strftime('%m-%d-%y %H.%M.%S'))
        elif args.file[-1]=="\\":
             file_path= '{}{} {}.csv'.format(file_path,company,datetime.today().strftime('%m-%d-%y %H.%M.%S'))
        
            
        
        print('Scrapping ',company)
        print('Writing to',file_path)
        #print(soup.prettify())
        jobs = []
        locations = []
        df = pd.DataFrame()
        

        prev_page_titles=[]
        for page in range(1,200):
            page = (page-1) * 10
            URL = baseurl.format(company.replace(' ','%20'),page) #Remove any spaces in company name
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(urllib.request.urlopen(URL), "lxml")

            targetElements = soup.find_all(name='div', attrs={'class':'row'})
            
            page_titles=[]

            for elem in targetElements:
                #comp_name = elem.find('b').getText()
                try:
                    job_title = elem.find('a', attrs={'data-tn-element':'jobTitle'}).getText()
                    page_titles.append(job_title)
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
                                'Location': location,'State':state,
                                'Date':get_days_ago(string_to_int(date1[0:2])), 'Date Raw':date1
                               }, ignore_index=True)
    
            #Check if we reached end of pages by comparing with previous pages   
            if(prev_page_titles==page_titles):
                #reached end of pages. Remove last n elements and break
                print('Reached End, Dropping rows:',len(targetElements))
                #print('Previous',prev_page_titles)
                #print('Current',page_titles)
                df.drop(df.tail(len(targetElements)).index,inplace=True) # drop last n rows
                break;
            prev_page_titles=copy.deepcopy(page_titles)
        df.to_csv(file_path, sep=',', encoding='utf-8')
        #return df


def string_to_int(string):
    try:
        variable = int(string)
    except ValueError:
        variable = None
    return variable

def get_days_ago(days):
    try:
        return (datetime.today() - timedelta(days=string_to_int(days))).strftime('%Y-%m-%d')
    except Exception as e:
        return None
        
        


Scrap_Data()