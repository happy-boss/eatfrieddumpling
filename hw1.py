from flask import Flask, request, render_template, redirect, session, url_for, jsonify
import mysql.connector
# 第一步先將景點的檔案開啟，這個檔案是json，做資料上的處理
import json
with open("data\\taipei-attractions.json", mode="r", encoding='utf-8') as file:
    data = json.load(file)
# 確定抓到資料了
# print(data)
# 把資料處理
app = Flask(
    __name__, static_folder="public", static_url_path="/")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="2021",
    database="mydatabase",
    buffered=True
)

mycursor = mydb.cursor()


clist = data["result"]["results"]
print(len(clist))
# print(clist)
# with open("data.txt","w",encoding='utf-8') as file:
#     for place in clist:
#         url="http://"+place["file"].split("http://")[1]
#         print(url)
#         file.write(place["info"]+","+place["stitle"]+","+place["longitude"]+","+place["latitude"]+","+url+"\n")


for i in range(0,len(clist)):
    index=clist[i]["_id"]
    print(i)
    name =clist[i]["stitle"]
    category = clist[i]["CAT2"]
    description = clist[i]["xbody"]
    address = clist[i]["address"]
    transport = clist[i]["info"]
    mrt = clist[i]["MRT"]
    latitude = clist[i]["latitude"]
    longitude = clist[i]["longitude"]
    mylist=clist[i]["file"].split("http://")
    for j in range(0,len(mylist)):
        want=mylist[j]
        if ".jpg" in mylist[j]or ".JPG" in mylist[j]or ".png" in mylist[j]or ".PNG" in mylist[j]:
             mylist.append(want)
             #這步到拿出我要的網址
             # print(mylist)
             images=str(mylist)
             #print(type(images))

            #寫入sql
    sql = "INSERT INTO power (id,name,category,description,address,transport,mrt,latitude,longitude,images) VALUES (%s,%s, %s,%s,%s, %s,%s,%s, %s,%s)"
    val = (index,name,category,description,address,transport,mrt,latitude,longitude,images)
    mycursor.execute(sql, val)
    mydb.commit()

