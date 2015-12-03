import mechanize, sys
from bs4 import BeautifulSoup

br = mechanize.Browser()
br.set_handle_robots(False)
baseUrl = 'http://www.magicbricks.com/'

def processPage(soup):
	attributes = {}
	# try:
	# 	response = br.open(url)
	# except:
	# 	print 'Some exception'
	#
	# soup = BeautifulSoup(response)

	# preliminary data
	preliminary = soup.find('div', {'class':'nDatabock'})
	temp = preliminary.find('div', {'class' : 'propIDnPDate'}).text.split('|')
	temp = [str(x.split(':')[1].strip()) for x in temp]

	attributes['id'] = temp[0]
	attributes['date_added'] = temp[1].replace("'", '20')

	temp = preliminary.find('div', {'class' : 'priceInfo'}).text.split('\n')
	attributes['apartment_type'] = temp[0].replace('Flat', '').strip()
	attributes['covered_area'] = temp[1].split(' ')[0].strip() # also include built_up_area later

	temp = preliminary.find('div', {'class' : 'nEMIblock'}).text.strip().split('\n')[0].replace('per', '').replace(',', '').replace(u'\u20b9', '').strip()
	attributes['per_square_feet_rate'] = temp

	temp = preliminary.findAll('div', {'class' : 'nActualAmt'})[1].text.replace(u'\u20b9', '').strip().split(' ')
	val = float(temp[0])*( 100000 if temp[1] == 'Lac' else 10000000 )
	attributes['price'] = val

	temp = preliminary.find('div', {'class' : 'nProjNmLoc'}).find('span', {'class' : 'place'}).text.split(',')
	attributes['city_name'] = temp[1].strip()
	attributes['locality'] = temp[0].strip()

	preliminary = preliminary.find('div', {'class' : 'nInfoDataBlock'}).findAll('div', {'class' : 'dataVal'})

	for x in preliminary:
		for y in x.text.replace('\n', ' ').strip().split(','):
			temp = ''.join([i if ord(i) < 128 else ' ' for i in y])
			
		# print temp
		# print







def doEverything():
	# try:
	# 	response = br.open('http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai-Metropolitan-Region&price=Y&pageOption=B')
	# except Exception as e:
	# 	print 'Error opening the page: ' + str(e)
	# 	sys.exit(1)

	# soup = BeautifulSoup(response)
	soup = BeautifulSoup(open('out.html', 'r'))
	divs = soup.findAll('div', {'class':'srpBlockListRow'})

	for div in divs:
		onclick = div['onclick']
		indexOfSlash = onclick.index('/')
		indexOfEqual = onclick.index("','")
		accessUrl = baseUrl + onclick[indexOfSlash:indexOfEqual]

		processPage(accessUrl)

soup = BeautifulSoup(open('out1.html', 'r'))
processPage(soup)
