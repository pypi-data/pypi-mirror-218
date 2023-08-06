from wsgiref.simple_server import make_server
import os
import re
import json
import datetime
import threading
import random

html3=''
tmp=[]
def cookie():
    while True:
        with open(".\\cookies.txt","r",encoding="UTF-8") as f2:
            newlist2=[]
            for i in f2.readlines():
                nowtime=datetime.datetime.now()
                every_cookie=eval(i.split("\n")[0])
                if str(every_cookie["time_to_live"]-nowtime)[0]=="-":
                    pass
                else:
                    newlist2.append(i)
            try:
                check2=tuple(newlist2[-1].split("\n"))
                if "\n" in check2:
                    newlist2[-1]=check2[0]
            except:
                pass
        with open(".\\cookies.txt","w", encoding="UTF8") as f2:
            f2.writelines(newlist2)
def makedict(env,re=None):
    HTTPdict={}
    HTTPdict["URLmatch"]=re
    HTTPdict["method"]=env['REQUEST_METHOD']
    HTTPdict["req_ip"]=env['REMOTE_ADDR']
    req_json=None
    try:
        req_body = env['wsgi.input'].read(int(env['CONTENT_LENGTH']))
        req_json = json.loads(req_body)
    except:
        pass
    HTTPdict["req_json"]=req_json
    HTTPdict["QUERY_STRING"]=env["QUERY_STRING"]
    return HTTPdict
def load_staic(link="."):
    link+="\\staic"        
    list1=[]
    for staicname in os.listdir(link):
        global staic_header
        staic_header="text/plain"
        with open(link+"\\"+staicname, "r", encoding="UTF8") as f:
            houzhui=staicname.split(".")[-1]
            if houzhui=="js":
                staic_header="application/x-javascript;charset=utf-8"
            elif houzhui=="css":
                staic_header="text/css;charset=utf-8"
            elif houzhui=="html":
                staic_header="text/html;charset=utf-8"
            try:
                list1.append(("/"+staicname,f.read(),staic_header,"text"))
            except UnicodeDecodeError:
                f.close()
                with open(link+"\\"+staicname,"rb") as f:
                    staic_header="application/octet-stream"
                    houzhui=staicname.split(".")[-1]
                    if houzhui=="ico":
                        staic_header="application/x-ico"
                    elif houzhui=="icon":
                        staic_header="application/x-icon"
                    list1.append(("/"+staicname,f.read(),staic_header,"byte"))          
    return list1
def errorhandle(status,status2,start_response,env):
    global err
    global url
    try:
        start_response(status2, [('Content-Type', 'text/html;charset=utf-8')])
    except:
        pass
    if err==0:
        return "<h1>"+status2+"</h1>"
    HTTP_req_dict=makedict(env)
    return str(err(status))
def app(environ,start_response):
    global html3
    global url
    global staic
    try:
        global tmp
        global staic  #???
        for url1 in url:
            if url1[0]==environ['PATH_INFO'] or (url1[4]=="RE" and not re.match(url1[0],environ['PATH_INFO'])==None):
                if environ['REQUEST_METHOD'] in url1[2]:
                    start_response('200 OK', url1[3])
                    match=None
                    if url1[0]==environ['PATH_INFO']:
                        pass
                    else:
                        match=re.findall(url1[0],environ['PATH_INFO'])
                    HTTP_req_dict= makedict(environ,match)
                    if not url1[5]=="websocket":
                        return [str(url1[1](HTTP_req_dict)).encode()]
                    else:
                        global Htmlcode
                        name=random.randint(1,999999)
                        global tmp
                        newtmp=[eve for eve in tmp if not eve[0]=="/"+str(name)]
                        tmp=list(newtmp)
                        tname="/"+str(name)
                        tmp.append(tname)
                        print("==========================")
                        print("Websocket is running at:%s"%(tname))
                        print("==========================")
                        code="""<script>var recv=0;function send(msg,fuc){var xmlhttp;if (window.XMLHttpRequest){xmlhttp=new XMLHttpRequest();}else{xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");}xmlhttp.onreadystatechange=function(){fuc(xmlhttp.status,JSON.parse(xmlhttp.responseText).msg)};xmlhttp.open("POST","%s",true);xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");xmlhttp.send(JSON.stringify({"msg":msg}));}</script>"""%(tname)+str(url1[1](HTTP_req_dict))
                        return [code.encode()]
                else:
                    return [str(errorhandle("405","405 Method Not Allowed",start_response,environ)).encode()]
        for staicdata in staic:
            if staicdata[0]==environ['PATH_INFO']:
                start_response('200 OK', [("Content-Type",staicdata[2])])
                if staicdata[3]=="byte":
                    return [staicdata[1]]
                return [staicdata[1].encode()]
        for tmphtml in tmp:
            if tmphtml==environ['PATH_INFO']:
                start_response('200 OK', [("Content-Type","application/json;chatset=utf-8")])
                try:
                    msg=makedict(environ,None)["req_json"]["msg"]
                    ret=str(json.dumps({"msg":webs(msg)}))
                except Exception as e:
                    ret=str(json.dumps({"msg":{"err":str(e)}}))
                return [ret.encode()]
        return [errorhandle("404","404 Not Found",start_response,environ).encode()]
    except Exception as e:
        print("==========================")
        print("Found a bug!")
        with open(".\\debug.txt", "a", encoding="UTF8") as f:
            if os.path.getsize(".\\debug.txt"):
                f.write("\n")
            f.write("==========================")
            f.write("\n")
            f.write(str(e))
            f.write("\n")
            f.write("==========================")
        print("see .\\debug.txt for more information")
        print("==========================")
        return [errorhandle("500","500 Internal Server Error",start_response,environ).encode()]
   

