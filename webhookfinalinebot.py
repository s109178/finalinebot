@app.route("/webhookfinalinebot", methods=["POST"])
def webhook3():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "zodiaChoice"):
        ZodiacSigns =  req.get("queryResult").get("parameters").get("ZodiacSigns")
        info = "我是星座聊天機器人,您選擇的星座是：" + ZodiacSigns + "，星座運勢：\n"

        db = firestore.client()
        collection_ref = db.collection("電影含分級")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if ZodiacSigns in dict["ZodiacSigns"]:
                result += "星座塔羅 | 柯夢波丹 Cosmopolitan Taiwan：" + dict["title"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n\n"
        info += result
    return make_response(jsonify({"fulfillmentText": info}))

#<a href="/tw/horoscopes/today/a32681177/aries-today/" label data-vars-cta="今日運勢" data-vars-ga-position="1" data-vars-ga-call-to-action="牡羊座今日運勢" data-vars-ga-outbound-link="https://www.cosmopolitan.com/tw/horoscopes/today/a32681177/aries-today/" class=" enk2x9t2 css-2yv34j e1c1bym14">
  #<style data-emotion="css 1eq4igh">.css-1eq4igh{display:block;margin-bottom:0;}.css-1eq4igh img{vertical-align:top;}</style>
  #<div data-vars-cta="今日運勢" data-vars-ga-position="1" data-vars-ga-call-to-action="牡羊座今日運勢" data-vars-ga-outbound-link="https://www.cosmopolitan.com/tw/horoscopes/today/a32681177/aries-today/" class="css-1eq4igh enk2x9t1">
    #<img src="https://hips.hearstapps.com/hmg-prod/images/daily-aries-1638434028.png?crop=0.329xw:0.985xh;0,0&amp;resize=360:*" alt="牡羊座今日運勢" title="牡羊座今日運勢" width="100%" height="auto" decoding="async" loading="lazy"/>
  #</div>
  #<style data-emotion="css azqqz2">
#</a>