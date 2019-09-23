#SWDV-660 – Applied DevOps
#Maryville University, 2019
#Week 7 Assignment: Encrypting with Python
#client.py
#Henrik Olsen (0913075)


import socket


#constants
HOST = '127.0.0.1'
PORT = 9500

CA_HOST = '127.0.0.1'
CA_PORT = 9501

VALIDATIONTEXT = 'session cipher key'


#function that print a "menu" and get user input
def getInput():
    inputStr = ""
    while len(inputStr) == 0:
        print()
        print("Enter '0' (zero) to close client")
        print("Enter anything else and send that to the server")
        print()
        inputStr = input("Input> ")
        print()
        print()
    return inputStr


def validateServer(serverName):
    #create socket and connect to host and port
    CA_Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CA_Connection.connect((CA_HOST, CA_PORT))

    #create certificate string: action, serverName, publicKey
    CA_String = "Validate," + serverName + ","

    #send certificate string to Certificate Authority server
    print("Sending server name to Certificate Authority...")
    CA_Connection.send(CA_String.encode())

    #get response from Certificate Authority server
    CA_Reply = CA_Connection.recv(1024).decode()
    print("Getting response (public key) from Certificate Authority: " + CA_Reply)

    #close connection to Certificate Authority
    CA_Connection.close()

    #return result from Certificate Authority (an int indicating the public key or 0)
    if CA_Reply == None:
        return 0
    else:
        return int(CA_Reply)


#encrypt function, using public key
def encrypt(text, publicKey):
    encryptedText = ''
    for char in text:
        encryptedText += chr(ord(char) + publicKey)
    return encryptedText


def main():
    #initialize local variables
    serverPublicKey = 0
    serverValidated = False

    #create socket and connect to host and port
    serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverConnection.connect((HOST, PORT))
    print("Connecting to server...")

    #send 'Hello' to server
    print("Saying 'Hello' to server")
    serverConnection.send('Hello'.encode())

    #get reply from server - should be server name
    serverReply = serverConnection.recv(1024).decode()
    print("Response from server: " + serverReply)

    #get public key (if it exist) from Certificate Authority
    print("Validating server via Certificate Authority")
    serverPublicKey = validateServer(serverReply)

    if (serverPublicKey == None):
        print("Saying Goodbye to server...")
        serverConnection.send('Goodbye'.encode())
        serverReply = serverConnection.recv(1024).decode()
    else:
        print("Shaking hands with server...")
        serverConnection.send(encrypt(VALIDATIONTEXT, serverPublicKey).encode())

        serverReply = serverConnection.recv(1024).decode()
        print ("server reply: "+ serverReply)
        if (serverReply == encrypt(VALIDATIONTEXT + ' acknowledgement', serverPublicKey)):
            serverValidated = True

    #validation successful - starting session with server
    while serverValidated:
        clientInput = getInput()

        #break session loop if user requests it and say Goodbye to server
        if clientInput == "0":
            serverValidated = False
            serverConnection.send('Goodbye'.encode())
        else:
            #send encrypted client input via connection/socket to server
            serverConnection.send(encrypt(clientInput, serverPublicKey).encode())

            #get response from server and print it out
            serverReply = serverConnection.recv(1024).decode()
            if serverReply == encrypt('OK', serverPublicKey):
                print('"OK" recived from server')
            else:
                print("Encrypted response from server: " + serverReply)


main()
