import Adafruit_DHT as dht
h, t = dht.read_retry(dht.DHT22, 5)

print "Hum: " + str(h)
print type(h)
print "Temp: " + str(t)
print type(t)

