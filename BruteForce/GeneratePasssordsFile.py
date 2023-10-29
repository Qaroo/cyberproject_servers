import ast
import random
from flask import Flask, request
import itertools

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def generate_password():
    if request.method == 'POST':
        keywords = request.form.getlist('keywords')
        print(f"keywords: {keywords}")
        if keywords is None or len(keywords) == 0:
            return "Syntax Error: Couldnt reach keywords list. Request Body should be:\nkeywords: List(String)"
        passwords = generate_passwords(keywords)
        return {"passwords": passwords}
    else:
        return "This server only gets POST requests method."


def generate_passwords(keywords):
    combinations = []
    final = []
    for r in range(len(keywords) + 1):
        for combination in itertools.combinations(keywords, r):
            combinations.append(combination)
    for c in combinations:
        word = ""
        for words in c:
            word += words
        final.append(word)

    file = open("passwords.txt", "w")
    for password in final:
        file.write(f"{password}\n")
    return final


app.run()