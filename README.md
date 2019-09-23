# 660week7-holsen1
Repository for SWDV-660, Week 7  
Henrik Olsen (0913075)
          
(1) Start "cert-auth.py" - the Certificate Authority (CA)  
(2) Start "server.py" - the server, which need to register with CA that must be running already  
(3) Start client.py - the client, which needs to interact with both server and CA that must be running already  
   
      
Week 7 Assignment Response


1.	How many hours do you estimate that you used in completing this assignment?   
Probably somewhere close to 8 hours, including debugging and answering these assignment questions.
2.	What was the most straightforward part of any task for you?   
I think the encryption I chose to use was the most straightforward part. It is a very simple substitution encryption where I add 10 to the ordinal value of the given character for my public key. My private key is very easy to determine if you know my public key (just a reverse: subtracting 10 from the ordinal value of the character).   
3.	Describe the most frustrating technical challenge you encountered, and how you overcame it.
I spent the most time on connecting to the new server (certificate authority) I created. It was my own fault, however. I copied the code from my server into the new server and changed it to do what it needed to do. I then copied the server code again and put it in my original server and changed the functionality to just send a string basically. I kept getting an error and could not run my server after I had started the certificate authority. I tried all kinds of stuff and was looking the error up on the internet as well. Then I took a short 10-minute break, came back and compared the connection code to my client’s code (technically, my server is now both a server (for the client) and a client (for the certificate authority server) – turns out I was trying to bind to IP and port from both files. I changed the server’s ‘bind’ to a ‘connect’ and it fixed my issues.   
4.	What one part, of the technologies used in this task, would you like to learn more about?
I think in general that encryption is pretty interesting, but maybe not to the detail level of the lecture from MIT. I had never heard of salt and pepper before and I think it’s an interesting concept that might be interesting to learn more about. I am not real sure how adding random salt can ensure the same result every time the hash is computed, unless the salt is also saved somewhere public along with the position to insert it – which seem to kind of defeat the purpose of using salt to begin with…
5.	If you could have one magic piece of documentation that would make this assignment easier, what would it tell you how to do?   
I don’t think I actually needed a magic piece of documentation for this assignment. As usual, I did a lot of prints while coding (and also in my final version) to help keep everything straight. Even with better documentation I would probably have thrown all those print statements in.

