from bs4 import BeautifulSoup
import json, mechanize, sys
import csv

current_page_no = 1

br = mechanize.Browser()
br.set_handle_robots(False)

header = ['id','latitude','longitude','price','city_name','locality','per_square_feet_rate','floor_count','floor_number','property_type','under_construction','date_added','available_from','apartment_type','age_of_property','age_of_property_date','main_entrance_facing','status','built_up_area','bedroom_count','bathroom_count','has_swimming_pool','has_gym','number_of_lifts','parking_count','has_gas_pipeline','water_supply_type','has_servant_room','power_backup_type','is_gated_community','security_type','is_society_formed','region_name','neighbourhood_score']

try:
	response = br.open("https://housing.com/in/buy/mumbai/mumbai")
except:
	print 'Unable to connect to housing. Check internet connection.'
	sys.exit(1)

data_file = csv.writer(open('training_data', 'a'))

data_file.writerow(header)

dataIdAccessUrl = 'https://rails.housing.com//api/v2/buy/'
error_file = open('error_logs', 'a')

def parseDataIds(data_ids):
	
	for data_id in data_ids:
		try:
			response = br.open(dataIdAccessUrl + data_id)
		except Exception as e:
			error_file.write('Unable to open page for id: ' + str(data_id))
			continue	

		json_data = response.read()
		
		f = open('logs/' + data_id, 'w')
		f.write(json_data)

		data = {}
		try:
			data = json.loads(json_data)['result']
		except Exception as e:
			error_file.write('Exception ' + str(e) + ' while accessing entry ' + str(data_id) + ' on page ' + str(current_page_no) + '\n')
		
		output = []

		if 'id' in data:
			output.append(str(data['id']))
		else:
			output.append(str('-1'))

		if 'latitude' in data:
			output.append(str(data['latitude']))
		else:
			output.append(str('-1'))

		if 'longitude' in data:
			output.append(str(data['longitude']))
		else:
			output.append(str('-1'))

		if 'price' in data:
			output.append(str(data['price']))
		else:
			output.append(str('-1'))

		if 'city_name' in data:
			output.append(str(data['city_name']))
		else:
			output.append(str('-1'))

		if 'locality' in data:
			output.append(str(data['locality']))
		else:
			output.append(str('-1'))

		if 'per_square_feet_rate' in data:
			output.append(str(data['per_square_feet_rate']))
		else:
			output.append(str('-1'))

		if 'floor_count' in data:
			output.append(str(data['floor_count']))
		else:
			output.append(str('-1'))

		if 'floor_number' in data:
			output.append(str(data['floor_number']))
		else:
			output.append(str('-1'))

		if 'property_type' in data:
			output.append(str(data['property_type']))
		else:
			output.append(str('-1'))

		if 'under_construction' in data:
			output.append(str(data['under_construction']))
		else:
			output.append(str('-1'))			

		if 'date_added' in data:
			output.append(str(data['date_added']))
		else:
			output.append(str('-1'))

		if 'available_from' in data:
			output.append(str(data['available_from']))
		else:
			output.append(str('-1'))	

		if 'apartment_type' in data:
			output.append(str(data['apartment_type']))
		else:
			output.append(str('-1'))

		if 'age_of_property' in data:
			output.append(str(data['age_of_property']))
		else:
			output.append(str('-1'))		

		if 'age_of_property_date' in data:
			output.append(str(data['age_of_property_date']))
		else:
			output.append(str('-1'))

		if 'main_entrance_facing' in data:
			output.append(str(data['main_entrance_facing']))
		else:
			output.append(str('0'))

		if 'status' in data:
			output.append(str(data['status']))
		else:
			output.append(str('-1'))
			
		if 'built_up_area' in data:
			output.append(str(data['built_up_area']))
		else:
			output.append(str('-1'))

		if 'bedroom_count' in data:
			output.append(str(data['bedroom_count']))
		else:
			output.append(str('-1'))

		if 'bathroom_count' in data:
			output.append(str(data['bathroom_count']))
		else:
			output.append(str('-1'))

		if 'has_swimming_pool' in data:
			output.append(str(data['has_swimming_pool']))
		else:
			output.append(str('0'))

		if 'has_gym' in data:
			output.append(str(data['has_gym']))
		else:
			output.append(str('0'))

		if 'number_of_lifts' in data:
			output.append(str(data['number_of_lifts']))
		else:
			output.append(str('0'))

		if 'parking_count' in data:
			output.append(str(data['parking_count']))
		else:
			output.append(str('0'))

		if 'has_gas_pipeline' in data:
			output.append(str(data['has_gas_pipeline']))
		else:
			output.append(str('0'))

		if 'water_supply_type' in data:
			output.append(str(data['water_supply_type']))
		else:
			output.append(str('-1'))

		if 'has_servant_room' in data:
			output.append(str(data['has_servant_room']))
		else:
			output.append(str('0'))

		if 'power_backup_type' in data:
			output.append(str(data['power_backup_type']))
		else:
			output.append(str('-1'))

		if 'is_gated_community' in data:
			output.append(str(data['is_gated_community']))
		else:
			output.append(str('0'))

		if 'security_type' in data:
			output.append(str(data['security_type']))
		else:
			output.append(str('-1'))
		
		if 'is_society_formed' in data:
			output.append(str(data['is_society_formed']))
		else:
			output.append(str('-1'))			

		if 'region_name' in data:
			output.append(str(data['region_name']))
		else:
			output.append(str('-1'))

		if 'neighbourhood_score' in data:
			output.append(str(data['neighbourhood_score']))
		else:
			output.append(str('-1'))

		output = [x.replace('False', '0') for x in output]
		output = [x.replace('True', '1') for x in output]

		data_file.writerow(output)

while True:
	soup = BeautifulSoup(response)

	divs = soup.findAll('div', {'class' : 'list-resale'})

	if not len(divs) == 0:

		data_ids = []

		for div in divs:
			data_ids.append(div['data-id'])

		parseDataIds(data_ids)
		print 'Received page: ' + str(current_page_no) + '. Total entries so far: ' + str(current_page_no*len(data_ids))
		
		# breaking condition
		status_div_strong = soup.findAll('div', {'class' : 'status-bar'})[0].findAll('strong')

		# print status_div_strong[0].text, status_div_strong[1].text, status_div_strong[2]self.text
		if int(status_div_strong[1].text) >= int(status_div_strong[2].text):
			break
	else:
		error_file.write('No data on page ' + str(current_page_no) + '. Skipping it!\n')

	current_page_no += 1
	try:
		response = br.open('https://housing.com/in/buy/mumbai/mumbai?page=' + str(current_page_no))
	except:
		print 'Unable to retrieve page %s. Stopped.' % str(current_page_no)