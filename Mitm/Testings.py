import time

import requests
from mitm import Mitm
input("Type RUN for run\n")
#response = requests.post("http://172.20.137.32:3265/mitm", data={"targetip":"172.20.151.216", "router":"172.20.159.254"})
#response = requests.post("http://127.0.0.1:3005/mitm", data={"stop":True})
#print(response.text)

#Mitm.get_mac("192.168.1.1")

m = Mitm("172.20.151.216", "172.20.159.254", "aaa")
m.start()
time.sleep(10)
m.stop()