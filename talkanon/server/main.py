# Imports.
from src.imports import *

def writeLogs(text):
    with open('errorLogs', 'w') as logFile:
        try:
            logFile.write(str(text))
        except:
            print("[!] - Failed to write logs.")

# Setup server vars
chans      = ["general", "info", "negres", "gangster"] # Channels names.
password   = "1234"                                    # Password of the server.
port       = 667                                       # Port of the server.
host       = ""                                        # Ip of the server (let it blank).
clientList = []                                        # List of the clients (dict).

# Message form
messageTemplate = "{user} said - {message}"

# Init the server.
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create the socket.
    server.bind((host, port))                                  # Bind the socket to the host and port var.
    server.listen()                                            # Listen to the socket.

    # Setup ssl certs / heys.
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain("../ssl/CERT/cert-server.pem","../ssl/CERT/cert-key.pem")

    # Setup ssl server.
    server_ssl = context.wrap_socket(server, server_side=True)
except Exception as exc:
    print('\n[+] An Error occured, check "errorLogs" file')
    writeLogs(text=exc)

def returnTime():
    # Anyways, useless, make it yourself not that difficult
    pass

def getChanHistoric(chan: str):
    # Return the historic of a chan (the file get the name of the chan)
    with open(f"chans/{chan}", "r") as chanFile:
        return chanFile.read()

def updateChanHistoric(chan: str, msg: str):
    historic = open(f"chans/{chan}", "r").read()
    if historic.splitlines().len() == 20:
        with open(f"chans/{chan}", "w") as chanFile:
            historic.pop(0)
            chanFile.write(historic + f"\n{msg}")
    else:
        if historic.len() == 0:
            with open(f"chans/{chan}", "w") as chanFile:
                chanFile.write(msg)
        else:
            with open(f"chans/{chan}", "w") as chanFile:
                chanFile.write(historic + f"\n{msg}")

def searchClientInList(clientSocket):
    # Return the clientDict by using the clientSocket as "keyword".
    for client in clientList:
        if client["socket"] == clientSocket:
            return client

def fetchAllSocketInClientList():
    # Fetch all clients sockets in the clientList (return the socket in the client dict).
    socketList = []
    for client in clientList:
        socketList.append(client["socket"])

def searchForClientsInChan(chan: str):
    clientInChan = []
    for client in clientList:
        if client["chan"] == chan:
            clientInChan.append(client)
            return clientInChan

def addClientsInList(clientSocket, nickname):
    # Add a client (dict) in the clientList, used when just connected.
    clientDict = {
        "nickname": nickname,
        "socket": clientSocket,
        "chan": ""
    }
    clientList.append(clientDict)

def editChan(client, chan: str):
    client["chan"] = chan
    return client

def clientThread(clientSocket):
    while True:
        try:
            # Client message (can be a normal message as a command or a chan modification).
            clientMsg = clientSocket.recv(1024)
            try:
                clientMsg = clientMsg.decode('utf-8')
            except Exception as exc:
                print('\n[+] An Error occured, check "errorLogs" file')
                writeLogs(str(exc) + " | Failed to decode the message from client in clientThread")
            client    = searchClientInList(clientSocket)
            nickname  = client["nickname"]

            # Edit chan command.
            if clientMsg.startswith("CHAN"):
                clientMsgChan = clientMsg[5:len(clientMsg)] # 5 chars cause CHAN and a space with then the channel name.
                if clientMsgChan in chans:
                    editedClient = editChan(client, clientMsgChan)
                    clientList.remove(client)
                    clientList.append(editedClient)

                    client.send(getChanHistoric())
                else:
                    clientSocket.send(BADCHAN)

            else:
                clients = searchForClientsInChan(client["chan"])
                for chanClient in clients:
                    chanClient.send(messageTemplate.format(nickname, clientMsg))

        except:
            client = searchClientInList(clientSocket)
            clientList.remove(client)
            clientSocket.close()
            break

def serverHandle():
    while True:
        # Accept connexion.
        client, address = server_ssl.accept()

        # Verifying client.
        verifyMsg = client.recv(1024).decode('utf-8')
        if verifymsg == CLIENT_HI:
            pass
        else:
            client.close()

        # Asking for nickname.
        client.send(NICKNAME)
        nickname = client.recv(1024).decode('utf-8')
        if nickname in users:
            pass
        else:
            client.send(NONUSER)
            client.close()

        # Asking for password.
        client.send(PASSWORD)
        clientPasswd = client.recv(1024).decode('utf-8')
        if clientPasswd == password:
            client.send(OKCODE)
        else:
            client.send(BADPASS)
            client.close()

        addClientsInList(client, nickname)

print("Server online!")
serverHandle()
