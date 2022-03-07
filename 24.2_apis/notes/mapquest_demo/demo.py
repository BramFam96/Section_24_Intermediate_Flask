import requests
from secret import mq_key

res = requests.get('http://www.mapquestapi.com/geocoding/v1/address',
                params = {'key': mq_key, 'location': 'Denver, CO'})