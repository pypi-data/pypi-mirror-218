"""
    Semp Python Tool by Win12Home
    Version:0.5.2.13 Beta
    
"""
from PIL import Image,ImageTk
from requests import *
from sys import set_int_max_str_digits as max
from subprocess import Popen
from random import randint
from datetime import datetime


max(0)
BINARY_TRUE="BTRUE"
BINARY_FALSE="BFALSE"

AUTO="AutoEnter"
NONE="NoEnter"

class NumberError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class BoolError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class ArgumentError(Exception):
    def __init__(self, *args, **kwargs):
        pass

def PhotoTk(file: str = ...):
    photo=Image.open(file)
    #Open Photo
    tkphoto=ImageTk.PhotoImage(image=photo)
    #Save Photo
    return tkphoto

def fromsnumber(b_from: int = 0,to: int = ...,passnum: int = 0):
    a=[]
    if passnum == None or passnum == 0:
        for x in range(b_from,to+1):
            a.append(x)
        return a
    else:
        try:
            for x in range(b_from, to + 1,passnum):
                a.append(x)
            return a
        except:
            raise NumberError("Name error.")

def CreatePassword(length: int = ...):
    sslist=["0","1","2","3","4","5","6","7","8","9","^","%","a","A","B","c","C","d","E","f","D","F","g","H","i","j","K","l","M","N","o","P","q","Q","r","s"
          ,"t","U","V","v","T","w","W","x","Y","z","!"]
    password=""
    temps=""
    for __count in range(length):
        for __count in range(5):
            temps=sslist[randint(0,len(sslist)-1)]
        password+=temps
    return password


class request_simplifies:
    def Download(website: str = ...,name: str = ...,binary: bool = ...):
        r = get(website)
        if binary == True or binary == BINARY_TRUE:
            with open(name, "wb") as f:
                for chunk in r.iter_content(chunk_size=512):
                    f.write(chunk)
        #This method can download JPG file, EXE file, PNG file, etc
        elif binary == False or binary == BINARY_FALSE:
            with open(name, "wb") as f:
                for chunk in r.iter_content(chunk_size=512):
                    f.write(chunk)
        #This method can download TXT file, JSON file, JS file, etc
        else:
            raise BoolError("Not be "+str(name)+".Expected BINARY_TRUE or BINARY_FALSE")
    def ResponseGet(website: str = ...):
        r=get(website)
        return {"Status_Code":r.status_code,"URL":r.url,"Text":r.text}

def power_operation(num1: int = ...,num2: int = ...):
    num=num1
    for __count in range(num2-1):
        num*=num1
    return num

 
def fibonacci_sequence(to: int = ...):
    numlist=[1,1,1]
    num=1
    for __count in range(to-3):
        num+=numlist[len(numlist)-2]
        numlist.append(num)
    return numlist

 
class Requester:
    def __init__(self,website: str = ...):
        super().__init__()
        self.websitelink=website
    def Download(self,name: str = ...,binary=False):
        self.r = get(self.websitelink)
        if binary == True or binary == BINARY_TRUE:
            with open(name, "wb") as f:
                for chunk in self.r.iter_content(chunk_size=512):
                    f.write(chunk)
        #This method can download JPG file, EXE file, PNG file, etc
        elif binary == False or binary == BINARY_FALSE:
            with open(name, "wb") as f:
                for chunk in self.r.iter_content(chunk_size=512):
                    f.write(chunk)
        #This method can download TXT file, JSON file, JS file, etc
        else:
            raise BoolError("Not "+str(name)+".Expected BINARY_TRUE or BINARY_FALSE")
    def ResponseGet(self):
        self.r=get(self.websitelink)
        return {"status_code":self.r.status_code,"url":self.r.url,"text":self.r.text}

 
def PyPrompt():
    Popen(
        "python.exe",
        shell=True,
        encoding="utf-8"
    )

 
def CmdPrompt():
    Popen(
        "cmd.exe",
        shell=True
    )

def CreateMarkdown(title: str = ...,text: list[str] = ...,name: str = ...,auto: str = AUTO):
    markdown=""
    markdown+=f"---\n{title}\n---\n"
    if auto == AUTO:
        for word in text:
            markdown+=f"{word}<br/>"
            with open(name, "w") as f:
                f.write(markdown)
    elif auto == NONE:
        for word in text:
            markdown+=word
        with open(name,"w") as f:
            f.write(markdown)
    else:
        raise ArgumentError("Not in AUTO or NONE")

def GetTime(format:str = "%Y.%m.%d %H:%M:%S"):
    return datetime.now().strftime(format)

def NowDate():
    return datetime.now()

def Date(year:int = ...,month:int = ...,day: int = ...):
    return datetime(year,month,day)

def DateWeekday(datevar):
    weekday={1:"Monday",2:"Tuesday",3:"Wednesday",4:"Thursday",5:"Friday",6:"Saturday",7:"Sunday"}
    return weekday[int(datevar.isoweekday())]
"""
Here are some examples.
Response(variable):
    response=Requester("https://1.1.1.1/")
    response.ResponseGet()
Response(code):
    request_simplifies.ResponseGet("https://1.1.1.1/")
Fibonacci Sequence:
    fibonacci_sequence(10)
Power:
    power_operation(10,5)
All Numbers:
    fromsnumber(5,135)
Photo TK:
    from tkinter import *
    root=Tk()
    root.title("Test")
    img=PhotoTk("C:/test.jpg")
    a=Label(self,image=img)
    a.pack()
    root.mainloop()
Markdown Creator:
    CreateMarkdown("Hello World!",["They are some example","They are some example"],"README.md")
"""