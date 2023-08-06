import socket
from .data import ThermostatData

class Trane:

	def __init__(self, timeout=socket._GLOBAL_DEFAULT_TIMEOUT):

		self.timeout = timeout

	def listen(self, host=None, port=0, bufsize=128):
		# set up TCP socket
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		sock.connect((host, port))
		# print(f"Connected to {self.ip}:{self.port}")
		try:
			while True:
				data = sock.recv(bufsize)
				if not data:
					break
				# strip newline and trailing null
				data = data[:-2]
				yield ThermostatData.from_data(data)
		finally:
			sock.close()