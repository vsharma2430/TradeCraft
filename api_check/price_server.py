import requests

r = requests.get('http://localhost:8006/NIFTYBEES.NS/').json()
print(r['ticker'])