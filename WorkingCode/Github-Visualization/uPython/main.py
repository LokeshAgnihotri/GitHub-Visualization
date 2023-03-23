import sys
from uHEC import http_event_collector

# Create event collector object, default SSL and HTTP Event Collector Port
http_event_collector_key_json = "PUTCOLLECTORKEYHERE"
http_event_collector_host = "HOSTNAMEOFTHECOLLECTOR"

testeventJSON = http_event_collector(http_event_collector_key_json, http_event_collector_host)

# Start event payload and add the metadata information
payload = {}
payload.update({"index":"main"})
payload.update({"sourcetype":"txt"})
payload.update({"source":"feather"})
payload.update({"host":"mysterymachine"})

testeventJSON.set_ntp_time()


# Add 5 test events
for i in range(5):
    payload.update({"event":{"action":"success","type":"json","message":"hello world","event_id":i}})
    testeventJSON.sendEvent(payload)

sys.exit(0)
