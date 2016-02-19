#!/usr/bin/python

import json
import csv
import StringIO
import numpy as np
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from videk_rest_client import Videk
from datetime import datetime
from proxydatabase import ProxyDatabase

server_port = 8080
videk_api_url = "http://localhost:3000/api"
videk_token = "yc92PyLkeBUyqN1msDan6YOCl+IT2u9M"

def main():

	try:
		server = HTTPServer(('', server_port), requestHandler)
		print "Started http server on port " + str(server_port)
		server.serve_forever()

	except KeyboardInterrupt:
		print "Shutting down the server"
		server.socket.close()

class requestHandler(BaseHTTPRequestHandler):

	sensor = ProxyDatabase("sensors")
	table = ProxyDatabase("tables")

	def upload_data(self, cluster, node, sensor_t, \
					sensor_q, sensor_u, measurements):

		x = Videk(videk_token)
		x.api_url = videk_api_url

		cluster_id = x.getClusterID(cluster)
		if cluster_id == None:
			x.createCluster(cluster)
			cluster_id = x.getClusterID(cluster)

		node_id = x.getNodeID(node)
		if node_id == None:
			x.createNode(node, cluster_id)
			node_id = x.getNodeID(node)

		sensor_id = x.getSensorID(node, sensor_t, sensor_q)
		if sensor_id == None:
			x.createSensor(node_id, sensor_t, sensor_q, sensor_u)
			sensor_id = x.getSensorID(node, sensor_t, sensor_q)

		videk_m = '''{"latitude":"","longitude":"","ts":"","value":""}'''

		preparedData = []
		for measurement in measurements:
			data = json.loads(videk_m)
			data['value'] = measurement["v"]
			data['ts'] = datetime.fromtimestamp(int(measurement["t"])) \
				.isoformat()
			data['latitude'] = measurement["lat"]
			data['longitude'] = measurement["lon"]
			preparedData.append(data)

		x.uploadMesurements(preparedData, node_id, sensor_id)

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		content = self.rfile.read(content_length)
		url = urlparse(self.path)
		resource = url.path
		params = parse_qs(url.query)

		if resource == "/reg-s":
			message = self.sensor.store(content)
			self.send_response(200)
			self.send_header('Content-Length', len(str(message)))
			self.end_headers()
			self.wfile.write(message)
			return

		if resource == "/reg-t":
			message = self.table.store(content)
			self.send_response(200)
			self.send_header('Content-Length', len(str(message)))
			self.end_headers()
			self.wfile.write(message)
			return

		if resource == "/data":
			t_id = self.table.get(params["tb"][0])
			if t_id != "null":
				tcsv = json.loads(t_id).get("tb")
			else:
				message = "Error: No such table!"
				self.send_response(200)
				self.send_header('Content-Length', len(message))
				self.end_headers()
				self.wfile.write(message)
				return

			tarray = tcsv.split(",")
			f = StringIO.StringIO(content)
			reader = csv.reader(f, delimiter=',')
			sensor_csv = np.array(list(reader)).T

			m = {"t":params["ts"][0],"lat":params["lat"][0], \
				"lon":params["lon"][0],"v":""}
			m_a = []
			videk_json = []
			for t, c in zip(tarray, sensor_csv):
				s_id = self.sensor.get(t)
				if s_id != "null":
					sensor = json.loads(s_id)
				else:
					message = "Error: No such sensor!"
					self.send_response(200)
					self.send_header('Content-Length', len(message))
					self.end_headers()
					self.wfile.write(message)
					return

				for sv in c:
					m["v"] = float(sv)
					m_a.append(m)
					m = {"t":params["ts"][0],"lat":params["lat"][0], \
						"lon":params["lon"][0],"v":""}
				sensor["m"] = m_a
				videk_json.append(sensor)
				m_a = []

			data = videk_json
			for sensor in data:
				cluster = sensor["c"]
				node = sensor["n"]
				s_t = sensor["st"]
				s_q = sensor["sq"]
				s_u = sensor["su"]
				measurements = sensor["m"]
				self.upload_data(cluster, node, s_t, s_q, s_u, measurements)

			message = "done"
			self.send_response(200)
			self.send_header('Content-Length', len(message))
			self.end_headers()
			self.wfile.write(message)
			return

		message = "Resource not found!"
		self.send_response(404)
		self.send_header('Content-Length', len(message))
		self.end_headers()
		self.wfile.write(message)
		return

if __name__ == "__main__":
	main()
