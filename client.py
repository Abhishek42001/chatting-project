#new
import socket,pickle,ctypes,sys
from colorama import Fore,Style,Back
from threading import Thread
from datetime import date, datetime
import mysql.connector

#keep all data on server,timestamp
chatdb=mysql.connector.connect(
    host="localhost",
    user="abhishek",
    password="abhipc",
    database="abhishek"
)

mycursor=chatdb.cursor()

whom="all"
flag=False
diff_names=set()
c1=socket.socket()
print("Connecting to server...\n")
c1.connect(('localhost',9997))
print("Connected.\n")

#Taking Name

room_list=pickle.loads(c1.recv(2048))
if len(room_list)==0:
    print("\n\t"+"\033[91m {}\033[00m".format("No room available,  create new one.")+"\n")
    room_name=input("\033[94m{}\033[00m".format("Enter Room name:"))
else:
    print("\nRoom list:",*list(room_list))
    room_name=input("\n"+"\033[92m{}\033[00m" .format("Select Room Name{case sensitive}(Or Create New One):"))

c1.send(room_name.encode())
names_in_room=pickle.loads(c1.recv(2048))
name=input("Enter Your Name:")
while name in names_in_room:
    print("User already exists.")
    name=input("Enter Name:")
mycursor.execute("show tables like "+"'"+name+"'")
 
#https://stackoverflow.com/questions/1650946/mysql-create-table-if-not-exists-error-1050/53582934
if not mycursor.fetchall():
    mycursor.execute("CREATE TABLE "+name+" (Who VARCHAR(255),Message VARCHAR(255)) PARTITION BY KEY(Who) (PARTITION p1 , PARTITION p2 ,PARTITION p3 , PARTITION p4 );")
#to listen_msg

c1.send(name.encode())
def listen_msg():
    global diff_names,name
    while True:
        #it contains flag,name_list or name,msg
        l=pickle.loads(c1.recv(1024))
        #if client wants List of connected people
        if l[0]=="True":
            name_list=l[1]
            print("\nConnected people list:\n")
            print(*[name for name in l[1]])
            diff_names.__init__()
            for i in l[1]:
                diff_names.add(i)
        else:
            recv_name=l[1].decode()
            msg=l[2].decode()
            t=datetime.now()
            time=t.strftime("%H:%M")
            #printing the recived message with time

            #inserting to database
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = (recv_name, msg+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()

            print("\n"+"<"+"\033[95m{}\033[00m".format(recv_name)+">: "+msg+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
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
        #if same person is choosed e.g  aman<-->aman
        if whom==name:
            whom="all"
            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("You can't chat with yourself...\n"))
        elif whom not in diff_names:
            whom="all"
            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("Wrong Selection(try again by using command command)\n"))
        else:
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        #set flag to False so that next time it won't ask for selecting name until...
        flag=False
    
    to_send=input()
    now=datetime.now()
    time=now.strftime("%H:%M")
    if to_send=="command":
        n=int(input("\033[92m {}\033[00m" .format("1.Quit\t2.Chat Privately 3.Chat with all  4.Show history:")))
        if n==1:
            break
        elif n==2:
            c1.send(pickle.dumps([name.encode(),"__send__list__".encode(),"all".encode()]))
            flag=True
        elif n==3:
            whom="all"
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        elif n==4:
            mycursor.execute("SELECT * FROM "+name)
            myresult = mycursor.fetchall()
            print()
            for x in myresult:
                for y in x:
                    print(y,end=": ")
                print()
              
            print("\n\t"+"\033[93m {}\033[00m" .format("\nThe End of history...\n\n"))
        
        else:
            print("\033[91m {}\033[00m" .format("Invalid Choice..."))
            
    else:
        if whom!="all":
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = ("You ("+whom+")", to_send+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()
            print("\033[95m{}\033[00m" .format("<You"+"("+whom+")"+">: ")+to_send+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
        else:
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = ("You", to_send+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()
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






import socket,pickle,ctypes,sys
from colorama import Fore,Style,Back
from threading import Thread
from datetime import date, datetime
import mysql.connector

chatdb=mysql.connector.connect(
    host="localhost",
    user="abhishek",
    password="abhipc",
    database="abhishek"
)

mycursor=chatdb.cursor()

whom="all"
flag=False
diff_names=set()
c1=socket.socket()
print("Connecting to server...\n")
c1.connect(('localhost',9997))
print("Connected.\n")

#Taking Name
name=input("Enter Your Name:")
#sending the name to the server


mycursor.execute("show tables like "+"'"+name+"'")

#https://stackoverflow.com/questions/1650946/mysql-create-table-if-not-exists-error-1050/53582934
if not mycursor.fetchall():
    mycursor.execute("CREATE TABLE "+name+" (Who VARCHAR(255),Message VARCHAR(255))")
c1.send(name.encode())

#to listen_msg
def listen_msg():
    global diff_names,name
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
            recv_name=l[1].decode()
            msg=l[2].decode()
            t=datetime.now()
            time=t.strftime("%H:%M")
            #printing the recived message with time

            #inserting to database
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = (recv_name, msg+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()

            print("\n"+"<"+"\033[95m{}\033[00m".format(recv_name)+">: "+msg+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
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
        #if same person is choosed e.g  aman<-->aman
        if whom==name:
            whom="all"
            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("You can't chat with yourself...\n"))
        elif whom not in diff_names:
            whom="all"
            print("\n"+Fore.RED+"\033[91m {}\033[00m" .format("Wrong Selection(try again by using command command)\n"))
        else:
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        #set flag to False so that next time it won't ask for selecting name until...
        flag=False
    
    to_send=input()
    now=datetime.now()
    time=now.strftime("%H:%M")
    if to_send=="command":
        n=int(input("\033[92m {}\033[00m" .format("1.Quit\t2.Chat Privately 3.Chat with all  4.Show history:")))
        if n==1:
            break
        elif n==2:
            c1.send(pickle.dumps([name.encode(),"__send__list__".encode(),"all".encode()]))
            flag=True
        elif n==3:
            whom="all"
            print("\n\t"+"\033[93m {}\033[00m" .format("Go for it...")+"\n\n")
        elif n==4:
            mycursor.execute("SELECT * FROM "+name)
            myresult = mycursor.fetchall()
            print()
            for x in myresult:
                for y in x:
                    print(y,end=": ")
                print()
              
            print("\n\t"+"\033[93m {}\033[00m" .format("\nThe End of history...\n\n"))
        
        else:
            print("\033[91m {}\033[00m" .format("Invalid Choice..."))
            
    else:
        if whom!="all":
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = ("You ("+whom+")", to_send+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()
            print("\033[95m{}\033[00m" .format("<You"+"("+whom+")"+">: ")+to_send+"\t"+"\033[96m {}\033[00m".format(time)+"\n")
        else:
            sql = "INSERT INTO "+name+" (Who,Message) VALUES (%s, %s)"
            val = ("You", to_send+"    "+time)
            mycursor.execute(sql, val)
            chatdb.commit()
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
