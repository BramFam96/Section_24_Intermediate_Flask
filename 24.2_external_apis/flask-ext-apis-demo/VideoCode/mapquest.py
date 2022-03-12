import requests
from secrets import MQ_KEY as key


response = requests.get('http://www.mapquestapi.com/geocoding/v1/address',
                        params={'key': key, 'location': '123 Main St.'})
