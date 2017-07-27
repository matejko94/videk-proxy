import requests
import json
import time


url_s = "http://194.249.173.73:11088/reg-s"
url_t = "http://194.249.173.73:11088/reg-t"
url_d = "http://194.249.173.73:11088/data"

sensor_1 = {"c":"ADRIA_s","n":"BeepMislinjaX13","st":"SHT21", \
	"sq":"accuracy-accuracy","su":"m"}

sensor_2 = {"c":"ADRIA_s","n":"BeepMislinjaX13","st":"SHT22", \
	"sq":"temperature","su":"degC"}

sensor_3 = {"c":"ADRIA_s","n":"BeepMislinjaX13","st":"SHT23", \
	"sq":"temperature","su":"degC"}

s1 = requests.post(url_s, data=json.dumps(sensor_1))
#s2 = requests.post(url_s, data=json.dumps(sensor_2))
#s3 = requests.post(url_s, data=json.dumps(sensor_3))

s = s1.text #+ "," + s2.text + "," + s3.text
print s
print s1.headers
#print s2.headers
#print s3.headers

table_data_1 = '{"tb":"' + str(s) + '"}'
#table_data_2 = '{"tb":"9,10,11,12,1"'

def send_table(url, table):
	print table
	t = requests.post(url, data=table)
	print t.text
	print t.headers
	return t.text

table_id_1 = send_table(url_t, table_data_1)

def send_data(url, table, data,time,lat,lon):
	url = url + "?tb=" + table + "&ts=" + str(time) \
	+"&lat="+str(lat) + "&lon="+str(lon)
	d = requests.post(url, data=data)
	print d.text
	print d.headers


import json
from pprint import pprint
import time
import datetime

with open('/home/matej/Desktop/videk-proxy/34-accuracy-accuracy') as data_file:    
    data = json.load(data_file)

for row in data[::-1]:
	print row
	print row["ts"]
	print row["latitude"]
	print row["longitude"]
	print row["value"]
	t=time.mktime(datetime.datetime.strptime(row["ts"], "%Y-%m-%dT%H:%M:%S").timetuple())
	send_data(url_d, table_id_1, str(row["value"]),str(int(t)),row["latitude"],row["longitude"])
	time.sleep(1)


