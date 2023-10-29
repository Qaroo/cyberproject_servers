
import requests
from bs4 import BeautifulSoup

import uuid
from flask import Flask, render_template,redirect, request

app = Flask(__name__) # obj

def findInfo(carNum):
    #This function do the webscraping
    url = f"https://www.find-car.co.il/car/private/{carNum}"
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    results = ""
    #Its go on all the strong tags in the html of the web and get text from it, append it and returns the list of the appended.
    for x in soup.find_all("strong"):
        print(x.text)
        results += "," + (x.text.replace(" ","").replace("\n", ""))
        #print(x.text.replace(" ",""))
    print("res:" + results)
    return results
    #print(soup)


@app.route("/findcar/<id>", methods=["GET","POST"])
def findcar(id):
    #This server get from the url the car's id and return the findinfo.
    return {"data":findInfo(id)}

if __name__ == "__main__":
    app.run(debug=True,port=80,host="0.0.0.0")
