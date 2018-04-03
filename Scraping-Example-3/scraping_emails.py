import urllib.request 
import re
import codecs
import pandas as pd
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup
from time import sleep
import socket
import lxml.html

# global validmail
scraped_emails = []
working_urls = []
internal_urls = []
urls_to_scrape = []

fileurls = codecs.open('urls-to-scrape.csv', 'r', 'latin-1')
filename = "scraped-emails.csv"

# proxy_support = urllib.request.ProxyHandler({"http":"http://61.233.25.166:80"})
# opener = urllib.request.build_opener(proxy_support)
# urllib.request.install_opener(opener)

# ua = UserAgent()
# header = {'user-agent':ua.chrome}


# The function to verify URLs
def verify_urls(file):

	sleep(30)
	linelist = file.readlines()
	for url in linelist:
		url = url.strip('\r\n')

		try:
			socket.setdefaulttimeout(8000)
			req = requests.get("http://" + url)
			r = req.status_code
			request = str(r)
			if(request[0] == '2'):
				working_url = req.url
				working_urls.append(working_url)
			else:
				continue

		except urllib.error.URLError as e:
			print(e.reason)
			pass

		except requests.exceptions.SSLError as q:
			pass

		except requests.exceptions.ConnectionError:
			r = "Connection Refused"
			pass


# The function to find top 50 internal links of a URL
def internal_links(var):

	nlines = 0
	dom = lxml.html.fromstring(var)
	for link in dom.xpath('//a/@href'):
		# print(link)
		nlines += 1
		# working_urls.append(link)
		if nlines >= 50:
			break
		internal_urls.append(link)


# The function to scrape emails
def scrape_emails():

	sleep(30)
	for url in working_urls:
		if(url.strip() == ''):
			continue
		try:
			fi = urllib.request.urlopen(url)
			s = fi.read().decode('utf-8')

			nlines = 0
			dom = lxml.html.fromstring(var)
			for link in dom.xpath('//a/@href'):
				# print(link)
				nlines += 1
				# working_urls.append(link)
				if nlines >= 50:
					break
				internal_urls.append(link)

			emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}", s)
			# print(emails)
			for validmail in emails:
				if(validmail[-3:] != 'gif' and validmail[-3:] != 'png' and validmail[-3:] != 'jpg' and validmail[-3:] != 'tif'):
					# print(validmail)
					scraped_emails.append(validmail)

			raw_data = {'emails': validmail}
			df = pd.DataFrame(raw_data, columns = ['emails'], index = [1])
			df.to_csv(f)

		except urllib.error.URLError:
			# The reason for this error. It can be a message string or another exception instance.
			print("URL Error")
			pass

		except requests.exceptions.ConnectionError:
			print("Connection Refused")
			pass

		except:
			print("General exception: here")
			pass


# urls_to_scrape = working_urls + internal_urls

# Calling functions
verify_urls(fileurls)
scrape_emails()
print(scraped_emails)
# print(internal_urls)
# print(scraped_emails)
# print(internal_urls)