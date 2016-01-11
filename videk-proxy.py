#!/usr/bin/python

import json
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs
from videk_rest_client import Videk
from datetime import datetime

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
			data['ts'] = datetime.fromtimestamp(measurement["t"]) \
						.isoformat()
			data['latitude'] = measurement["lat"]
			data['longitude'] = measurement["lon"]
			preparedData.append(data)

		x.uploadMesurements(preparedData, node_id, sensor_id)

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		content = self.rfile.read(content_length)
		try:
			data = json.loads(content)

			for sensor in data:
				cluster = sensor["c"]
				node = sensor["n"]
				s_t = sensor["st"]
				s_q = sensor["sq"]
				s_u = sensor["su"]
				measurements = sensor["m"]

				self.upload_data(cluster, node, s_t, s_q, s_u, measurements)
		except:
			pass

		self.send_response(200)

if __name__ == "__main__":
	main()
