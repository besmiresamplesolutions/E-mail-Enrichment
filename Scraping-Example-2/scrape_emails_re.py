import urllib.request 
import re
import codecs
import pandas as pd
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup

urls = []
global validmail

file_urls = codecs.open('urls.csv', 'r', 'latin-1')

# filename = codecs.open('scraping_test.csv', 'w', 'utf-8')
filename = "scraping_test.csv"

try:
	f = open(filename, 'a')
	f.seek(0)
	f.truncate()
except:
	print("Please close the .csv file in order for changes to append")

ua = UserAgent()
header = {'user-agent':ua.chrome}

for url in file_urls:
	if(url.strip() == ''):
		continue
	try:
		fi = urllib.request.urlopen(url)
		s = fi.read().decode('utf-8')

		emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
		# print(emails)
		for validmail in emails:
			if(validmail[-3:] != 'gif' and validmail[-3:] != 'png' and validmail[-3:] != 'jpg' and validmail[-3:] != 'tif'):
				print(validmail)


		urls.append(validmail)
		raw_data = {'emails': validmail}
		df = pd.DataFrame(raw_data, columns = ['emails'], index = [1])
		df.to_csv(f)

	except:
		print("Exception")
		pass


f.close()