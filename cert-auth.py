#SWDV-660 – Applied DevOps
#Maryville University, 2019
#Week 7 Assignment: Encrypting with Python
#cert-auth.py
#Henrik Olsen (0913075)


import socket


#constants
HOST = '127.0.0.1'
PORT = 9501


def main():
        #create socket and bind it to host and port
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.bind((HOST, PORT))
        #start listening
        connection.listen()

        #create dictionary to hold certifications and public keys
        certs = {}

        print("Certificate Authority running...")
        print("Listening on " + HOST + ":" + str(PORT))

        #run Certificate Server
        runServer = True
        while runServer:
            #initialize CA response
            response = ""

            #create session
            session, addr = connection.accept()

            #get data (string)
            receivedData = session.recv(1024).decode().split(',')
            #action, host, publicKey = receivedData.split(',')
            action = receivedData[0]
            host = receivedData[1]
            publicKey = receivedData[2]
            print("Data received: " + action + "," + host + "," + publicKey)

            if action == 'Register':
                certs[host] = publicKey
                response = "200-OK"

            elif action == 'Validate':
                if host in certs:
                    response = certs[host]
                else:
                    response = None

            else:
                #invalid input received
                response = ""

            #send response to CA client
            if response != "":
                session.send(response.encode())

            #close session
            session.close()


main()
