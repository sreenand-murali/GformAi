from openai import OpenAI
client = OpenAI(api_key="")
from urllib.request import urlopen
from bs4 import BeautifulSoup

import js2py
import openai 
  
openai.api_key = ''

url = input("enter link : ")


html = urlopen(url)
soup = BeautifulSoup(html, "html.parser")
script = soup.body.find_all("script",{'type':'text/javascript'})[0].string

questions = []
answers=[]
res1 = js2py.eval_js(script)
for i in range(0,20):
    if(type(res1)!=js2py.base.JsObjectWrapper):
        continue
    elif(type(res1[1])!=js2py.base.JsObjectWrapper):
        continue
    elif(type(res1[1][1])!=js2py.base.JsObjectWrapper):
        continue
    elif(type(res1[1][1][i])!=js2py.base.JsObjectWrapper):
        continue
    elif(type(res1[1][1][i][4])!=js2py.base.JsObjectWrapper):
        continue
    else:
        answerList = res1[1][1][i][4][0][1]
        if(answerList == None):
            continue
        else:
            question = res1[1][1][i][1]
            questions.append(question)
            answers.append(answerList)
qStr=""
for i in range(0, len(questions)):
    qStr+=str(i+1)+". "
    qStr+=questions[i]+"\noptions:\n"
    for j in range(0,len(answers[i])):
        qStr+=str(j+1)+"."
        qStr+=answers[i][j][0]+"\n"
    qStr+="\n"


print(qStr)


print("/////////////////////Chat-GPT-Answers////////////////////")
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": qStr+"give answers for these questions in short text along with level of confidence in answer in percentage from this given paragraph" },
    
  ]
)

print(completion.choices[0].message.content)
