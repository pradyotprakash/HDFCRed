import mechanize, sys, csv
from bs4 import BeautifulSoup

baseUrl = 'http://www.99acres.com/'

br = mechanize.Browser()
br.set_handle_robots(False)

try:
	response = br.open('http://www.99acres.com/search/property/buy/residential-all/mumbai?search_type=QS&search_location=CP12&lstAcn=CP_R&lstAcnId=12&src=CLUSTER&preference=S&selected_tab=1&city=12&res_com=R&property_type=R&isvoicesearch=N&keyword=mumbai&strEntityMap=IiI%3D&refine_results=Y&Refine_Localities=Refine%20Localities&action=%2Fdo%2Fquicksearch%2Fsearch&searchform=1&price_min=null&price_max=null')
except:
	print 'Unable to connect to 99acres. Check internet connection.'
	sys.exit(1)

data_file = csv.writer(open('training_data.csv', 'a'))
error_file = open('error_logs', 'a')

def processProperty(soup):
	print soup

while True:
	soup = BeautifulSoup(response)
	divs = soup.findAll('div', {'class' : 'srpWrap', 'data-pgid' : 'QS'})

	for div in divs:
		prop_id = div['data-propid']
		print baseUrl + prop_id
		response = mechanize.urlopen(baseUrl + prop_id, timeout=10.0)
		processProperty(BeautifulSoup(response))
		break

	next_page = soup.find('a', {'name' : 'nextbutton'})['href']

	break # comment out this later
	response = br.open(next_page)