class _Dakada:
    def __init__(self,link=".",host='',port=8000):
        self.link=link
        self.host=host
        self.port=port
        self.url1=[]
        self.err1=0
        self.websocket=0
        return 
    def addpath(self,path,URL_type="URL",method=['GET'],req_header=[('Content-Type', 'text/html;charset=utf-8')],mode="staic"):
        def returnfuc(fuc):
            self.url1.append((path,fuc,method,req_header,URL_type,mode))
        return returnfuc
    def run(self):
        try:
            global url
            global err
            global p_link
            global staic
            global webs
            err=self.err1
            url=self.url1
            p_link=self.link
            webs=self.websocket
            print("making server...")
            staic=load_staic(p_link)
            http=make_server(str(self.host),self.port,app)
            print("OK")
            print("starting cookiehandler...")
            t=threading.Thread(target=cookie)
            t.setDaemon(True)
            t.start()
            print("OK")
            print("Dakada(ver 2.1) is running!")
            if self.host=='':
                print("View at:http://localhost:"+str(self.port))
            else:
                print("View at:http://"+self.host+":"+str(self.port))
            http.serve_forever()
        except KeyboardInterrupt:
            print("server exit")
    def seterr(self,fuc):
        self.err1=fuc
    def register_blueprint(self,blueprint):
        self.url1+=blueprint.url1
    class db:
        def __init__(self,link=".",cookie=False):
            self.link=link
            self.dangerstr=["\n"]
            if not cookie:
                self.link+="\\db"
        def adddangerstr(self,dangerlist):
            self.dangerstr+=dangerlist
        def add(self,dblink,jsonordict_list):
            with open(self.link+"\\"+dblink, "a", encoding="UTF8") as f:
                i=1
                if os.path.getsize(self.link+"\\"+dblink):
                    f.write("\n")
                for every_json in jsonordict_list:
                    newlist=[danger for danger in dangerstr if danger in str(every_json)]
                    if not newlist==[]:
                        return "Bad data!"
                    f.write(str(every_json))
                    if not i==len(jsonordict_list):
                        f.write("\n")
                    i+=1
        def load(self,dblink,key):
            returnlist=[]
            with open(self.link+"\\"+dblink,"r", encoding="UTF8") as f:
                list1=f.readlines()
                for every_json in list(list1):
                    every_json2=eval(every_json.split("\n")[0])
                    dictkey=list(every_json2.keys())[0]
                    dictvalue=list(every_json2.values())[0]
                    if key==dictkey:
                        returnlist.append(every_json2)
            return returnlist
        def save(self,dblink,key,value):
            with open(self.link+"\\"+dblink,"r", encoding="UTF8") as f:
                list1=f.readlines()
                i=0
                for every_json in list(list1):
                    every_json2=eval(every_json.split("\n")[0])
                    dictkey=list(every_json2.keys())[0]
                    if dictkey==key:
                        list1[i]=str({dictkey:value})+"\n"
                    i+=1
            with open(self.link+"\\"+dblink,"w", encoding="UTF8") as f:
                f.writelines(list1)
        def delete(self,dblink,key):
            with open(self.link+"\\"+dblink,"r", encoding="UTF8") as f:
                list1=f.readlines()
                i=0
                newlist=[]
                length=len(list1)
                for every_json in range(length):
                    every_json2=eval(list1[every_json].split("\n")[0])
                    dictkey=list(every_json2.keys())[0]
                    if dictkey==key:
                        pass
                    else:
                        newlist.append(list1[i])
                    i+=1
                try:
                    check=tuple(newlist[-1].split("\n"))
                    if "\n" in check:
                        newlist[-1]=check[0]
                except:
                    pass
            with open(self.link+"\\"+dblink,"w", encoding="UTF8") as f:
                f.writelines(newlist)
        def clear(self,dblink):
            with open(self.link+"\\"+dblink,"w", encoding="UTF8") as f:
                f.writelines([])
    def newwebsocket(self,fuc):
        self.websocket=fuc
import sys
sys.modules[__name__]=_Dakada