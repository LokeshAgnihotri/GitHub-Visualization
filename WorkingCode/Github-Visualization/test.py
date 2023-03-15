from splunk_http_event_collector import http_event_collector 
import json
import logging
import sys

token = "f6a91647-602a-4309-8ec7-ad5a46e53839"
server_uri = "https://prd-p-ngvek.splunkcloud.com"

hec = http_event_collector(token=token, http_event_server=server_uri)

# Sample JSON structure
json_data = {
    "name": "John",
    "age": 30,
    "city": "New York"
}

# Create the event data
event_data = {
    "event": json.dumps(json_data),
    "sourcetype": "my_event_type"
}

response = hec.sendEvent(event_data)
print(response)
