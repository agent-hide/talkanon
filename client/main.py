from src.imports import *

# Server var ([0] = "ip": str | [1] = "port": int)
# Note: you need to add your servers manually
servers = [
    {
        "ip": "127.0.0.1",
        "port": 667
    },

    {
        "ip": "1.1.1.1",
        "port": 1234
    }
]

menu = f"""{mainColor}
  _        _ _
 | |_ __ _| | |____ _ _ _  ___ _ _
 |  _/ _` | | / / _` | ' \/ _ \ ' \\
  \__\__,_|_|_\_\__,_|_||_\___/_||_|{resetColor}

 |-> The channel based anonymous chat

"""

credits = """
 Developer: hide-wow on github | agent-hide on github | hide#1600 on discord
"""

def connectServer(server: dict, clientInfo: dict):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations("../ssl/CA/ca-cert.pem")

    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client = context.wrap_socket(socket_obj, server_hostname=server["ip"])
    client.connect( ( server["ip"], server["port"] ) )

    client.send(CLIENT_HI)

    returnMsg = client.recv(1024)
    if returnMsg == NICKNAME:
        client.send(clientInfo["nickname"])
    
    returnMsg = client.recv(1024)
    if returnMsg == NONUSER:
        sys.exit("")

def serverMenu():
    clear()
    print(menu)

    i = 1
    for server in servers:
        ip   = server["ip"]
        port = server["port"]
        print(f" [{i}] Server {i} | Info - IP: {ip} PORT: {port}\n")
        i+=1

    def choice():
        serverChoice = input(" Choose a server: ")
        try:
            serverChoice = int(serverChoice)
            try:
                server = servers[serverChoice-1]
                return server
            except:
                print(" Please, use a valid number.")
                serverChoice = ""
                choice()
        except:
            print(" Please use a number.")
            serverChoice = ""
            choice()

    server = choice()

    nickname = input(" Nickname: ")
    password = input(" Password: ")

    client = {
        "nickname": nickname,
        "password": password
    }

    connectServer(server, client)

def mainMenu():
    clear()
    print(menu)

    print(""" [1] Server menu\n [2] Credits\n""")
    
    def choice():
        menuChoice = input(" Choose an option: ")
        
        if menuChoice == "1":
            serverMenu()
        elif menuChoice == "2":
            print(credits)
            choice()
        else:
            print(" Invalid action.")
            choice()

    choice()

if __name__ == "__main__":
    mainMenu()
