import threading
import uuid

import flask
from flask import Flask, request
from mitm import Mitm

app = Flask(__name__)


def start(user):
    user.start()

mitmuser = None
user_uuid = None
@app.route("/mitm", methods=["GET", "POST"])#Create the server route with get and post methods
def man_in_the_middle():
    global mitmuser
    global user_uuid
    if request.method == 'POST':
        #if we get stop, we want to stop the proccess.
        stop = request.form.get('stop')
        if stop:
            print(f"Mitmuser: {mitmuser}")
            if mitmuser:
                mitmuser.stop()
                return "Success"
        else:
            #Else we want to create a Mitm object and setart the proccess.
            targetip = request.form.get('targetip')
            router = request.form.get('router')
            if targetip is None or router is None:
                return "Unfortunately we couldn't make this request.\nReason: wrongs args.\nRequests arguments: targetip(String), router(String)"
            user_uuid = str(uuid.uuid1())
            mitmuser = Mitm(targetip, router, user_uuid)
            a = threading.Thread(target=start, args=(mitmuser,))
            a.start()
            return f"task_id:{user_uuid}"
    else:
        if mitmuser is None:
            return "No Attack is running."
        return f"Attack on: {mitmuser.target}"


