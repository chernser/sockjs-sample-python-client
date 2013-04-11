from client.Client import Client
import time

client = Client('/socket.io', "localhost", 9999)
client.connect()

time.sleep(5)

if client.send("{ \"value\": 123}"):
    print "Message sent"

if client.send("\"echome\""):
    print "Echo message sent"


client.disconnect()



