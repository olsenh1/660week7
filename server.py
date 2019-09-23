#SWDV-660 – Applied DevOps
#Maryville University, 2019
#Week 7 Assignment: Encrypting with Python
#server.py
#Henrik Olsen (0913075)

#very simple encryption/decryption using substitution cipher


import socket


#constants
HOST = '127.0.0.1'
PORT = 9500

CA_HOST = '127.0.0.1'
CA_PORT = 9501

SERVERNAME = "SecretsServer"
PUBLICKEY = +10
PRIVATEKEY = -10

VALIDATIONTEXT = 'session cipher key'


def registerServer():
    #create socket and connect to host and port
    CA_Connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CA_Connection.connect((CA_HOST, CA_PORT))

    #create certificate string: action, serverName, publicKey
    CA_String = "Register," + SERVERNAME + "," + str(PUBLICKEY)

    #send certificate string to certificate authority server
    CA_Connection.send(CA_String.encode())

    #get response from certificate authority server
    CA_Reply = CA_Connection.recv(1024).decode()

    #close connection to certificate authority server
    CA_Connection.close()

    #return boolean from function depending on result from registration
    return (CA_Reply == "200-OK")


#Decrypt function, using private key
def decrypt(text):
    decryptedText = ''
    for char in text:
        decryptedText += chr(ord(char) + PRIVATEKEY)
    return decryptedText


#Encrypt function, using public key
def encrypt(text):
    encryptedText = ''
    for char in text:
        encryptedText += chr(ord(char) + PUBLICKEY)
    return encryptedText


def main():
    if not registerServer():
        print("")
        print("Error registering server with Certification Authority - Shutting down...")
        exit
    else:
        print("Server successfully registered with Certification Authority...!")

        #run never-ending loop
        while True:
            #create socket and bind it to host and port
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connection.bind((HOST, PORT))

            #start listening
            connection.listen()
            print()
            print("Listening on " + HOST + ":" + str(PORT))

            #start/accept new session
            session, addr = connection.accept()

            #run loop for session
            runServer = True
            while runServer:
                    #get data (string) from client
                    receivedData = session.recv(1024).decode()

                    if receivedData == "Hello":
                        print("'Hello' received, responding with '" + SERVERNAME + "'")
                        outputData = SERVERNAME

                    elif receivedData == "Goodbye":
                        outputData = "Goodbye"
                        runServer = False

                    else:
                        print("Encrypted text received: '" + receivedData + "'")
                        print("Decrypting...")
                        decryptedText = decrypt(receivedData)
                        print("Client request: '" + decryptedText + "'")
                        if decryptedText == VALIDATIONTEXT:
                            outputData = encrypt(VALIDATIONTEXT + ' acknowledgement')
                        else:
                            print("Handling request......")
                            print("Responding with 'OK'")
                            outputData = encrypt("OK")

                    #send response to client
                    print("Response: '" + outputData +"'")
                    session.send(outputData.encode())
                    print()


main()
