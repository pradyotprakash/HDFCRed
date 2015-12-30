from bs4 import BeautifulSoup
import json, mechanize, datetime, csv

browser = mechanize.Browser()
browser.set_handle_robots(False)

soup = BeautifulSoup(browser.open('http://safar.tropmet.res.in/map_data.php?city_id=2&for=current'))
scriptTags = soup.findAll('script')

c = 0
d = {}
for script in scriptTags:
	text = script.text
	if 'var markers' in text:
		soup = BeautifulSoup(text)
		
		relevantTables = soup.findAll('table')

		for i in range(0, len(relevantTables), 2):
			location = str(relevantTables[i].find('tr').find('td').text)

			innerTable = relevantTables[i+1]
			trs = innerTable.findAll('tr')
			y = []
			for i in range(1, len(trs)):
				l = []
				for td in trs[i].findAll('td'):
					l.append(str(td.text))
				y.append(l[0:2])
			d[location] = y

writeData = str(datetime.datetime.now()) + '__' + str(d) + '\n'
f = csv.writer(open('pollutionData.csv', 'a'))

now = datetime.datetime.now()
for key in d:
	for v in d[key]:
		f.writerow([now, key] + v)