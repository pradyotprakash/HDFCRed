import json, csv, math
from urllib2 import urlopen
from sklearn.ensemble import BaggingRegressor

def getPlace(lat, lon):
	url = "http://maps.googleapis.com/maps/api/geocode/json?"
	url += "latlng=%s,%s&sensor=false" % (lat, lon)
	v = urlopen(url).read()
	j = json.loads(v)

	components = j['results'][0]['address_components']
	country = town = None
   
	for c in components:
		if "country" in c['types']:
			country = c['long_name']
		if "administrative_area_level_2" in c['types']:
			town = c['long_name']
	
	return (str(town), str(country))

def getXYZ(lat, lon):
	R = float(6371.0)
	
	lat = float(lat)*math.pi/180.0
	lon = float(lon)*math.pi/180.0

	x = R * math.cos(lat) * math.cos(lon)
	y = R * math.cos(lat) * math.sin(lon)
	z = R * math.sin(lat)

	return (x, y, z)

def weightF(p, q, r):
	p = map(float, p)
	q = map(float, q)

	x = 0.0
	for i in range(len(p)):
		x += ((p[i]) - (q[i]))**2

	x = math.sqrt(x)
	x = x/r
	
	if x > 1 or x <= 0.0:
		return False
	else:
		return True

def createTest(params):
	
	# convert lat, long to x, y, z
	temp = getXYZ(params['lat'], params['long'])
	params['x'] = temp[0]
	params['y'] = temp[1]
	params['z'] = temp[2]

	head = ['x','y','z','floor_count','floor_number','apartment_type','age_of_property','main_entrance_facing','built_up_area','bedroom_count','bathroom_count','has_swimming_pool','has_gym','number_of_lifts','parking_count','has_gas_pipeline','has_servant_room','power_backup_type','is_gated_community','security_type']
	attributeList = ['apartment_type', 'security_type', 'power_backup_type', 'main_entrance_facing']

	# read the attribute file
	attributeMap = eval(open('../../../data/attributeMap').read())

	test = [None]*len(head)

	i = 0
	for key in head:
		if key in params:
			test[i] = params[key]
		i += 1	

	for attribute in attributeList:
		index = head.index(attribute)
		test[index] = attributeMap[attribute][test[index]]

	return test	

def avmPredict(params):
	town = getPlace(params['lat'], params['long'])[0]

	x, y, z = getXYZ(params['lat'], params['long'])

	r = 1.0

	data = []
	target = []
	header = []

	with open('../../../data/working22.csv') as f:
	
		f = csv.reader(f)
		header = next(f)

		for row in f:
			t = (map(float, row[:3] + row[4:]), float(row[3]))

			if weightF([x, y, z], t[0][0:3], r):
				data.append(t[0])
				target.append(t[1])

	ensemble = BaggingRegressor()
	ensemble.fit(data, target)

	test = createTest(params)
	return ensemble.predict(test)

if __name__ == '__main__':
	params = {'lat':'19.171807','long':'72.960542','floor_count':'4','floor_number':'3','apartment_type':'1 BHK','age_of_property':'3','main_entrance_facing':'North-East','built_up_area':'450','bedroom_count':'1','bathroom_count':'1','has_swimming_pool':'0','has_gym':'0','number_of_lifts':'0','parking_count':'1','has_gas_pipeline':'0','has_servant_room':'0','power_backup_type':'None','is_gated_community':'0','security_type':'None'}
	print avmPredict(params)