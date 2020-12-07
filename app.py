from flask import Flask,render_template,redirect,request,send_file
import json
import ssl
from urllib.request import Request,urlopen
import requests

from bs4 import BeautifulSoup

ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE
def fin_title(url):
    #print(url)
    req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
    webpage=urlopen(req).read()

    soup=BeautifulSoup(webpage,'html.parser')

    #print(soup)

    question=soup.find("title")
    return question.text.replace(" - Quora","")


def func(url):

    req=Request(url,headers={'User-Agent':'Mozilla/5.0'})
    webpage=urlopen(req).read()

    soup=BeautifulSoup(webpage,'html.parser')

    quora_json=dict()

    question=soup.find("title")
    quora_json["question"]=question.text.replace(" - Quora","")


    quora_json["answers"]=[]
    answer=soup.find("script",{"type":"application/ld+json"})
    #print(json.loads(answer.string)["mainEntity"])
    ans_list=json.loads(answer.string)["mainEntity"]["suggestedAnswer"]

    for answer in ans_list:
    
        try:
            author=answer["author"]["name"]
        except KeyError as e:
            author="Not available"
        try:
            text=answer["text"]
        except KeyError as e:
            text="Not available"
        try:
            dateCreated=answer["dateCreated"]
        except KeyError as e:
            dateCreated="Not available"
     

    
        
        
        answer_val={
            "author":author,
            "dateCreated" : dateCreated,
                    "text":text,
                    
                    
        
        
        }
        

        quora_json["answers"].append(answer_val)

    json_obj=json.dumps(quora_json,indent=4)
    with open("data.txt",'w') as outfile:
        outfile.write(json_obj)

    # name="fgf"
    # filename="%s.txt"%name
    # os.rename("data.txt",filename)



app = Flask(__name__)







@app.route('/')
def hello():
    return render_template('home.html')
@app.route('/link')
def link_op():
    return render_template('index.html')
@app.route('/handle_data/<path:title>')
def fin(title):
    func(title)
    
    pa="data.txt"

    return send_file(pa, as_attachment=True)
  
@app.route('/preloaded')
def fun():
    l=['https://www.quora.com/What-is-your-salary-Are-you-happy-with-it',
    'https://www.quora.com/Whats-wrong-with-capitalism-What-system-should-replace-it-Is-it-really-communism',
    'https://www.quora.com/Who-is-really-the-richest-person-in-the-world-Putin-A-Rothschild']

    um=dict()
     
    for u in l:
        um[u]=fin_title(u)
        #print(5)
    return render_template('preloaded.html', results = um)


@app.route('/handle_data', methods=['POST'])
def handle_data():
    um=dict()
    urls=request.form['url']
    #print("*")
    url=urls.split(",")
    #print("1")
    #print("2")

    for u in url:
        um[u]=fin_title(u)
        #print(5)
        
    return render_template('res.html', results = um)

if __name__=='__main__':
    app.run(threaded=False)