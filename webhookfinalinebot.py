import requests,json
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request,make_response, jsonify

from datetime import datetime


app = Flask(__name__)


@app.route("/webhookfinalinebot", methods=["POST"])
def webhookfinalinebot():
    req = request.get_json(force=True)
    action = req.get("queryResult").get("action")

    if (action == "zodiaChoice"):
        ZodiacSigns = req.get("queryResult").get("parameters").get("ZodiacSigns")
        info = "您選擇的星座是:" + ZodiacSigns +"，星座運勢：\n"

        db = firestore.client()
        collection_ref = db.collection("星座")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if ZodiacSigns in dict["ZodiacSigns"]:
                result += "星座名：" + dict["title"] + "\n"
                result += "運勢：" + dict["hyperlink"] + "\n\n"
        info += result
    
        

    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run(debug=True)
