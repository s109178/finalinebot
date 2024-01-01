import requests, json
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request,make_response, jsonify

from datetime import datetime


app = Flask(name)


@app.route("/webhookfinalinebot", methods=["POST"])
def webhookfinalinebot():
    req = request.get_json(force=True)
    action = req.get("queryResult").get("action")

    if action == "zodiaChoice":
        ZodiacSigns = req.get("queryResult").get("parameters").get("ZodiacSigns")
        info = f"您選擇的星座是：{ZodiacSigns}，星座運勢：\n"

        url = "https://www.cosmopolitan.com/tw/horoscopes/today/"
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # 此處需要修改為JSON-LD資料中提供的星座URL
            # 假設星座資訊在<div class="your-class">裡面
            zodiac_info = soup.find("div", class_="your-class").text
            info += zodiac_info

    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run(debug=True)
