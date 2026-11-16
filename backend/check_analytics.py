import requests

url = "http://127.0.0.1:8000/api/v1/stocks/RELIANCE/analytics"

response = requests.get(url, params={"limit": 250})
response.raise_for_status()

result = response.json()
records = result["data"]

print("20th Record:")
print(records[19])

print("\n50th Record:")
print(records[49])

print("\nLast Record:")
print(records[-1])