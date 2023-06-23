# MyQ Synchronous SDK example
A simple Python SDK to interact with MyQ (Chamberlain) Rest API to run simple operations and get information. Utilizing [arraylabs pymyq package](https://github.com/arraylabs/pymyq).

## Setup
First, `pip install -r requirements.txt`.

The `MyQ` class requires environment variables named `MYQ_USER` and `MYQ_PASS` to run. Alternatively, instantiate the class with these parameters. Fill it your individual credentials you use to log in to the MyQ app on your phone.

## Usage
```python
import asyncio

import MyQ


my_q = MyQ()
asyncio.get_event_loop().run_until_complete(my_q.get_garage_doors())
asyncio.get_event_loop().run_until_complete(my_q.open_garage_door('Grass'))
```