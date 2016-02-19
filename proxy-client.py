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

res = requests.post(url_s+"test", data=json.dumps(sensor_1))
print res
print res.headers

#s1 = requests.post(url_s, data=json.dumps(sensor_1))
#s2 = requests.post(url_s, data=json.dumps(sensor_2))
#s3 = requests.post(url_s, data=json.dumps(sensor_3))

#s = s1.text + "," + s2.text + "," + s3.text
#print s
#print s1.headers
#print s2.headers
#print s3.headers

#table_data = {"tb":str(s)}
#t = requests.post(url_t, data=json.dumps(table_data))
#print t.text
#print t.headers

#d = "1,2,3\n4,5,6\n7,8,9.122"
#time = str(int(time.time()))
#url_d = url_d + "?tb=" + t.text + "&ts=" + time + \
#	"&lat=46.056947" + "&lon=14.505751"
#d = requests.post(url_d, data=d)
#print d.text
#print d.headers
