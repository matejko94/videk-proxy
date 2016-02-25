import unittest
import requests
import socket
import time
import threading
from multiprocessing import Process

class BlockingClient:

	def run(self, message):
		s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(("localhost",8080))
		s.send("POST /reg-s HTTP/1.1\n")
		s.send("Content-Length: " + str(len(message)) + "\n\n")
		time.sleep(10)
		s.send(message)
		while True:
			resp = s.recv(1024)
			if resp == "": break
			print resp,
		s.close()

class VidekProxyTests(unittest.TestCase):

	def setUp(self):
		url = "http://localhost:8080"
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

	def test_client_hang(self):
		message = '{"c":"Beep","n":"BeepMislinjaX","st":"SHT21", \
						"sq":"temperature","su":"degC"}'
		threading.Thread(target=BlockingClient().run, args=(message,)).start()
		response = requests.post(self.url_s, data=message)
		self.assertTrue(isinstance(int(response.text), int))

if __name__ == '__main__':
	unittest.main()
