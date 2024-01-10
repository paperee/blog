# main.py
# -*- coding: UTF-8 -*-

from flask import Flask,jsonify,request,render_template,send_file
from flask_limiter import Limiter
from json import dump,load
from codecs import open
from time import time
from os import path,listdir
from re import search

def test(path_):
    if not path.exists(path_):
        dump((),load_(path_,"w"))

    return path_

def load_(file,mode="r"):
    return open(file,mode,"UTF-8-sig")

def time_(path_):
    return round(path.getmtime(path_))

def getip():
    return request.headers.get("X-Forwarded-For",request.remote_addr)

def checkPath(text):
    return search(u'^[\u4e00-\u9fa5_a-zA-Z0-9]{1,24}$',text)

def limited():
    return "……"

app=Flask(str(round(time())),template_folder="client")
limiter=Limiter(app=app,key_func=getip)

method=("POST","GET")

@app.errorhandler(Exception)
@limiter.limit("2/minute")
def error(error):
    return render_template("404.html")

@app.route("/",methods=method)
@limiter.limit("2/minute")
def index():
    list_=((file.rsplit(".",1)[0],time_(f"notes/{file}")) for file in listdir("notes"))
    list__=[file.rsplit(".",1)[0] for file in listdir("pages")]
    data=sorted(list_,key=lambda essay:essay[1],reverse=True)
    bing="</a><a href='".join([f"/notes/{file_[0]}'>{file_[0]}" for file_ in data]+[f"/pages/{file_}'>{file_}" for file_ in list__])
    return render_template("index.html",data=(data,list__),bing="<a href='"+bing+"</a>")

@app.route("/<path:folder>/<path:file>",methods=method)
@limiter.limit("2/minute")
def essay(folder,file):
    if not checkPath(folder):
        return jsonify((0,"纸片","哼哼哼 啊啊啊啊"))
    
    path_=f"{folder}/{file}.md"
    text="#"+load_(path_).read().split("#",1)[-1]
    data=(folder,file,text,time_(path_),load(load_(test(f"client/_/{file}.json"))))
    return render_template("essay.html",folder=folder,title=file,data=data,bing=text[:min(50,len(text))].replace("\n","\\n")+"……")

@app.route("/files/<path:folder>/<path:file>",methods=method)
@limiter.limit("4/second")
def file(folder,file):
    return send_file(f"{folder}/{file}")

@app.route("/comment",methods=method)
@limiter.limit("2/minute")
def comment():
    form=request.form
    note=form.get("note","")
    list_=(form.get("nick",""),form.get("text",""),round(time()))

    if note+".md" not in listdir(form.get("folder","")):
        return jsonify((0,"评论","呃 找不到这篇笔记……"))

    if not all(list_):
        return jsonify((0,"评论","昵称/评论内容可能不完善？"))

    if not list_[0].isalnum() or len(list_[0])>=11:
        return jsonify((0,"评论","用数字/字母/汉字取个11字内的昵称吧！"))

    if len(list_[1])>=111:
        return jsonify((0,"评论","每条评论限制在111字内"))

    path_=f"client/_/{note}.json"
    data=load(load_(test(path_)))
    data.append(list_)
    dump(data,load_(path_,"w"))
    return jsonify((1,"评论","评论发送成功！",list_))

if __name__=="__main__":
    app.run(host="127.0.0.1",port=1234,debug=False)