import requests
from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

from flask import Flask, render_template, request,make_response, jsonify

from datetime import datetime
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>顏仁駿Python網頁1/3c</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>仁駿簡介網頁</a><br>"
    homepage += "<a href=/account>網頁表單輸入帳密傳值</a><br>"
    homepage += "<a href=/read>讀取FIREBASE資料</a><br>"

    homepage += "<a href=/books>精選圖書列表</a><br>"
    homepage += "<a href=/read>書名查詢</a><br>"
    homepage += "<a href=/spider>網路爬蟲抓取楊子清老師網站的課程</a><br>"
    homepage += "<br><a href=/webhook3>讀取開眼電影即將上映影片，寫入Firestore</a><br>"
    homepage += "<br><a href=/webhookfinalinebot></a><br>"
    return homepage


@app.route("/webhookfinalinebot", methods=["POST"])
def webhookfinalinebot():
    req = request.get_json(force=True)
    action = req.get("queryResult").get("action")
    info = action
    if (action == "zodiaChoice"):
        ZodiacSigns = req.get("queryResult").get("parameters").get("ZodiacSigns")
        info = "您選擇的星座是:" + ZodiacSigns +"，星座運勢：\n"

        db = firestore.client()
        collection_ref = db.collection("星座")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if ZodiacSigns in dict["title"]:
                result += "星座名：" + dict["title"] + "\n"
                result += "運勢：" + dict["hyperlink"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
    app.run(debug=True)