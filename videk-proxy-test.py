import unittest
import requests

class VidekProxyTests(unittest.TestCase):

	def setUp(self):
		self.url_s = "http://localhost:8080/reg-s"
		self.url_t = "http://localhost:8080/reg-t"
		self.url_d = "http://localhost:8080/data"

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
