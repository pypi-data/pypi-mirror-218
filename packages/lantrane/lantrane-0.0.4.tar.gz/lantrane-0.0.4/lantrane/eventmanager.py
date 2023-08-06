from typing import Callable


class EventManager:
	"""inftastructure for managing events and callbacks
	
	Based on https://github.com/home-assistant-libs/zwave-js-server-python/blob/master/zwave_js_server/event.py
	"""

	def __init__(self) -> None:
		"""Initialize event base."""
		self._listeners: dict[str, list[Callable]] = {}

	def on(
		self, event_name: str, callback: Callable
	) -> Callable:
		"""Register an event callback."""
		listeners: list = self._listeners.setdefault(event_name, [])
		listeners.append(callback)

		def unsubscribe() -> None:
			"""Unsubscribe listeners."""
			if callback in listeners:
				listeners.remove(callback)

	def emit(self, event_name: str, data: object) -> None:
		"""Run all callbacks for an event."""
		for listener in self._listeners.get(event_name, []).copy():
			listener(data)