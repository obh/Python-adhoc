#!/bin/python

import requests

# Where USD is the base currency you want to use
url = 'https://v6.exchangerate-api.com/v6/a3c32622a3a3df6a5c2cd430/history/USD/2021/09/27/1'

# Making our request
response = requests.get(url)
data = response.json()

# Your JSON object
print(data)
