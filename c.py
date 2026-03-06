import socket,threading

port=int(input("Port: "))
name=input("Name: ")

s=socket.socket()
try:
    s.bind(("127.0.0.1",port))
    s.listen()
    clients=[]
    print("Room created")

    def handle(c):
        while True:
            msg=c.recv(1024)
            for cl in clients:
                cl.send(msg)

    while True:
        c,_=s.accept()
        clients.append(c)
        threading.Thread(target=handle,args=(c,),daemon=True).start()

except:
    s.connect(("127.0.0.1",port))

    def recv():
        while True:
            print(s.recv(1024).decode())

    threading.Thread(target=recv,daemon=True).start()

    while True:
        msg=input()
        s.send(f"{name}: {msg}".encode())