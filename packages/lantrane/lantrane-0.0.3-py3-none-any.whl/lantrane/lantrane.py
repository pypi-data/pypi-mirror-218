import socket
import asyncio
from .data import ThermostatData

class Trane:

	def __init__(self, host: str, port:int):#timeout=socket._GLOBAL_DEFAULT_TIMEOUT
		self.host = host
		self.port = port
		# self.timeout = timeout

	def validate(self):
		"""Validates whether the given host and port can be connected to.

		Returns:
			bool: whether or not the given host and port could successfully connect
		"""
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((self.host, self.port))
		except ConnectionRefusedError:
			return False
		finally:
			sock.close()
		
		return True

	async def listen(self, bufsize=128):

		# Register the open socket to wait for data.
		reader, writer = await asyncio.open_connection(host=self.host, port=self.port, family=socket.AF_INET)
		# sock=rsock,

		# print(f"Connected to {self.ip}:{self.port}")
		try:
			while True:
				data = await reader.read(bufsize)
				if not data:
					break
				# strip newline and trailing null
				data = data[:-2]
				yield ThermostatData.from_data(data)
		except (TimeoutError, ConnectionAbortedError, ConnectionResetError) as e:
			# sockets generally either time out, close, or reset.
			# https://stackoverflow.com/a/15175067/
			print("Connection Error")
			print(e)
		finally:
			writer.close()
			await writer.wait_closed()