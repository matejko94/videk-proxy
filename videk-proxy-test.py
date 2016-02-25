import unittest
import requests

class VidekProxyTests(unittest.TestCase):

	def setUp(self):
		#url = "http://194.249.173.73:11088"
		url = "http://LOCALHOST:8080"
		self.url_s = url + "/reg-s"
		self.url_t = url + "/reg-t"
		self.url_d = url + "/data"

	def test_correct_sensor_registration(self):
		correct_sensor = '{"c":"Beep","n":"BeepMislinjaX","st":"SHT21", \
						"sq":"temperature","su":"degC"}'
		response = requests.post(self.url_s, data=correct_sensor)
		self.assertTrue(isinstance(int(response.text), int))

	def test_broken_sensor_registration(self):
		broken_sensor = '{"c":"Beep","n":"BeepMislinjaX","st":"SHT21", \
						"sq":"temperature","su":"deg'
		response = requests.post(self.url_s, data=broken_sensor)
		self.assertEqual("Error: Wrong data format!", response.text)

	def test_correct_table_registration(self):
		correct_sensor = '{"c":"Beep","n":"BeepMislinjaX","st":"SHT21", \
						"sq":"temperature","su":"degC"}'
		response = requests.post(self.url_s, data=correct_sensor)
		correct_table = '{"tb":"' + response.text + '"}'
		response = requests.post(self.url_t, data=correct_table)
		self.assertTrue(isinstance(int(response.text), int))

	def test_broken_table_registration(self):
		broken_table = '{"tb":"9,10,11,12,1"'
		response = requests.post(self.url_t, data=broken_table)
		self.assertEqual("Error: Wrong data format!", response.text)

if __name__ == '__main__':
	unittest.main()
