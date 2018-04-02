from email_scraper import scrape_emails
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import smtplib, os, sys, socket, codecs
from smtplib import SMTPException
import pandas as pd
from collections import OrderedDict
from datetime import date
import numpy as np 

file_urls = codecs.open('urls.csv','r','utf-8')

# emails = set()

# Where the output will be stored
filename = "scraping_emails.csv"

f = open(filename, "a")
f.seek(0)
f.truncate()

# Setting a fake agent to make google "think" a browser is sending requests
ua = UserAgent()
header = {'user-agent':ua.chrome}

for enrich_url in file_urls:

		try:
			if(len(enrich_url)==0):
				continue
			else:
				# print("______________")

				if(enrich_url[0:5] == "https"):
					if(enrich_url[-1] == "\n"):
						website = requests.get(enrich_url[:-2], headers=header)
					else:
						website = requests.get(enrich_url, headers=header)
				else:
					if(enrich_url[-1] == "\n"):
						website = requests.get("https://" + enrich_url[:-2], headers=header)
					else:
						website = requests.get("https://" + enrich_url, headers=header)

			# We're using html.parser since it's in Python already / no need to extra-install
			soup = BeautifulSoup(website.content, 'html.parser')

			# In order to scrape e-mails, we select 
			mailto = soup.select('a[href^="mailto:"]')

			scraped_emails = scrape_emails(str(mailto))
			print(scraped_emails)

		except:
			print("No result")
			continue