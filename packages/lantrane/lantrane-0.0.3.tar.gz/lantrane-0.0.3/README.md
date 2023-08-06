# Lantrane

A python library for interacting with Trane thermostats over the local network


## Usage Example
Your thermostat for communicating, variable speed heat pump systems might have a port open that emits data every time the compressor speed changes if you can find the right port via nmap and telnet (usually port 30,000 or so), this example will listen on that port and give you data. The port may change when the device is updated though.

```python
from lantrane import Trane
import asyncio

async def read_async():
	async for data in Trane(args.ip, args.port).listen():
	print(data)

asyncio.run(read_async())
```



## Distribution

```
python3 setup.py bdist_wheel
python3 setup.py sdist
twine check dist/*
twine upload dist/*
```