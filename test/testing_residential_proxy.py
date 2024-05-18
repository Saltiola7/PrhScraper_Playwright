import pprint
import requests


host = 'brd.superproxy.io'
port = 22225

username = 'brd-customer-hl_91c8167a-zone-residential_proxy_prh'
password = 'jczpq3hmd6ic'


proxy_url = f'http://{username}:{password}@{host}:{port}'

proxies = {
    'http': proxy_url,
    'https': proxy_url
}


url = "https://virre.prh.fi"
response = requests.get(url, proxies=proxies)
pprint.pprint(response.json())
pprint.pprint(response.json())