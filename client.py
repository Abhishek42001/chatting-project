import socket,pickle,ctypes,sys
from colorama import Fore,Style,Back
from threading import Thread
from datetime import date, datetime

Back.BLACK
whom="all"
flag=False

diff_names=set()
c1=socket.socket()
print("Connecting to server...\n")
print("Connected.\n")
c1.connect(('localhost',9997))

#Taking Name
name=input("Enter Your Name:")
#sending the name to the server
c1.send(name.encode())

#to listen_msg
def listen_msg():
    global diff_names
    while True:
        #it contains flag,name_list or name,msg
        l=pickle.loads(c1.recv(1024))
        #if client wants List of connected people
        if l[0]=="True":
            name_list=l[1]
            print("\nConnected people list:\n")
            print(*[name for name in l[1].values()])
            diff_names.__init__()
            for i in l[1].values():
                diff_names.add(i)
        else:
            name=l[1].decode()
            msg=l[2].decode()
            t=datetime.now()
            time=t.strftime("%H:%M")
            #printing the recived message with time
            print("\n"+"<"+"\033[95m{}\033[00m".format(name)+">: "+msg+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
#Receiving message from server
print(c1.recv(1024).decode())
print("\t",end="")
print(c1.recv(1024).decode())
print("\n")

#making a thread of this client
t=Thread(target=listen_msg)

t.start()

#to send message
while True:
    #if we have to choose a name
    if flag:
        whom=input("Select name:")
        #if same person is choosen e.g  aman<-->aman
        if whom==name:
            whom="all"

            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("You can't chat with yourself...\n"))
        elif whom not in diff_names:
            whom="all"
            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("Wrong Selection\n"))
        else:
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        #set flag to False so that next time it won't ask for selecting name until...
        flag=False
    
    to_send=input()
    now=datetime.now()
    time=now.strftime("%H:%M")
    if to_send=="command":
        n=int(input("\033[92m {}\033[00m" .format("1.Quit\t2.Chat Privately 3.Chat with all:")))
        if n==1:
            break
        elif n==2:
            c1.send(pickle.dumps([name.encode(),"__send__list__".encode(),"all".encode()]))
            flag=True
        elif n==3:
            whom="all"
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        else:
            print("\033[91m {}\033[00m" .format("Invalid Choice..."))
            
    else:
        if whom!="all":
            print("\033[95m{}\033[00m" .format("<You"+"("+whom+")"+">: ")+to_send+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
        else:
            print("\033[95m{}\033[00m" .format("<You>: ")+to_send+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
        c1.send(pickle.dumps([name.encode(),to_send.encode(),whom.encode()]))


#from stackoverflow 
#geeksforgeeks (different way to kill a thread)
def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
kill_thread(t)
c1.close()
