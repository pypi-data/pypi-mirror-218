"""
    Semp Python Tool by Win12Home
    Version:0.5.0.3 Beta
    
"""
from PIL import Image,ImageTk
from requests import *
from sys import set_int_max_str_digits as max
from subprocess import Popen


max(0)
BINARY_TRUE="BTRUE"
BINARY_FALSE="BFALSE"

class NumberError(Exception):
    def __init__(self, *args, **kwargs):
        pass

class BoolError(Exception):
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
"""