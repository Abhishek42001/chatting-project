#new
import pickle,socket,ctypes
from collections import defaultdict
from datetime import datetime
from threading import Thread
import sys


s=socket.socket()
print("Socket Created successfully")
s.bind(('localhost',9997))

room=defaultdict(set)
s.listen(100)
print("Waiting for connections")

connections=set()
name_socket=dict()
t=None
def client_thread(conn,port,name,room_name):
    global connections,name_socket,room
    try:
        conn.send(bytes(f"\nWelcome to '{room_name.decode()}' Chat Room  {name.decode()}.\nNote:use \'command\' command to for special commands.\n\n    Start Chatting...\n",'utf-8'))
        now=datetime.now()
        t=now.strftime("%m/%d/%Y, %H:%M:%S")
        conn.send(t.encode())
    except:
        room[room_name.decode()].remove(name.decode())
        if len(room[room_name.decode()])==0:
            del room[room_name.decode()]
        print(f"<{name.decode()}> got disconnected without typing room name(accidently)...\n")
        return

    while True:
        try:
            temp=pickle.loads(conn.recv(2048))
            name=temp[0]
            msg=temp[1]
            whom=temp[2]
            if msg.decode()=="__send__list__":
                l=["True",list(room[room_name.decode()]),msg]
                conn.send(pickle.dumps(l))
            elif whom.decode()=="all":
                for person in room[room_name.decode()]:
                    if name_socket[person]!=conn:
                        l=["False",name,msg]
                        #print(msg.decode())
                        name_socket[person].send(pickle.dumps(l))
            else:
                #print(whom)
                name_socket[whom.decode()].send(pickle.dumps(["False",(name.decode()+"(Privately)").encode(),msg]))

        except:
            room[room_name.decode()].remove(name.decode())
            if len(room[room_name.decode()])==0:
                del room[room_name.decode()]
            print(f"<{name.decode()}> got disconnected...\n")
            break
            
            

def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)    
while True:
    c1,address1=s.accept()
    connections.add(c1)
    #have to handle the case if different persons with same name join
    c1.send(pickle.dumps(set(room.keys())))
    try:
        name=c1.recv(1024)
        room_name=c1.recv(1024)
        room[room_name.decode()].add(name.decode())
        print(f"<{name.decode()}>:Connected with ip address:{address1[0]}\n",end=" ")
        if room_name:
            print("With room name:",room_name.decode())
        #if client got disconnected anyhow like keyboard interruption
        elif not room_name or not name:
            room[room_name.decode()].remove(name.decode())
            if len(room[room_name.decode()])==0:
                del room[room_name.decode()]
            print(f"<{name.decode()}>: got disconnected... with ip address {address1[0]}\n")
            kill_thread(t)
            continue
        name_socket[name.decode()]=c1

        t=Thread(target=client_thread,args=(c1,address1[1],name,room_name))
        t.start()
    except:
        continue
# kill_thread(t)
# for c in connections:
#     c.close()

#s.close()    


















import pickle
import socket
import ctypes
from datetime import datetime
from threading import Thread
import sys


s=socket.socket()
print("Socket Created successfully")
s.bind(('localhost',9997))

s.listen(100)
print("Waiting for connections")

connections=set()
name_socket=dict()
names=dict()
def client_thread(conn,port,name):
    global connections,name_socket,names
    conn.send(bytes(f"\nWelcome to Chat Room  {names[port]}.\nNote:use \'command\' command to for special commands.\n\n    Start Chatting...\n",'utf-8'))
    now=datetime.now()
    t=now.strftime("%m/%d/%Y, %H:%M:%S")
    conn.send(t.encode())

    while True:
        try:
            temp=pickle.loads(conn.recv(2048))
            name=temp[0]
            msg=temp[1]
            whom=temp[2]
            if msg.decode()=="__send__list__":
                l=["True",names,msg]
                conn.send(pickle.dumps(l))
            elif whom.decode()=="all":
                for connection in connections:
                    if connection!=conn:
                        l=["False",name,msg]
                        connection.send(pickle.dumps(l))
            else:
                #print(whom)
                name_socket[whom.decode()].send(pickle.dumps(["False",(name.decode()+"(Privately)").encode(),msg]))

        except:
            if conn in connections:
                del names[port]
                connections.remove(conn)
            print(f"<{name.decode()}> got disconnected...\n")
            break
            
            

def kill_thread(thread):
    """
    thread: a threading.Thread object
    """
    thread_id = thread.ident
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
    if res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)    
while True:
    c1,address1=s.accept()
    connections.add(c1)
    name=c1.recv(1024)
    print(f"<{name.decode()}>:Connected with ip address:{address1[0]}\n")
    names[address1[1]]=name.decode()
    name_socket[name.decode()]=c1

    t=Thread(target=client_thread,args=(c1,address1[1],name))
    t.start()
# kill_thread(t)
# for c in connections:
#     c.close()

#s.close()    


