import mechanize, sys, csv, requests
from bs4 import BeautifulSoup

currentPageNo = 1

br = mechanize.Browser()
br.set_handle_robots(False)
baseUrl = 'http://www.magicbricks.com/'

data_file = csv.writer(open('training_data.csv', 'a'))
error_file = open('error_logs', 'a')

header = ['id','built_up_area','has_no_maintenance_staff','has_water_storage','has_no_lift','has_no_indoor_games_room','apartment_type','has_no_power_back_up','has_no_bank_&_atm','id','has_no_gymnasium','has_waste_disposal','has_no_swimming_pool','has_no_reserved_parking','has_no_kids_club6','price','has_no_security','has_vaastu_compliant','has_no_visitor_parking','city_name','date_added','has_no_kids_play_area','has_intercom_facility','per_square_feet_rate','covered_area','locality','has_no_club_house']
data_file.writerow(header)

def processPage(url, propertyId):
	
	print propertyId
	error_file.write('Processing ' + propertyId + '\n')

	attributes = {}
	attributes['id'] = propertyId

	try:
		response = br.open(url)
	except Exception as e:
		error_file.write('Some exception while accessing the property: ' + propertyId + 'having url ' + url + ': ' + str(e) + '\n')
		return

	soup = BeautifulSoup(response)
	f = open('logs/' + propertyId, 'w')
	f.write(str(soup))
	f.close()

	# preliminary data
	try:
		preliminary = soup.find('div', {'class':'nDatabock'})
	except:
		pass
	try:
		temp = preliminary.find('div', {'class' : 'propIDnPDate'}).text.split('|')
		temp = [str(x.split(':')[1].strip()) for x in temp]


		attributes['id'] = temp[0]
		attributes['date_added'] = temp[1].replace("'", '20')
	except:
		pass

	try:
		temp = preliminary.find('div', {'class' : 'priceInfo'}).text.split('\n')
		attributes['apartment_type'] = temp[0].replace('Flat', '').strip()
		attributes['covered_area'] = temp[1].split(' ')[0].strip()
		attributes['built_up_area'] = temp[1].split(' ')[0].strip() # updated this later if it exists
	except:
		pass

	try:
		temp = preliminary.find('div', {'class' : 'nEMIblock'}).text.strip().split('\n')[0].replace('per', '').replace(',', '').replace(u'\u20b9', '').strip()
		attributes['per_square_feet_rate'] = temp
	except:
		pass

	try:
		temp = preliminary.findAll('div', {'class' : 'nActualAmt'})[1].text.replace(u'\u20b9', '').strip().split(' ')
		val = float(temp[0])*( 100000 if temp[1] == 'Lac' else 10000000 )
		attributes['price'] = val
	except:
		pass

	try:
		temp = preliminary.find('div', {'class' : 'nProjNmLoc'}).find('div')

		attributes['locality'] = temp.find('span', {'itemprop' : 'streetAddress'}).text.strip()
		attributes['city_name'] = temp.find('span', {'itemprop' : 'addressLocality'}).text.strip()
	except:
		pass

	try:
		preliminary = preliminary.find('div', {'class' : 'nInfoDataBlock'}).findAll('div', {'class' : 'dataVal'})

		# get some stuff from here, number of rooms etc.
		for x in preliminary:
			for y in x.text.replace('\n', ' ').strip().split(','):
				temp = ''.join([i if ord(i) < 128 else ' ' for i in y])

			# print temp
			# print
	except:
		pass

	try:
		temp = soup.find('div', {'class' : 'nMoreListData'}).findAll('div', {'class' : 'ndataRow'})
		for x in temp:
			dataLabel = x.find('div', {'class' : 'dataLabel'}).text.replace('\n', '').strip()
			if dataLabel == 'Facing':
				attributes['main_entrance_facing'] = x.find('div', {'class' : 'dataVal'}).text.replace('\n', '').strip()
			elif dataLabel == 'Lifts':
				attributes['number_of_lifts'] = x.find('div', {'class' : 'dataVal'}).text.replace('\n', '').strip()
			elif dataLabel == 'Water Availability':
				attributes['water_supply_type'] = x.find('div', {'class' : 'dataVal'}).text.replace('\n', '').strip()
			elif dataLabel == 'Status of Electricity':
				attributes['power_backup_type'] = x.find('div', {'class' : 'dataVal'}).text.replace('\n', '').strip()
			elif dataLabel == 'Area':
				x = x.find('span', {'id' : 'carpetAreaDisplay'})
				attributes['built_up_area'] = x.text.strip()
			elif dataLabel == 'Address':
				x = x.find('div', {'class' : 'dataVal'}).text.replace('\n', '').strip().split(',')
				l = len(x)
				attributes['locality'] = x[l-2]
				attributes['city_name'] = x[l-1]
	except:
		pass

	# amenities section
	try:
		temp = soup.find('div', {'id' : 'normalAminities'}).findAll('li')
		for x in temp:
			y = x.find('span', {'class' : 'ameLabel'}).text.lower()
			z = str('has_' + '_'.join(y.split(' ')))
			if y.startswith('no'):
				attributes[z] = '0'
			else:
				attributes[z] = '1'
	except:
		pass

	output = []

	for key in attributes:
		if key not in header:
			header.append(key)

	for key in header:
		if key not in attributes:
			output.append('-1')
		else:
			output.append(attributes[key])	
	data_file.writerow(output)

def doEverything():
	global currentPageNo
	try:
		response = br.open('http://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Mumbai-Metropolitan-Region&price=Y&pageOption=B')
	except Exception as e:
		print 'Error opening the initial page: ' + str(e)
		sys.exit(1)
	print response.read()
	return	
	while True:
		soup = BeautifulSoup(response)
		divs = soup.findAll('div', {'class':'srpBlock'})

		for div in divs:
			propertyId = div['id']
			propertyId = propertyId[propertyId.rindex('r')+1:]

			onclick = div['onclick']
			indexOfSlash = onclick.index('/')
			indexOfEqual = onclick.index("','")
			accessUrl = baseUrl + onclick[indexOfSlash:indexOfEqual]
			processPage(accessUrl, propertyId)

		# access next page
		print 'Processed page: %s' % currentPageNo
		x = soup.find('a', {'class' : 'toc'})['href']
		if not x:
			break
		else:
			nextPageLink = baseUrl + x

		print nextPageLink

		try:
			response = br.open(nextPageLink)
			currentPageNo += 1
		except Exception as e:
			print 'Unable to open page %s. Stopping!' % currentPageNo
			break

doEverything()
data_file.writerow(header)