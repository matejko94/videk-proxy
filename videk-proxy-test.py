import requests
import json
import time

url_s = "http://localhost:8080/reg-s"
url_t = "http://localhost:8080/reg-t"
url_d = "http://localhost:8080/data"

sensor_1 = {"c":"Beep","n":"BeepMislinjaX","st":"SHT21", \
	"sq":"temperature","su":"degC"}

sensor_2 = {"c":"Beep","n":"BeepMislinjaX","st":"SHT22", \
	"sq":"temperature","su":"degC"}

sensor_3 = {"c":"Beep","n":"BeepMislinjaX","st":"SHT23", \
	"sq":"temperature","su":"degC"}

s1 = requests.post(url_s, data=json.dumps(sensor_1))
s2 = requests.post(url_s, data=json.dumps(sensor_2))
s3 = requests.post(url_s, data=json.dumps(sensor_3))

s = s1.text + "," + s2.text + "," + s3.text
print s
print s1.headers
print s2.headers
print s3.headers

table_data_1 = '{"tb":"' + str(s) + '"}'
table_data_2 = '{"tb":"9,10,11,12,1"'

def send_table(url, table):
	print table
	t = requests.post(url, data=table)
	print t.text
	print t.headers
	return t.text

table_id_1 = send_table(url_t, table_data_1)
table_id_2 = send_table(url_t, table_data_2)

test_data_1 = "1,2,3\n4,5,6\n7,8,9.122"
test_data_2 = "AT#HTTPCFG?.AT#HTTPCFG?.AT#HTTPCFG?.AT#H"
test_data_3 = "0.1,nan,0.2"

def send_data(url, table, data):
	local_time = str(int(time.time()))
	url = url + "?tb=" + table + "&ts=" + local_time + \
		"&lat=46.056947" + "&lon=14.505751"
	d = requests.post(url, data=data)
	print d.text
	print d.headers

send_data(url_d, table_id_1, test_data_1)
send_data(url_d, table_id_1, test_data_2)
send_data(url_d, table_id_1, test_data_3)
