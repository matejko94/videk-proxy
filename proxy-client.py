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

s1 = requests.post(url_s, data=json.dumps(sensor_1)).text
s2 = requests.post(url_s, data=json.dumps(sensor_2)).text
s3 = requests.post(url_s, data=json.dumps(sensor_3)).text

s = s1+","+s2+","+s3
print s

table_data = {"tb":s}
t = requests.post(url_t, data=json.dumps(table_data)).text
print t

d = "11,22,33.9"
time = str(int(time.time()))
url_d = url_d + "?tb=" + t + "&ts=" + time + \
	"&lat=46.056947" + "&lon=14.505751"
d = requests.post(url_d, data=d).text
print d
