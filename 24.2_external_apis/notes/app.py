import requests
term = 'Arctic Monkeys'
# res = requests.get('https://itunes.apple.com/search?term=jack+johnson&limit=2')
res = requests.get('https://itunes.apple.com/search', params ={'term': term,'limit':5})

# lets do something

data = res.json();

for result in data['results']:
    print(result['trackName'])