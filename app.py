from flask import *
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2021",
    database="mydatabase",
    buffered=True
)


mycursor = mydb.cursor()


# Pages
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")

@app.route("/api/attractions")
def api_attractions():
    page=request.args.get("page")
    page=int(page)*12
    # page=str(page)
    print(page)
    keyword=request.args.get("keyword")
    nextpage=(319-page)//12
    print(nextpage)
    print(type(nextpage))
    #這裡是只有page存在的時候發生的條件
    if keyword==None:
        #用f字串要加上{}讓他的型態改變
        mycursor.execute(f"SELECT  * FROM power  limit 12 offset {page}")
        result=mycursor.fetchall()
        # print('type(result): ', type(result))
        # print(result)
        if result!=None:
            myseclist=[]
            for i in range(0,12):
                want={
                "id":result[i][0],
                "name":result[i][1],
                "category":result[i][2],
                "description":result[i][3],
                "address":result[i][4],
                "transport":result[i][5],
                "mrt":result[i][6],
                "latitude":result[i][7],
                "longitude":result[i][8],
                "images":result[i][9]
                }

                myseclist.append(want)

                # print("迴圈後印出來的",myseclist)
            
            return json.dumps({"nextpage":nextpage,"data":myseclist},sort_keys=False)
        else:
            return  jsonify({
                "error":"True",
                "message":"你可能頑皮搞錯指令或是伺服器異常"
            })
           
    #這裡是有page跟keyword的狀況          
    else:
        mycursor.execute(f"SELECT  * FROM power where name like '%{keyword}%' limit 12 offset {page}")
        results=mycursor.fetchall()
        print('type(results): ', type(results))
        print("兩個條件都有的結果",results)
        if results!=None:
            mytirlist=[]
            for i in range(0,12):
                want={
                "id":results[i][0],
                "name":results[i][1],
                "category":results[i][2],
                "description":results[i][3],
                "address":results[i][4],
                "transport":results[i][5],
                "mrt":results[i][6],
                "latitude":results[i][7],
                "longitude":results[i][8],
                "images":results[i][9]
                }

                mytirlist.append(want)

                # print("第二個迴圈後印出來的",mytirlist)
                
            return json.dumps({"nextpage":nextpage,"data":mytirlist},sort_keys=False)
        else:
            return  jsonify({
                "error":"True",
                "message":"你可能頑皮搞錯指令或是伺服器異常"
            })  
         


@app.route("/api/attraction/<attractionId>")
def api_attraction(attractionId):
    print(attractionId)
    mycursor.execute("SELECT  * FROM power WHERE id= '%s'"%(attractionId))
    user=mycursor.fetchone()
    print(user)
    if user!=None:
        mylsit={
            "id":user[0],
            "name":user[1],
            "category": user[2],
            "description": user[3],
            "address": user[4],
            "transport": user[5],
            "mrt": user[6],
            "latitude": user[7],
            "longitude": user[8],
            "images":user[9]
            }
        return json.dumps({"data":mylsit},sort_keys=False)
    else:
        return jsonify({
            "error":"True",
            "message":"你的景點編號輸入錯誤或是伺服器異常"
        })    


app.run(port=3000)
