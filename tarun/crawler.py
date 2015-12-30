import mechanize, json, csv, math

R = 6371.0

def getXYZ(lat, lon):
	lat = lat*math.pi/180
	lon = lon*math.pi/180
	
	x = R * math.cos(lat) * math.cos(lon)
	y = R * math.cos(lat) * math.sin(lon)
	z = R * math.sin(lat)

	return [x, y, z]

def distance(lat1, lon1, lat2, lon2):
	p1 = getXYZ(lat1, lon1)
	p2 = getXYZ(lat2, lon2)

	return math.sqrt(sum([(a-b)**2 for a,b in zip(p1, p2)]))

def getter(latitude, longitude, radius, type_, APIKey, f):
	
	browser = mechanize.Browser()
	browser.set_handle_robots(False)

	queryString = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
	
	parameters = {}
	parameters['location'] = latitude + ',' + longitude
	parameters['radius'] = str(radius)
	parameters['type'] = type_
	parameters['key'] = APIKey

	for key, value in parameters.items():
		queryString += key + '=' + value + '&'
	
	print queryString
	response = browser.open(queryString[:len(queryString)-1])
	results = json.loads(response.read())['results']
	
	count = 0
	for result in results:
		count += 1
		lat = float(result['geometry']['location']['lat'])
		lng = float(result['geometry']['location']['lng'])

		l = [result['name'], distance(float(latitude), float(longitude), lat, lng)]
		# f.writerow(l)
	f.writerow([latitude, longitude, type_, count])
		
f = csv.writer(open('data.csv', 'a'))
getter('19.13105', '72.90767', 500, 'food', 'AIzaSyBLdHwDMmlqX-eAcM_gCDsmaTFAXZJF8uQ', f)

# food, 