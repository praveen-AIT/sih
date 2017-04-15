import urllib2 
import json
url1="https://api.thingspeak.com/update?api_key=4QWC6Z9XNBKLLAVR&field1="
url2="https://api.thingspeak.com/update?api_key=P5RSD0I5UZOWKUK8&field1="

READ_API_KEY='4URK7ED8A5C50CI5'
CHANNEL_ID=168317

conn = urllib2.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s"% (CHANNEL_ID,READ_API_KEY))
response = conn.read()
print "http status code=%s" % (conn.getcode())
data=json.loads(response)
lat = data['field1']
lon = data['field2']

print lat,lon;



predicted = 1000
urllib2.urlopen("https://api.thingspeak.com/update?api_key=KC4993A8IONGFH1U&field1=%f"% (predicted))


"""
Chat conversation end
"""